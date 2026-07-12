import React from 'react'
import { useSelector } from 'react-redux'
import HCPPicker from './HCPPicker'
import ModeToggle from './ModeToggle'
import StructuredForm from './StructuredForm'
import ChatPanel from './ChatPanel'
import InteractionTimeline from './InteractionTimeline'

export default function LogInteractionScreen() {
  const mode = useSelector((s) => s.ui.mode)

  return (
    <div className="screen">
      <section className="screen__panel">
        <HCPPicker />
        <ModeToggle />
        <div className="screen__body">
          {mode === 'form' ? <StructuredForm /> : <ChatPanel />}
        </div>
      </section>
      <InteractionTimeline />
    </div>
  )
}
