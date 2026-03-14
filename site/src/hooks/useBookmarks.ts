import { useState, useCallback, useEffect } from 'react'

export interface Bookmark {
  entityType: string
  entityId: string
  title: string
  addedAt: string
}

const STORAGE_KEY = 'querypat_bookmarks'

function loadBookmarks(): Bookmark[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function saveBookmarks(bookmarks: Bookmark[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(bookmarks))
}

// Global listeners for cross-component sync
const listeners = new Set<() => void>()

function notify() {
  listeners.forEach(fn => fn())
}

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>(loadBookmarks)

  useEffect(() => {
    const refresh = () => setBookmarks(loadBookmarks())
    listeners.add(refresh)
    return () => { listeners.delete(refresh) }
  }, [])

  const toggle = useCallback((entityType: string, entityId: string, title: string) => {
    const current = loadBookmarks()
    const idx = current.findIndex(b => b.entityType === entityType && b.entityId === entityId)
    if (idx >= 0) {
      current.splice(idx, 1)
    } else {
      current.push({ entityType, entityId, title, addedAt: new Date().toISOString() })
    }
    saveBookmarks(current)
    setBookmarks(current)
    notify()
  }, [])

  const isBookmarked = useCallback((entityType: string, entityId: string) => {
    return bookmarks.some(b => b.entityType === entityType && b.entityId === entityId)
  }, [bookmarks])

  return { bookmarks, toggle, isBookmarked }
}
