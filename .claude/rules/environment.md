# Rule: working environment

## One checkout, shared

Work in `C:\QueryPat` on `main`. Do not create git worktrees or feature
branches: the owner works in several windows on the same checkout and wants the
work in one place.

Because other windows share it:

- `git status` first. Changes you did not make belong to another window: do
  not revert, stage, commit or "clean up" them.
- Stage only your own files by path (`git add <paths>`); never `git add -A` or
  `git commit -a`.
- Never use `git stash`, `git reset --hard` or `git checkout -- <path>` on files
  you did not change.
- `database/unified.sqlite` is git-ignored and shared too; a seeder run writes
  it for everyone, which is fine — seeders are idempotent.

## Preview

The preview entries are in `C:\QueryPat\.claude\launch.json`. The site lives
under `/QueryPat/` and uses a **HashRouter**: links are `#/studies/...`; never a
bare `href="#anchor"` (scroll in JS; read the anchor from `useLocation().hash`).

## Deploy

A push to `main` deploys: `.github/workflows/deploy.yml` builds `site/` and
publishes to GitHub Pages (`https://t3dy.github.io/QueryPat/`), in about a
minute (`gh run list --workflow deploy.yml`). Push only when the owner asks.

## Pre-commit guard

`python scripts/safeguard/check_data_diff.py --install-hook` once. It refuses
commits that delete curated content; an entry edited in place (a corrected
locator, a reworded field) passes. See `generated-files.md`.

## Python and encoding

Windows console output is cp1252: run scripts that print corpus text with
`PYTHONIOENCODING=utf-8`. Write JSON with `encoding='utf-8'` and
`ensure_ascii=False`.
