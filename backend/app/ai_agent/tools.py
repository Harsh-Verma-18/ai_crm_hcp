import json
import re
from datetime import date
 
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
 
from app.ai_agent.db_tools import db_session
from app.ai_agent.llm import llm_extraction
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.models.followup import FollowUp
 
 
# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
 
_TITLE_PREFIX_RE = re.compile(r"^(dr|dr\.|mr|mr\.|mrs|mrs\.|ms|ms\.|prof|prof\.)\s+", re.IGNORECASE)


def _normalize_hcp_name(hcp_name: str) -> str:
    """Strip common titles (Dr., Mr., Prof., ...) so lookups aren't thrown
    off by a prefix the caller included but the stored name doesn't have."""
    return _TITLE_PREFIX_RE.sub("", hcp_name.strip())


def _find_hcp(db, hcp_name: str | None = None, hcp_id: int | None = None):
    if hcp_id:
        return db.query(HCP).filter(HCP.id == hcp_id).first()
    if hcp_name:
        cleaned = _normalize_hcp_name(hcp_name)
        # Try the cleaned name first, then fall back to the raw input,
        # in case the stored name itself includes a title.
        match = db.query(HCP).filter(HCP.name.ilike(f"%{cleaned}%")).first()
        if match:
            return match
        return db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
    return None
 
 
def _extract_json(text: str) -> dict:
    """Best-effort parse of a JSON object out of an LLM response."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
 
 
EXTRACTION_SYSTEM_PROMPT = """You are a pharmaceutical/life-sciences CRM assistant.
Given a field rep's free-text notes about a visit/call with a healthcare
professional (HCP), extract structured data as STRICT JSON with exactly
these keys:
 
- "summary": one or two sentence neutral summary of what happened
- "sentiment": one of "Positive", "Neutral", "Negative" (the HCP's receptiveness)
- "products_discussed": comma-separated product names mentioned, or "" if none
- "next_action": a short recommended next step (e.g. "Send clinical study data")
- "followup_date": an ISO date (YYYY-MM-DD) if the notes imply a follow-up
  timeframe (e.g. "next week" -> compute a plausible date), else null
 
Respond with ONLY the JSON object, no other text.
"""
 
 
def _extract_interaction_fields(raw_notes: str, interaction_type: str) -> dict:
    response = llm_extraction.invoke(
        [
            SystemMessage(content=EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(
                content=f"Interaction type: {interaction_type}\n\nNotes:\n{raw_notes}\n\nToday's date: {date.today().isoformat()}"
            ),
        ]
    )
    data = _extract_json(response.content)
    return {
        "summary": data.get("summary") or raw_notes[:280],
        "sentiment": data.get("sentiment") or "Neutral",
        "products_discussed": data.get("products_discussed") or "",
        "next_action": data.get("next_action") or "",
        "followup_date": data.get("followup_date") or None,
    }
 
 
# ---------------------------------------------------------------------------
# Tool 1: search_hcp
# ---------------------------------------------------------------------------
 
@tool
def search_hcp(city: str) -> str:
    """Search for healthcare professionals (doctors) by city, so the rep can
    pick who to log an interaction against."""
    with db_session() as db:
        doctors = db.query(HCP).filter(HCP.city.ilike(f"%{city}%")).all()
 
        if not doctors:
            return f"No HCPs found in {city}."
 
        lines = [f"Found {len(doctors)} HCP(s) in {city}:"]
        for doc in doctors:
            lines.append(
                f"- Dr. {doc.name} (id={doc.id}), {doc.speciality}, "
                f"{doc.hospital}, {doc.phone}"
            )
        return "\n".join(lines)
 
 
# ---------------------------------------------------------------------------
# Tool 2: log_interaction  (REQUIRED)
# ---------------------------------------------------------------------------
 
@tool
def log_interaction(
    hcp_name: str,
    raw_notes: str,
    interaction_type: str = "Visit",
) -> str:
    """Log a new interaction with an HCP from free-text notes (e.g. dictated
    or typed by the rep in chat). Uses the LLM to extract a summary, the
    HCP's sentiment, products discussed, a recommended next action, and a
    follow-up date from the notes, then saves the interaction to the CRM
    database. `interaction_type` should be one of: Visit, Call, Email,
    Conference.
    """
    with db_session() as db:
        hcp = _find_hcp(db, hcp_name=hcp_name)
        if not hcp:
            return (
                f"I couldn't find an HCP named '{hcp_name}'. "
                f"Try search_hcp first to confirm the name/spelling."
            )
 
        fields = _extract_interaction_fields(raw_notes, interaction_type)
 
        interaction = Interaction(
            hcp_id=hcp.id,
            interaction_type=interaction_type,
            raw_input=raw_notes,
            summary=fields["summary"],
            sentiment=fields["sentiment"],
            products_discussed=fields["products_discussed"],
            next_action=fields["next_action"],
            followup_date=fields["followup_date"],
        )
        db.add(interaction)
        db.flush()  # get interaction.id before commit
 
        return (
            f"Logged interaction #{interaction.id} with Dr. {hcp.name}.\n"
            f"Type: {interaction_type}\n"
            f"Summary: {fields['summary']}\n"
            f"Sentiment: {fields['sentiment']}\n"
            f"Products discussed: {fields['products_discussed'] or 'none'}\n"
            f"Next action: {fields['next_action'] or 'none'}\n"
            f"Follow-up date: {fields['followup_date'] or 'none'}\n"
            f"(You can say 'edit interaction {interaction.id}' to correct anything.)"
        )
 
 
# ---------------------------------------------------------------------------
# Tool 3: edit_interaction  (REQUIRED)
# ---------------------------------------------------------------------------
 
@tool
def edit_interaction(interaction_id: int, change_instructions: str) -> str:
    """Edit a previously logged interaction. `change_instructions` is a
    natural-language description of what to change, e.g. 'set sentiment to
    positive and change the next action to send samples next week'. Only
    the fields mentioned are updated; everything else is left as-is.
    """
    with db_session() as db:
        interaction = (
            db.query(Interaction).filter(Interaction.id == interaction_id).first()
        )
        if not interaction:
            return f"No interaction found with id {interaction_id}."
 
        current = {
            "interaction_type": interaction.interaction_type,
            "products_discussed": interaction.products_discussed,
            "summary": interaction.summary,
            "sentiment": interaction.sentiment,
            "next_action": interaction.next_action,
            "followup_date": interaction.followup_date,
        }
 
        patch_prompt = f"""You are editing a CRM interaction record.
Current record (JSON): {json.dumps(current)}
 
Instruction from the field rep: "{change_instructions}"
 
Return STRICT JSON containing ONLY the fields that should change, using the
same keys as the current record. Do not include unchanged fields. Respond
with ONLY the JSON object."""
 
        response = llm_extraction.invoke([HumanMessage(content=patch_prompt)])
        patch = _extract_json(response.content)
 
        allowed_fields = current.keys()
        applied = {}
        for key, value in patch.items():
            if key in allowed_fields and value not in (None, ""):
                setattr(interaction, key, value)
                applied[key] = value
 
        if not applied:
            return (
                "I couldn't figure out a concrete change from that instruction. "
                "Try being specific, e.g. \"set sentiment to Positive\"."
            )
 
        db.flush()
        changes = ", ".join(f"{k} -> {v}" for k, v in applied.items())
        return f"Updated interaction #{interaction_id}: {changes}"
 
 
# ---------------------------------------------------------------------------
# Tool 4: get_interaction_history
# ---------------------------------------------------------------------------
 
@tool
def get_interaction_history(hcp_name: str) -> str:
    """Get the past logged interactions for an HCP, most recent first. Useful
    before a visit, to prep the rep on prior conversations."""
    with db_session() as db:
        hcp = _find_hcp(db, hcp_name=hcp_name)
        if not hcp:
            return f"I couldn't find an HCP named '{hcp_name}'."
 
        interactions = (
            db.query(Interaction)
            .filter(Interaction.hcp_id == hcp.id)
            .order_by(Interaction.id.desc())
            .limit(10)
            .all()
        )
        if not interactions:
            return f"No interactions logged yet for Dr. {hcp.name}."
 
        lines = [f"Last {len(interactions)} interaction(s) with Dr. {hcp.name}:"]
        for i in interactions:
            lines.append(
                f"#{i.id} [{i.interaction_type}] {i.summary} "
                f"(sentiment: {i.sentiment}, next: {i.next_action or 'n/a'})"
            )
        return "\n".join(lines)
 
 
# ---------------------------------------------------------------------------
# Tool 5: create_followup
# ---------------------------------------------------------------------------
 
@tool
def create_followup(hcp_name: str, task: str, due_date: str) -> str:
    """Create a follow-up task for an HCP. `due_date` should be an ISO date
    string (YYYY-MM-DD)."""
    with db_session() as db:
        hcp = _find_hcp(db, hcp_name=hcp_name)
        if not hcp:
            return f"I couldn't find an HCP named '{hcp_name}'."
 
        try:
            parsed_date = date.fromisoformat(due_date)
        except ValueError:
            parsed_date = None
 
        followup = FollowUp(
            hcp_id=hcp.id,
            task=task,
            due_date=parsed_date,
            status="Pending",
        )
        db.add(followup)
        db.flush()
 
        return (
            f"Follow-up #{followup.id} created for Dr. {hcp.name}: "
            f"'{task}' due {due_date}."
        )
 
 
ALL_TOOLS = [
    search_hcp,
    log_interaction,
    edit_interaction,
    get_interaction_history,
    create_followup,
]