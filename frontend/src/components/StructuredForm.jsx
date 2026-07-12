import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { selectSelectedHcp } from '../store/hcpSlice'
import { submitInteraction } from '../store/interactionSlice'

const INTERACTION_TYPES = ['Visit', 'Call', 'Email', 'Conference']
const SENTIMENTS = ['Positive', 'Neutral', 'Negative']

const emptyForm = {
  interaction_type: 'Visit',
  products_discussed: '',
  summary: '',
  sentiment: 'Neutral',
  next_action: '',
  followup_date: '',
}

export default function StructuredForm() {
  const dispatch = useDispatch()
  const selectedHcp = useSelector(selectSelectedHcp)
  const submitStatus = useSelector((s) => s.interactions.submitStatus)
  const [form, setForm] = useState(emptyForm)
  const [savedId, setSavedId] = useState(null)

  const update = (field) => (e) =>
    setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedHcp) return

    const result = await dispatch(
      submitInteraction({
        hcp_id: selectedHcp.id,
        interaction_type: form.interaction_type,
        products_discussed: form.products_discussed || null,
        raw_input: form.summary,
        summary: form.summary,
        sentiment: form.sentiment,
        next_action: form.next_action || null,
        followup_date: form.followup_date || null,
      })
    )

    if (submitInteraction.fulfilled.match(result)) {
      setSavedId(result.payload.id)
      setForm(emptyForm)
    }
  }

  if (!selectedHcp) {
    return <p className="empty-hint">Pick an HCP above to log an interaction.</p>
  }

  return (
    <form className="log-form" onSubmit={handleSubmit}>
      <div className="log-form__row">
        <div className="field">
          <label className="field-label" htmlFor="interaction_type">
            Type
          </label>
          <select
            id="interaction_type"
            value={form.interaction_type}
            onChange={update('interaction_type')}
          >
            {INTERACTION_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label className="field-label" htmlFor="sentiment">
            Sentiment
          </label>
          <select id="sentiment" value={form.sentiment} onChange={update('sentiment')}>
            {SENTIMENTS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label className="field-label" htmlFor="followup_date">
            Follow-up date
          </label>
          <input
            id="followup_date"
            type="date"
            value={form.followup_date}
            onChange={update('followup_date')}
          />
        </div>
      </div>

      <div className="field">
        <label className="field-label" htmlFor="products_discussed">
          Products discussed
        </label>
        <input
          id="products_discussed"
          type="text"
          placeholder="e.g. CardioPlus 10mg, OncoShield IV"
          value={form.products_discussed}
          onChange={update('products_discussed')}
        />
      </div>

      <div className="field">
        <label className="field-label" htmlFor="summary">
          What happened
        </label>
        <textarea
          id="summary"
          rows={4}
          required
          placeholder="Notes from the visit or call..."
          value={form.summary}
          onChange={update('summary')}
        />
      </div>

      <div className="field">
        <label className="field-label" htmlFor="next_action">
          Next action
        </label>
        <input
          id="next_action"
          type="text"
          placeholder="e.g. Send samples, schedule follow-up"
          value={form.next_action}
          onChange={update('next_action')}
        />
      </div>

      <div className="log-form__footer">
        {savedId && (
          <span className="log-form__saved">Saved as interaction #{savedId}</span>
        )}
        <button type="submit" className="btn-primary" disabled={submitStatus === 'loading'}>
          {submitStatus === 'loading' ? 'Saving…' : 'Save interaction'}
        </button>
      </div>
    </form>
  )
}
