# Next steps: turning on community editing

Everything in the codebase is done. What's left is the part only you can do —
creating the Supabase project and the Vercel project, and pasting two keys into
each. Budget about 20 minutes.

Nothing here breaks the existing site. If you never do any of it, the portal
keeps working exactly as it does now: the community layer stays completely
dormant unless the two environment variables below are present at build time.

---

## What was built

| Piece | Where |
|---|---|
| Database schema, security rules, leaderboard | [`supabase/schema.sql`](supabase/schema.sql) |
| Supabase client + all queries | `site/src/lib/supabase.ts` |
| Auth (sign-in, session, profile) | `site/src/community/AuthProvider.tsx` |
| Comment drawer on every page | `site/src/community/CommentsDock.tsx` |
| Comment form with the type dropdown | `site/src/community/ContributionForm.tsx` |
| A single contribution (votes, edit, moderate) | `site/src/community/ContributionCard.tsx` |
| My-account dashboard | `site/src/pages/Account.tsx` → `/#/account` |
| Site-wide activity feed | `site/src/pages/Community.tsx` → `/#/community` |
| Public contributor profiles | `site/src/pages/Profile.tsx` → `/#/u/username` |
| Leaderboard | `site/src/pages/Leaderboard.tsx` → `/#/leaderboard` |
| Moderation queue | `site/src/pages/Moderate.tsx` → `/#/moderate` |
| Vercel build + routing config | [`vercel.json`](vercel.json) |

**How readers use it.** Every page gets a *Discuss this page* button in the
bottom-right corner. Opening it shows that page's thread and a form. The form's
dropdown offers the five types you asked for: **Comment, Correction, Suggested
edit, Suggested tag / metadata, Relevant source.** Corrections and suggested
edits get an extra field for the replacement wording; corrections and sources
get a citation field.

**Card-level precision without touching 40 page components.** Instead of adding
a button to every card, readers *highlight any passage* on the page and a
"Comment on selection" chip appears. The highlighted text is stored with the
contribution and shown as a quote, so you always know exactly which sentence
someone meant. This works on every page — cards, essays, dictionary entries,
Exegesis segments — for free.

**Getting around.** Threads support replies and "helpful" upvotes, and can be
filtered inside the drawer (all / suggestions / comments / unresolved). Every
contribution has a **Copy link** button producing a permalink like
`…/#/dictionary/valis?c=42`; opening one lands on the page with the drawer open
and that note highlighted. Author names lead to public profiles, profiles and the
leaderboard cross-link, and `/#/community` is the site-wide feed of everything
recent, filterable by type and status.

**How scoring works.** The leaderboard ranks by a score built from: accepted work
×5, a live suggestion ×3, a comment or reply ×1, plus one per upvote received.
Declined and duplicate work counts nothing, so volume alone earns nothing — and
you cannot upvote yourself, which the database enforces, not just the browser.
The numbers on someone's account dashboard and public profile come from the same
view the leaderboard ranks by, so they can never disagree.

---

## Step 1 — Create the Supabase project

1. Go to <https://supabase.com>, sign in with GitHub, and click **New project**.
2. Name it something like `querypat`. Pick a region near you. Save the database
   password somewhere safe (you won't need it for this, but you will one day).
3. Wait ~2 minutes for it to provision.

## Step 2 — Create the tables

1. In the Supabase dashboard, open **SQL Editor** → **New query**.
2. Open `supabase/schema.sql` from this repo, copy the whole file, paste it in,
   and click **Run**.
3. You should see "Success. No rows returned." The file is safe to re-run later —
   it drops and recreates the policies, triggers, and leaderboard view without
   touching anyone's contributions, so re-running is how you pick up any future
   change to the rules or the scoring.

This creates three tables (`profiles`, `contributions`, `contribution_votes`),
a `leaderboard` view, and the Row Level Security policies that decide who can do
what. In short: anyone can read; signed-in people can write their own
contributions and edit or delete them; only moderators can accept or decline
anything. Those rules are enforced by the database itself, not by the browser,
so they hold even if someone calls the API directly.

## Step 3 — Set the redirect URLs

Supabase refuses to send people back to a URL it doesn't know about.

1. Dashboard → **Authentication** → **URL Configuration**.
2. **Site URL**: your Vercel domain once you have it (e.g.
   `https://querypat.vercel.app`). For now `http://localhost:5173` is fine.
3. **Redirect URLs**: add all of these, one per line:
   ```
   http://localhost:5173/QueryPat/
   https://your-project.vercel.app/
   https://t3dy.github.io/QueryPat/
   ```
   Come back and fix the middle one once Vercel gives you the real domain.

Email sign-in works out of the box with no extra setup — Supabase emails a
one-time link. (Their built-in mailer is rate-limited to a few messages an hour,
which is fine for early days. If the site gets busy, add a real SMTP provider
under **Authentication → Emails**.)

**Optional — GitHub / Google sign-in.** The sign-in page shows both buttons, but
they only work once you enable the provider under **Authentication → Providers**
and paste in the OAuth app credentials that provider gives you. Skip this
entirely if you like; email links are enough.

## Step 4 — Get your two keys

Dashboard → **Project Settings** → **API**. You need:

- **Project URL** — looks like `https://abcdefgh.supabase.co`
- **anon / public key** — a long string starting `eyJ...`

Both are meant to be public and shipped in the browser bundle; the security
rules from Step 2 are what protect the data. **Do not** use the `service_role`
key anywhere in this project — that one bypasses all the rules.

## Step 5 — Run it locally first

```bash
cp site/.env.example site/.env.local
```

Open `site/.env.local`, paste in your two values, then:

```bash
npm run dev --prefix site
```

Visit <http://localhost:5173/QueryPat/>, click **Sign in** in the nav, request a
link, and check your email. After signing in you'll be asked to pick a username.
Then open any page, hit *Discuss this page*, and leave a test comment.

`.env.local` is git-ignored, so your keys never get committed.

## Step 6 — Make yourself a moderator

You're a regular member until you say otherwise. In the Supabase **SQL Editor**:

```sql
update public.profiles set role = 'admin' where username = 'YOUR_USERNAME';
```

Reload the site and a **Moderate** link appears in the nav. From the moderation
queue (or from any comment inline) you can mark contributions **Accepted**,
**Declined**, or **Duplicate**, with an optional editor's note that the
contributor sees. Accepted work is weighted five times a plain comment on the
leaderboard, so accepting things is what makes the rankings meaningful.

You can promote trusted contributors the same way with `role = 'moderator'`.

## Step 7 — Deploy to Vercel

1. Go to <https://vercel.com>, sign in with GitHub, **Add New → Project**, and
   import `t3dy/QueryPat`.
2. Leave every build setting alone — `vercel.json` in the repo root already tells
   Vercel to install and build inside `site/` and serve `site/dist`.
3. Before clicking Deploy, expand **Environment Variables** and add both, for
   all three environments (Production, Preview, Development):

   | Name | Value |
   |---|---|
   | `VITE_SUPABASE_URL` | your Project URL |
   | `VITE_SUPABASE_ANON_KEY` | your anon key |

4. Deploy. Then go back to Supabase **Authentication → URL Configuration** and
   put the real Vercel domain into Site URL and Redirect URLs.

> These are build-time variables baked into the bundle, so **after changing
> either one you must redeploy** for it to take effect.

### About the existing GitHub Pages deploy

`.github/workflows/deploy.yml` still publishes to GitHub Pages on every push,
and that's untouched. That build has no Supabase keys, so the Pages copy simply
has no community features — a read-only mirror. The Vite config picks the right
base path automatically (`/` on Vercel, `/QueryPat/` on Pages), so both work.

If you'd rather retire Pages once Vercel is live, just delete that workflow file.

---

## Things worth knowing

**Comments are attached to URLs.** A thread belongs to a path like
`/dictionary/valis`. If you ever rename a slug, that page's existing thread won't
follow it. Renames are rare, and this is what keeps the whole feature from
needing an ID on every card in the archive — but it's the tradeoff to know about.

**No email notifications.** Contributors see their own work under *My Account*;
you see everything under *Moderate*. If you later want an email whenever someone
files a correction, that's a Supabase Database Webhook plus a small function —
say the word and it's maybe thirty lines.

**Spam.** Nothing can be posted without a verified email address, which stops the
casual stuff, and declined work scores nothing, so there is no leaderboard payoff
in noise. If it ever becomes a problem, the next step is Supabase's built-in
CAPTCHA on sign-up (Authentication → Settings → Enable CAPTCHA protection) —
a dashboard toggle plus one key, no code change.

**Cost.** Supabase's free tier covers this comfortably: 500 MB of database and
50,000 monthly active users. Vercel's Hobby tier likewise, for a
non-commercial project.

**Deleting an account.** Removing a user in the Supabase dashboard cascades —
their profile, contributions, and votes all go with them.
