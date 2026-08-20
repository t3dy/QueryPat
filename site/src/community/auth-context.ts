import { createContext, useContext } from 'react'
import type { Session, User } from '@supabase/supabase-js'
import type { Profile } from '../lib/supabase'

export interface AuthState {
  /** True only when Supabase env vars were present at build time. */
  enabled: boolean
  loading: boolean
  session: Session | null
  user: User | null
  /** Null until the signed-in user has claimed a username. */
  profile: Profile | null
  isModerator: boolean
  signInWithEmail: (email: string) => Promise<void>
  signInWithOAuth: (provider: 'github' | 'google') => Promise<void>
  signOut: () => Promise<void>
  saveProfile: (patch: Partial<Omit<Profile, 'id' | 'role' | 'created_at'>>) => Promise<void>
  refreshProfile: () => Promise<void>
}

export const AuthContext = createContext<AuthState | null>(null)

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
