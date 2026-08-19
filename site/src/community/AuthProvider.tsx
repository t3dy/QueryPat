import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'
import type { Session } from '@supabase/supabase-js'
import { communityEnabled, db, fetchProfile, supabase, type Profile } from '../lib/supabase'
import { AuthContext, type AuthState } from './auth-context'

/** Where Supabase should send people back to after an email link or OAuth hop. */
export function authRedirectUrl() {
  return window.location.origin + import.meta.env.BASE_URL
}

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(communityEnabled)

  useEffect(() => {
    if (!supabase) return
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session)
      setLoading(false)
    })
    const { data: sub } = supabase.auth.onAuthStateChange((_event, next) => {
      setSession(next)
      setLoading(false)
    })
    return () => sub.subscription.unsubscribe()
  }, [])

  const userId = session?.user.id ?? null

  const refreshProfile = useCallback(async () => {
    if (!userId) return setProfile(null)
    setProfile(await fetchProfile(userId))
  }, [userId])

  useEffect(() => {
    if (!communityEnabled) return
    void refreshProfile()
  }, [refreshProfile])

  const value = useMemo<AuthState>(() => ({
    enabled: communityEnabled,
    loading,
    session,
    user: session?.user ?? null,
    profile,
    isModerator: profile?.role === 'moderator' || profile?.role === 'admin',

    async signInWithEmail(email) {
      const { error } = await db().auth.signInWithOtp({
        email,
        options: { emailRedirectTo: authRedirectUrl() },
      })
      if (error) throw error
    },

    async signInWithOAuth(provider) {
      const { error } = await db().auth.signInWithOAuth({
        provider,
        options: { redirectTo: authRedirectUrl() },
      })
      if (error) throw error
    },

    async signOut() {
      await db().auth.signOut()
      setProfile(null)
    },

    async saveProfile(patch) {
      if (!userId) throw new Error('Not signed in')
      const { error } = await db()
        .from('profiles')
        .upsert({ id: userId, ...patch }, { onConflict: 'id' })
      if (error) {
        throw new Error(
          error.code === '23505'
            ? 'That username is already taken.'
            : error.message,
        )
      }
      await refreshProfile()
    },

    refreshProfile,
  }), [loading, session, profile, userId, refreshProfile])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
