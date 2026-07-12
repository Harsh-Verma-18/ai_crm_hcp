import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { fetchHcps } from './store/hcpSlice'
import LogInteractionScreen from './components/LogInteractionScreen'
import './App.css'

export default function App() {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(fetchHcps())
  }, [dispatch])

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header__brand">
          <span className="app-header__mark" aria-hidden="true" />
          <div>
            <p className="app-header__eyebrow">Field CRM</p>
            <h1 className="app-header__title">Log Interaction</h1>
          </div>
        </div>
      </header>
      <main className="app-main">
        <LogInteractionScreen />
      </main>
    </div>
  )
}
