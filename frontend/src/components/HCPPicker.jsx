import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { selectHcp, selectHcps, selectSelectedHcp } from '../store/hcpSlice'

function initials(name) {
  return name
    .split(' ')
    .map((p) => p[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()
}

export default function HCPPicker() {
  const dispatch = useDispatch()
  const hcps = useSelector(selectHcps)
  const selected = useSelector(selectSelectedHcp)

  return (
    <div className="hcp-picker">
      <label className="field-label" htmlFor="hcp-select">
        Interacting with
      </label>
      <select
        id="hcp-select"
        className="hcp-picker__select"
        value={selected?.id || ''}
        onChange={(e) => dispatch(selectHcp(Number(e.target.value)))}
      >
        {hcps.length === 0 && <option value="">No HCPs yet</option>}
        {hcps.map((h) => (
          <option key={h.id} value={h.id}>
            {h.name} — {h.speciality}
          </option>
        ))}
      </select>

      {selected && (
        <div className="hcp-card">
          <div className="hcp-card__avatar">{initials(selected.name)}</div>
          <div className="hcp-card__body">
            <p className="hcp-card__name">{selected.name}</p>
            <p className="hcp-card__meta">
              {selected.speciality} · {selected.hospital} · {selected.city}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
