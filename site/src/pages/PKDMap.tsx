import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  allLocations,
  californiaLocations,
  expansionCandidates,
  locationCategoryLabel,
  locationCategoryTone,
  type PKDLocationCategory,
  type PKDGeographyLocation,
} from '../data/pkdGeography'

declare global {
  interface Window {
    L?: any
  }
}

const LEAFLET_CSS_ID = 'pkd-leaflet-css'
const LEAFLET_JS_ID = 'pkd-leaflet-js'

function loadLeaflet(): Promise<any> {
  if (window.L) return Promise.resolve(window.L)

  return new Promise((resolve, reject) => {
    if (!document.getElementById(LEAFLET_CSS_ID)) {
      const link = document.createElement('link')
      link.id = LEAFLET_CSS_ID
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      link.crossOrigin = ''
      document.head.appendChild(link)
    }

    const existingScript = document.getElementById(LEAFLET_JS_ID) as HTMLScriptElement | null
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve(window.L))
      existingScript.addEventListener('error', () => reject(new Error('Leaflet failed to load')))
      return
    }

    const script = document.createElement('script')
    script.id = LEAFLET_JS_ID
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.crossOrigin = ''
    script.onload = () => resolve(window.L)
    script.onerror = () => reject(new Error('Leaflet failed to load'))
    document.head.appendChild(script)
  })
}

function markerHtml(color: string) {
  return `<div class="pkd-map-pin" style="background:${color}">
    <span style="background:${color};box-shadow:0 0 0 4px rgba(255,255,255,0.78),0 0 0 7px ${color}22"></span>
  </div>`
}

function popupHtml(location: PKDGeographyLocation) {
  return `
    <div class="pkd-popup">
      <div class="pkd-popup-kicker">${location.category}</div>
      <div class="pkd-popup-kind">${location.kind}</div>
      <h3>${location.label}</h3>
      <div class="pkd-popup-address">${location.address}, ${location.city}, ${location.state}</div>
      <p>${location.significance}</p>
      <div class="pkd-popup-meta">
        <span><strong>Years:</strong> ${location.years}</span>
        <span><strong>Source:</strong> ${location.source}</span>
      </div>
    </div>
  `
}

function tooltipText(location: PKDGeographyLocation) {
  const summary = location.significance.length > 120 ? `${location.significance.slice(0, 117)}...` : location.significance
  return `${location.label} — ${summary}`
}

export default function PKDMap() {
  const mapRef = useRef<HTMLDivElement | null>(null)
  const leafletMapRef = useRef<any>(null)
  const markerRefs = useRef<Map<string, any>>(new Map())
  const [selectedId, setSelectedId] = useState<string>(californiaLocations[0]?.id ?? '')
  const [categoryFilter, setCategoryFilter] = useState<'all' | PKDLocationCategory>('all')
  const [search, setSearch] = useState('')
  const [mapReady, setMapReady] = useState(false)

  const visibleCalifornia = useMemo(() => {
    const q = search.trim().toLowerCase()
    return californiaLocations.filter(loc => {
      const matchesCategory = categoryFilter === 'all' || loc.category === categoryFilter
      const haystack = `${loc.label} ${loc.address} ${loc.city} ${loc.significance} ${loc.years} ${loc.category} ${loc.kind}`.toLowerCase()
      const matchesSearch = !q || haystack.includes(q)
      return matchesCategory && matchesSearch
    })
  }, [categoryFilter, search])

  const activeSelectedId =
    visibleCalifornia.some(loc => loc.id === selectedId)
      ? selectedId
      : visibleCalifornia[0]?.id || californiaLocations[0]?.id || ''

  const selectedLocation = useMemo(
    () => visibleCalifornia.find(loc => loc.id === activeSelectedId) || visibleCalifornia[0] || californiaLocations[0],
    [activeSelectedId, visibleCalifornia]
  )

  const californiaCategories = new Set(californiaLocations.map(loc => loc.category))

  useEffect(() => {
    let disposed = false
    let map: any

    loadLeaflet()
      .then(L => {
        if (disposed || !mapRef.current) return

        map = L.map(mapRef.current, {
          zoomControl: true,
          scrollWheelZoom: false,
          attributionControl: true,
          minZoom: 5,
          maxZoom: 12,
        })

        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
          attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        }).addTo(map)

        const bounds = L.latLngBounds([])

        californiaLocations.forEach(loc => {
          const icon = L.divIcon({
            className: 'pkd-map-icon',
            html: markerHtml(locationCategoryTone(loc.category)),
            iconSize: [20, 20],
            iconAnchor: [10, 10],
            popupAnchor: [0, -10],
          })

          const marker = L.marker([loc.lat, loc.lng], { icon }).addTo(map)
          marker.bindPopup(popupHtml(loc), { className: 'pkd-map-popup' })
          marker.bindTooltip(tooltipText(loc), {
            className: 'pkd-map-tooltip',
            direction: 'top',
            sticky: true,
            opacity: 0.98,
          })
          marker.on('click', () => setSelectedId(loc.id))
          marker.on('mouseover', () => marker.openTooltip())
          marker.on('mouseout', () => marker.closeTooltip())
          marker.on('popupopen', () => setSelectedId(loc.id))

          markerRefs.current.set(loc.id, marker)
          bounds.extend([loc.lat, loc.lng])
        })

        if (californiaLocations.length > 1) {
          map.fitBounds(bounds.pad(0.12))
        } else if (californiaLocations[0]) {
          map.setView([californiaLocations[0].lat, californiaLocations[0].lng], 9)
        }

        leafletMapRef.current = map
        setMapReady(true)
      })
      .catch(() => setMapReady(false))

    return () => {
      disposed = true
      markerRefs.current.clear()
      if (leafletMapRef.current) {
        leafletMapRef.current.remove()
        leafletMapRef.current = null
      }
    }
  }, [])

  useEffect(() => {
    const map = leafletMapRef.current
    const marker = markerRefs.current.get(activeSelectedId)
    if (!map || !marker) return
    map.panTo(marker.getLatLng(), { animate: true, duration: 0.5 })
    marker.openPopup()
  }, [activeSelectedId])

  return (
    <>
      <div className="page-header geography-header">
        <div>
          <h1>Philip K. Dick Geography</h1>
          <p>
            California first: a live map of the places Dick lived, worked, and kept returning to in the novels,
            with a catalog below that keeps the out-of-state and international sites ready for the next expansion.
          </p>
        </div>
        <div className="geography-header-links">
          <Link to="/biography">Biography</Link>
          <Link to="/archive">Source documents</Link>
          <Link to="/timeline">Timeline</Link>
        </div>
      </div>

      <div className="stats-grid geography-stats">
        <div className="stat-card">
          <div className="stat-value">{californiaLocations.length}</div>
          <div className="stat-label">California map points</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{californiaCategories.size}</div>
          <div className="stat-label">Color categories</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{allLocations.length}</div>
          <div className="stat-label">Total catalog entries</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{expansionCandidates.length}</div>
          <div className="stat-label">Expansion candidates</div>
        </div>
      </div>

      <div className="detail-section geography-intro">
        <p>
          The current map keeps the view tight on California because that is where the biography becomes
          spatially dense: Berkeley, Point Reyes, Marin County, Fullerton, and Santa Ana are doing a lot of the
          interpretive work. The colors now separate biography, novel settings, short-story settings, university
          and archive sites, and public events, so the fiction geography and the life chronology can sit on the
          same surface without blurring together. The catalog includes non-California places from the same
          chronology so we can judge whether a broader map would still scan cleanly.
        </p>
      </div>

      <section className="geography-shell">
        <div className="geography-map-panel card">
          <div className="geography-toolbar">
            <div className="geography-filter-row">
              {(['all', 'Biography', 'Novel setting', 'Short story setting', 'Institutional site', 'Event'] as const).map(category => (
                <button
                  key={category}
                  type="button"
                  className={categoryFilter === category ? 'filter-chip active' : 'filter-chip'}
                  onClick={() => setCategoryFilter(category)}
                >
                  {category === 'all' ? 'All categories' : category}
                </button>
              ))}
            </div>
            <input
              className="search-input geography-search"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search addresses, cities, or site notes"
              aria-label="Search geography locations"
            />
          </div>

          <div className="geography-map-wrap">
            <div ref={mapRef} className="geography-map" aria-label="Map of California PKD locations" />
            {!mapReady && <div className="geography-map-loading">Loading map...</div>}
          </div>

          <div className="map-legend">
            {(['Biography', 'Novel setting', 'Short story setting', 'Institutional site', 'Event'] as const).map(category => (
              <span key={category} className="legend-item">
                <span className="legend-swatch" style={{background: locationCategoryTone(category)}} />
                {locationCategoryLabel(category)}
              </span>
            ))}
          </div>
        </div>

        <aside className="geography-sidebar">
          <div className="detail-section">
            <h2>Selected place</h2>
            {selectedLocation ? (
              <div className="selected-place">
                <div className="selected-place-kind" style={{ color: locationCategoryTone(selectedLocation.category) }}>
                  {selectedLocation.category}
                </div>
                <div className="selected-place-kind-secondary">{selectedLocation.kind}</div>
                <h3>{selectedLocation.label}</h3>
                <div className="selected-place-address">
                  {selectedLocation.address}, {selectedLocation.city}, {selectedLocation.state}
                </div>
                <p>{selectedLocation.significance}</p>
                <dl className="selected-place-meta">
                  <div>
                    <dt>Years</dt>
                    <dd>{selectedLocation.years}</dd>
                  </div>
                  <div>
                    <dt>Status</dt>
                    <dd>{selectedLocation.status === 'mapped' ? 'On California map' : 'Catalog only'}</dd>
                  </div>
                  <div>
                    <dt>Source</dt>
                    <dd>{selectedLocation.source}</dd>
                  </div>
                </dl>
              </div>
            ) : null}
          </div>

          <div className="detail-section">
            <h2>California catalog</h2>
            <div className="location-list">
              {visibleCalifornia.map(loc => (
                <button
                  key={loc.id}
                  type="button"
                  className={activeSelectedId === loc.id ? 'location-row active' : 'location-row'}
                  onClick={() => setSelectedId(loc.id)}
                >
                  <span className="location-row-top">
                    <strong>{loc.label}</strong>
                    <span className="location-row-kind" style={{ color: locationCategoryTone(loc.category) }}>
                      {loc.category}
                    </span>
                  </span>
                  <span className="location-row-sub">
                    {loc.city}, {loc.state} | {loc.years} | {loc.kind}
                  </span>
                  <span className="location-row-note">{loc.significance}</span>
                </button>
              ))}
            </div>
          </div>
        </aside>
      </section>

      <section className="detail-section geography-catalog">
        <h2>Catalog for expansion</h2>
        <p>
          These are the first non-California anchors I would expand into if we decide the map should grow beyond
          the state boundary.
        </p>
        <div className="catalog-table-wrap">
          <table className="catalog-table">
            <thead>
              <tr>
                <th>Place</th>
                <th>Status</th>
                <th>Category</th>
                <th>Type</th>
                <th>Why it matters</th>
              </tr>
            </thead>
            <tbody>
              {expansionCandidates.map(loc => (
                <tr key={loc.id}>
                  <td>
                    <strong>{loc.label}</strong>
                    <div className="catalog-place-meta">
                      {loc.city}, {loc.state}
                    </div>
                  </td>
                  <td>{loc.status === 'mapped' ? 'Mapped' : 'Catalog only'}</td>
                  <td>
                    <span className="catalog-category" style={{ color: locationCategoryTone(loc.category) }}>
                      {loc.category}
                    </span>
                  </td>
                  <td>{loc.kind}</td>
                  <td>{loc.significance}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </>
  )
}
