import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { selectSelectedHcp } from '../store/hcpSlice'
import { fetchInteractionsForHcp, selectInteractionsForHcp } from '../store/interactionSlice'

const SENTIMENT_CLASS = {
  Positive: 'tag--positive',
  Neutral: 'tag--neutral',
  Negative: 'tag--negative',
}

export default function InteractionTimeline() {
  const dispatch = useDispatch()
  const selectedHcp = useSelector(selectSelectedHcp)
  const interactions = useSelector(
    selectInteractionsForHcp(selectedHcp?.id)
  )

  useEffect(() => {
    if (selectedHcp) {
      dispatch(fetchInteractionsForHcp(selectedHcp.id))
    }
  }, [dispatch, selectedHcp])

  if (!selectedHcp) return null

  return (
    <aside className="timeline">
      <h2 className="timeline__title">Recent history</h2>
      {interactions.length === 0 && (
        <p className="empty-hint">No interactions logged yet with {selectedHcp.name}.</p>
      )}
      <ul className="timeline__list">
        {interactions.map((i) => (
          <li key={i.id} className="timeline__item">
            <div className="timeline__item-head">
              <span className="timeline__item-type">{i.interaction_type}</span>
              {i.sentiment && (
                <span className={`tag ${SENTIMENT_CLASS[i.sentiment] || ''}`}>
                  {i.sentiment}
                </span>
              )}
            </div>
            <p className="timeline__item-summary">{i.summary}</p>
            {i.next_action && (
              <p className="timeline__item-next">Next: {i.next_action}</p>
            )}
          </li>
        ))}
      </ul>
    </aside>
  )
}
