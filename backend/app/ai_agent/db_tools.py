from contextlib import contextmanager
from app.database import SessionLocal
 
 
@contextmanager
def db_session():
    """
    Short-lived DB session for use inside a single tool call.
 
    Tools run inside a LangGraph node, outside of FastAPI's request-scoped
    `Depends(get_db)`, so each tool opens/closes its own session via this
    context manager to avoid leaking connections across turns.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
 