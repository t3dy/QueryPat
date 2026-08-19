-- ============================================================
-- QueryPat - community editing schema
-- Run this whole file once in the Supabase SQL Editor.
-- It is idempotent: safe to re-run after edits.
-- ============================================================

-- -- Enums ----------------------------------------------------
do $$ begin
  create type contribution_kind as enum
    ('comment', 'correction', 'suggested_edit', 'suggested_tag', 'source');
exception when duplicate_object then null; end $$;

do $$ begin
  create type contribution_status as enum
    ('open', 'accepted', 'rejected', 'duplicate');
exception when duplicate_object then null; end $$;

-- -- Profiles -------------------------------------------------
create table if not exists public.profiles (
  id           uuid primary key references auth.users on delete cascade,
  username     text unique not null check (username ~ '^[a-z0-9_]{3,24}$'),
  display_name text check (char_length(display_name) <= 60),
  bio          text check (char_length(bio) <= 400),
  role         text not null default 'member'
                 check (role in ('member', 'moderator', 'admin')),
  created_at   timestamptz not null default now()
);

-- -- Contributions (comments / corrections / suggestions) -----
create table if not exists public.contributions (
  id             bigint generated always as identity primary key,
  author_id      uuid not null references public.profiles(id) on delete cascade,
  parent_id      bigint references public.contributions(id) on delete cascade,
  target_path    text not null check (char_length(target_path) <= 300),
  target_label   text check (char_length(target_label) <= 200),
  target_section text check (char_length(target_section) <= 200),
  quote          text check (char_length(quote) <= 1200),
  kind           contribution_kind   not null default 'comment',
  status         contribution_status not null default 'open',
  body           text not null check (char_length(body) between 1 and 5000),
  proposed_value text check (char_length(proposed_value) <= 5000),
  source_url     text check (char_length(source_url) <= 500),
  resolved_by     uuid references public.profiles(id),
  resolved_at     timestamptz,
  resolution_note text check (char_length(resolution_note) <= 1000),
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

create index if not exists contributions_target_idx on public.contributions (target_path, created_at desc);
create index if not exists contributions_author_idx on public.contributions (author_id, created_at desc);
create index if not exists contributions_status_idx on public.contributions (status, created_at desc);
create index if not exists contributions_parent_idx on public.contributions (parent_id);

-- -- Upvotes ("this is helpful") ------------------------------
create table if not exists public.contribution_votes (
  contribution_id bigint not null references public.contributions(id) on delete cascade,
  voter_id        uuid   not null references public.profiles(id) on delete cascade,
  created_at      timestamptz not null default now(),
  primary key (contribution_id, voter_id)
);

-- -- Helpers --------------------------------------------------
create or replace function public.is_moderator()
returns boolean language sql stable security definer set search_path = public as $fn$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('moderator', 'admin')
  );
$fn$;

create or replace function public.touch_updated_at()
returns trigger language plpgsql as $fn$
begin
  new.updated_at = now();
  return new;
end $fn$;

drop trigger if exists contributions_touch on public.contributions;
create trigger contributions_touch before update on public.contributions
  for each row execute function public.touch_updated_at();

-- Only moderators may change status / resolution / authorship fields.
create or replace function public.guard_contribution_status()
returns trigger language plpgsql security definer set search_path = public as $fn$
begin
  if not public.is_moderator() then
    new.status          := old.status;
    new.resolved_by     := old.resolved_by;
    new.resolved_at     := old.resolved_at;
    new.resolution_note := old.resolution_note;
    new.author_id       := old.author_id;
    if old.status <> 'open' then
      new.body           := old.body;
      new.proposed_value := old.proposed_value;
      new.source_url     := old.source_url;
      new.quote          := old.quote;
    end if;
  elsif new.status is distinct from old.status then
    new.resolved_by := auth.uid();
    new.resolved_at := case when new.status = 'open' then null else now() end;
  end if;
  return new;
end $fn$;

drop trigger if exists contributions_guard on public.contributions;
create trigger contributions_guard before update on public.contributions
  for each row execute function public.guard_contribution_status();

-- -- Row Level Security ---------------------------------------
alter table public.profiles           enable row level security;
alter table public.contributions      enable row level security;
alter table public.contribution_votes enable row level security;

drop policy if exists profiles_read        on public.profiles;
drop policy if exists profiles_insert_self on public.profiles;
drop policy if exists profiles_update_self on public.profiles;
create policy profiles_read        on public.profiles for select using (true);
create policy profiles_insert_self on public.profiles for insert with check (id = auth.uid());
create policy profiles_update_self on public.profiles for update
  using (id = auth.uid() or public.is_moderator())
  with check (id = auth.uid() or public.is_moderator());

drop policy if exists contributions_read   on public.contributions;
drop policy if exists contributions_insert on public.contributions;
drop policy if exists contributions_update on public.contributions;
drop policy if exists contributions_delete on public.contributions;
create policy contributions_read   on public.contributions for select using (true);
create policy contributions_insert on public.contributions for insert
  with check (author_id = auth.uid());
create policy contributions_update on public.contributions for update
  using (author_id = auth.uid() or public.is_moderator());
create policy contributions_delete on public.contributions for delete
  using (author_id = auth.uid() or public.is_moderator());

drop policy if exists votes_read   on public.contribution_votes;
drop policy if exists votes_insert on public.contribution_votes;
drop policy if exists votes_delete on public.contribution_votes;
create policy votes_read   on public.contribution_votes for select using (true);
create policy votes_insert on public.contribution_votes for insert
  with check (
    voter_id = auth.uid()
    and not exists (
      select 1 from public.contributions c
      where c.id = contribution_id and c.author_id = auth.uid()
    )
  );
create policy votes_delete on public.contribution_votes for delete using (voter_id = auth.uid());

-- -- Leaderboard ----------------------------------------------
-- Scoring, in words: accepted work counts five times; an open suggestion
-- counts three (two for being a suggestion, one for existing); an open comment
-- or reply counts one; declined and duplicate work counts nothing, so there is
-- no reward for volume alone. Upvotes from *other* readers add one each.
drop view if exists public.leaderboard;
create view public.leaderboard
with (security_invoker = on) as
with counted as (
  select
    c.*,
    (c.status not in ('rejected', 'duplicate')) as counts_for_score
  from public.contributions c
)
select
  p.id                                                 as user_id,
  p.username,
  p.display_name,
  p.role,
  count(c.id)                                          as total,
  count(c.id) filter (where c.status = 'accepted')     as accepted,
  count(c.id) filter (where c.status = 'open')         as open_count,
  count(c.id) filter (where c.kind <> 'comment')       as edits,
  count(c.id) filter (where c.kind = 'correction')     as corrections,
  count(c.id) filter (where c.kind = 'suggested_edit') as suggested_edits,
  count(c.id) filter (where c.kind = 'suggested_tag')  as tags,
  count(c.id) filter (where c.kind = 'source')         as sources,
  count(c.id) filter (where c.parent_id is not null)   as replies,
  count(distinct c.target_path)                        as pages,
  coalesce(sum(v.votes), 0)                            as upvotes,
  (count(c.id) filter (where c.status = 'accepted') * 5)
    + (count(c.id) filter (where c.counts_for_score and c.kind <> 'comment') * 2)
    + count(c.id) filter (where c.counts_for_score)
    + coalesce(sum(v.votes), 0)                        as score,
  min(c.created_at)                                    as first_contribution_at,
  max(c.created_at)                                    as last_contribution_at
from public.profiles p
left join counted c on c.author_id = p.id
left join lateral (
  select count(*)::int as votes
  from public.contribution_votes cv
  where cv.contribution_id = c.id
) v on true
group by p.id, p.username, p.display_name, p.role;

grant select on public.leaderboard to anon, authenticated;
