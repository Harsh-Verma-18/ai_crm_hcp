import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setMode } from '../store/uiSlice'

export default function ModeToggle() {
  const dispatch = useDispatch()
  const mode = useSelector((s) => s.ui.mode)

  return (
    <div className="mode-toggle" role="tablist" aria-label="Logging method">
      <span
        className="mode-toggle__indicator"
        style={{ transform: mode === 'chat' ? 'translateX(100%)' : 'translateX(0)' }}
        aria-hidden="true"
      />
      <button
        type="button"
        role="tab"
        aria-selected={mode === 'form'}
        className={`mode-toggle__btn ${mode === 'form' ? 'is-active' : ''}`}
        onClick={() => dispatch(setMode('form'))}
      >
        Structured form
      </button>
      <button
        type="button"
        role="tab"
        aria-selected={mode === 'chat'}
        className={`mode-toggle__btn ${mode === 'chat' ? 'is-active' : ''}`}
        onClick={() => dispatch(setMode('chat'))}
      >
        Chat with assistant
      </button>
    </div>
  )
}
