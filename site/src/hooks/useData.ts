import { useState, useEffect } from 'react'

const BASE = import.meta.env.BASE_URL + 'data/'

export function useData<T>(path: string): { data: T | null; loading: boolean; error: string | null } {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(BASE + path)
      .then(r => {
        if (!r.ok) throw new Error(`Failed to load ${path}: ${r.status}`)
        return r.json()
      })
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [path])

  return { data, loading, error }
}
