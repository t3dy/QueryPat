import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import LaneFilter from './LaneFilter'
import LaneBadge from './LaneBadge'

interface Passage {
  passage_id: number
  lane: string
  source_mode: string
  doc_id: string
  doc_title: string
  passage_text: string
  matched_terms: string[]
  claim_type: string
  confidence: string
  /** Exegesis segment this excerpt was cut from, when there is one. */
  seg_id?: string | null
  /** Human-readable source line, e.g. "Letter to Brig Elliot, April 15, 1981". */
  citation?: string | null
  date?: string | null
}

interface EvidencePacket {
  ev_id: string
  claim_text: string
  evidence_summary: string
  confidence: string
  source_method: string
  lane_a_count: number
  lane_b_count: number
  lane_c_count: number
  passages: Passage[]
}

interface EvidencePanelProps {
  packets: EvidencePacket[]
}

export default function EvidencePanel({ packets }: EvidencePanelProps) {
  const [activeLanes, setActiveLanes] = useState<string[] | null>(null)
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  function togglePacket(evId: string) {
    setExpanded(prev => {
      const next = new Set(prev)
      if (next.has(evId)) next.delete(evId)
      else next.add(evId)
      return next
    })
  }

  const availableLanes = useMemo(() => {
    const seen = new Set<string>()
    for (const pkt of packets ?? []) {
      for (const p of pkt.passages ?? []) seen.add(p.lane)
    }
    return ['A', 'B', 'C', 'D', 'E'].filter(l => seen.has(l))
  }, [packets])

  // Until the filter is touched, every lane present in the data is shown.
  const laneSet = useMemo(
    () => new Set(activeLanes ?? availableLanes),
    [activeLanes, availableLanes],
  )

  if (!packets || packets.length === 0) return null

  return (
    <div className="detail-section">
      <h2>Evidence</h2>
      <LaneFilter onChange={setActiveLanes} lanes={availableLanes} />
      <div className="evidence-packets">
        {packets.map(pkt => {
          const filteredPassages = pkt.passages.filter(p => laneSet.has(p.lane))
          if (filteredPassages.length === 0) return null
          const isOpen = expanded.has(pkt.ev_id)
          return (
            <div key={pkt.ev_id} className="evidence-packet card">
              <div
                className="evidence-packet-header"
                onClick={() => togglePacket(pkt.ev_id)}
                style={{ cursor: 'pointer' }}
              >
                <div style={{ flex: 1 }}>
                  <p className="evidence-claim">{pkt.claim_text}</p>
                  <div className="card-meta" style={{ marginTop: '0.4rem' }}>
                    <span className={`badge badge-confidence-${pkt.confidence}`}>
                      {pkt.confidence}
                    </span>
                    <span>{filteredPassages.length} passage{filteredPassages.length !== 1 ? 's' : ''}</span>
                  </div>
                </div>
                <span className="evidence-toggle">{isOpen ? '\u25B2' : '\u25BC'}</span>
              </div>
              {isOpen && (
                <div className="evidence-passages">
                  {pkt.evidence_summary && (
                    <p style={{ fontSize: '0.88rem', lineHeight: 1.6, marginBottom: '0.75rem', color: 'var(--text-secondary)' }}>
                      {pkt.evidence_summary}
                    </p>
                  )}
                  {filteredPassages.map(p => (
                    <div key={p.passage_id} className="evidence-passage">
                      <div className="card-meta" style={{ marginBottom: '0.35rem' }}>
                        <LaneBadge lane={p.lane} />
                        <span style={{ fontWeight: 600 }}>
                          {p.citation || p.doc_title}
                        </span>
                        {p.seg_id && (
                          <Link to={`/segments/${p.seg_id}`}>Read the entry &rarr;</Link>
                        )}
                      </div>
                      <div className="evidence-excerpt">{p.passage_text}</div>
                      {p.matched_terms && p.matched_terms.length > 0 && (
                        <div className="card-meta" style={{ marginTop: '0.3rem' }}>
                          {p.matched_terms.map(t => (
                            <span key={t} className="entity-tag">{t}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
