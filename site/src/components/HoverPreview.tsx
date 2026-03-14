import { useState, useRef, useEffect } from 'react'
import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'

interface PreviewData {
  title: string
  type: string
  description: string
}

interface HoverPreviewProps {
  to: string
  children: ReactNode
  className?: string
  style?: React.CSSProperties
  title?: string
}

const BASE = import.meta.env.BASE_URL + 'data/'

// Cache fetched previews in memory
const previewCache = new Map<string, PreviewData | null>()

function parseRoute(to: string): { dataPath: string; type: string } | null {
  const m = to.match(/^\/dictionary\/(.+)$/)
  if (m) return { dataPath: `dictionary/terms/${m[1]}.json`, type: 'Dictionary Term' }

  const n = to.match(/^\/names\/(.+)$/)
  if (n) return { dataPath: `names/entities/${n[1]}.json`, type: 'Name' }

  const a = to.match(/^\/archive\/(.+)$/)
  if (a) return { dataPath: `archive/docs/${a[1]}.json`, type: 'Archive Document' }

  const s = to.match(/^\/segments\/(.+)$/)
  if (s) return { dataPath: `segments/${s[1]}.json`, type: 'Exegesis Summary' }

  return null
}

function extractPreview(data: Record<string, unknown>, type: string): PreviewData {
  const title = (data.canonical_name || data.canonical_form || data.title || '') as string
  let description = ''
  if (data.card_description) description = data.card_description as string
  else if (data.definition) description = data.definition as string
  else if (data.concise_summary) description = data.concise_summary as string
  else if (data.card_summary) description = data.card_summary as string

  if (description.length > 180) description = description.slice(0, 180) + '...'

  return { title, type, description }
}

export default function HoverPreview({ to, children, className, style, title: titleProp }: HoverPreviewProps) {
  const [preview, setPreview] = useState<PreviewData | null>(null)
  const [visible, setVisible] = useState(false)
  const [position, setPosition] = useState<'below' | 'above'>('below')
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const linkRef = useRef<HTMLAnchorElement>(null)

  const showPreview = () => {
    timeoutRef.current = setTimeout(() => {
      setVisible(true)
      // Determine position
      if (linkRef.current) {
        const rect = linkRef.current.getBoundingClientRect()
        setPosition(rect.top > window.innerHeight * 0.6 ? 'above' : 'below')
      }
      // Fetch data if needed
      const route = parseRoute(to)
      if (!route) return

      if (previewCache.has(to)) {
        setPreview(previewCache.get(to) || null)
        return
      }

      fetch(BASE + route.dataPath)
        .then(r => { if (r.ok) return r.json(); return null })
        .then(data => {
          if (!data) { previewCache.set(to, null); return }
          const p = extractPreview(data, route.type)
          previewCache.set(to, p)
          setPreview(p)
        })
        .catch(() => previewCache.set(to, null))
    }, 300)
  }

  const hidePreview = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current)
    setVisible(false)
    setPreview(null)
  }

  useEffect(() => {
    return () => { if (timeoutRef.current) clearTimeout(timeoutRef.current) }
  }, [])

  return (
    <span
      className="hover-preview-wrapper"
      onMouseEnter={showPreview}
      onMouseLeave={hidePreview}
    >
      <Link ref={linkRef} to={to} className={className} style={style} title={titleProp}>
        {children}
      </Link>
      {visible && preview && (
        <div className={`hover-preview-card hover-preview-${position}`}>
          <div className="hover-preview-type">{preview.type}</div>
          <div className="hover-preview-title">{preview.title}</div>
          {preview.description && (
            <div className="hover-preview-desc">{preview.description}</div>
          )}
        </div>
      )}
    </span>
  )
}
