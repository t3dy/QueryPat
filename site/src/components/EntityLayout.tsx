import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import BookmarkButton from './BookmarkButton'

interface Badge {
  label: string
  className?: string
}

interface EntityLayoutProps {
  title: string
  entityType: string
  entityId: string
  badges?: Badge[]
  description?: string | null
  tags?: { label: string; to?: string }[]
  backLink?: { label: string; to: string }
  children: ReactNode
  footer?: ReactNode
}

export default function EntityLayout({
  title,
  entityType,
  entityId,
  badges,
  description,
  tags,
  backLink,
  children,
  footer,
}: EntityLayoutProps) {
  return (
    <>
      <div className="page-header entity-header">
        <div className="entity-title-row">
          <h1>{title}</h1>
          <BookmarkButton entityType={entityType} entityId={entityId} title={title} />
        </div>
        <p>
          {badges?.map((b, i) => (
            <span key={i} className={`badge ${b.className || 'badge-category'}`} style={{ marginRight: '0.5rem' }}>
              {b.label}
            </span>
          ))}
        </p>
        {description && (
          <p style={{ marginTop: '0.35rem', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
            {description}
          </p>
        )}
        {tags && tags.length > 0 && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.5rem' }}>
            {tags.map((t, i) =>
              t.to ? (
                <Link key={i} to={t.to} className="entity-tag" style={{ textDecoration: 'none' }}>
                  {t.label}
                </Link>
              ) : (
                <span key={i} className="entity-tag">{t.label}</span>
              )
            )}
          </div>
        )}
      </div>

      <div className="entity-content">
        {children}
      </div>

      {footer}

      {backLink && (
        <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
          <Link to={backLink.to}>{backLink.label}</Link>
        </div>
      )}
    </>
  )
}
