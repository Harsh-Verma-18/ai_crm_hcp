import React, { useEffect, useRef, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { queueUserMessage, sendChatMessage } from '../store/chatSlice'

export default function ChatPanel() {
  const dispatch = useDispatch()
  const { messages, status, threadId } = useSelector((s) => s.chat)
  const [draft, setDraft] = useState('')
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, status])

  const handleSend = (e) => {
    e.preventDefault()
    const text = draft.trim()
    if (!text || status === 'sending') return
    dispatch(queueUserMessage(text))
    dispatch(sendChatMessage({ message: text, threadId }))
    setDraft('')
  }

  return (
    <div className="chat-panel">
      <div className="chat-panel__log" ref={scrollRef}>
        {messages.length === 0 && (
          <p className="empty-hint">
            Tell the assistant what happened — e.g. "Log a visit with Dr. Asha Rao,
            discussed CardioPlus 10mg, she was positive, follow up next week."
          </p>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`chat-bubble chat-bubble--${m.role}`}>
            {m.text}
          </div>
        ))}
        {status === 'sending' && (
          <div className="chat-bubble chat-bubble--assistant chat-bubble--pending">
            <span className="pulse-line" aria-hidden="true">
              <svg viewBox="0 0 120 24" width="72" height="16">
                <polyline
                  points="0,12 24,12 32,2 40,22 48,12 120,12"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </span>
            <span className="sr-only">Assistant is thinking</span>
          </div>
        )}
      </div>

      <form className="chat-panel__composer" onSubmit={handleSend}>
        <input
          type="text"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Describe the visit, call, or email…"
          aria-label="Message"
        />
        <button type="submit" className="btn-primary" disabled={status === 'sending'}>
          Send
        </button>
      </form>
    </div>
  )
}
