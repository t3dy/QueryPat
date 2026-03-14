# Under the Hood: How Tool Calls Work in QueryPat Development

## What This Document Covers

When Claude Code works on QueryPat — building features, auditing data, improving entries — it orchestrates dozens of tool calls behind each visible action. This document explains what those calls are, why they happen in the order they do, and how the system scales to handle a project with 1,100+ segments, 310 dictionary terms, 410 names, and 228 archive documents.

---

## The Tools

Claude Code has access to several categories of tools:

**File operations** — `Read`, `Write`, `Edit`, `Glob`, `Grep`. These are the workhorses. Read fetches file contents. Edit performs surgical string replacements (find old text, replace with new text). Glob finds files by pattern. Grep searches file contents by regex. Write creates or overwrites files.

**Shell execution** — `Bash`. Runs commands: `npm run build`, `git status`, `python scripts/build_all.py`. Used for compilation, version control, and running data pipelines.

**Subagents** — `Agent`. Launches independent Claude instances that can search, read, and analyze code in parallel. Each agent gets its own context window and returns a single result. Critical for parallelizing work that would otherwise be sequential.

**Preview server** — `preview_start`, `preview_screenshot`, `preview_snapshot`, `preview_console_logs`, `preview_inspect`. Runs the Vite dev server and verifies changes visually and structurally without asking the user to check manually.

**Task management** — `TodoWrite`. Tracks multi-step work so the user can see progress in real time.

---

## Pattern 1: Building a New Component

When Claude Code builds something like `HoverPreview.tsx`, the sequence looks like this:

```
1. Read existing components to understand patterns
   → Read Layout.tsx, TermDetail.tsx, App.css
   → Learn: HashRouter, useData hook, CSS custom properties, import type syntax

2. Read the data files the component will consume
   → Read a sample term JSON, segment JSON, name JSON
   → Learn: field names, data shapes, what to extract for previews

3. Write the new component
   → Write site/src/components/HoverPreview.tsx

4. Edit consuming files to integrate it
   → Edit TermDetail.tsx: add import, wrap Link elements with HoverPreview
   → Edit SegmentDetail.tsx: same treatment
   → Edit NameDetail.tsx: same treatment

5. Edit CSS
   → Edit App.css: add hover preview styles, positioning, animation, responsive rules

6. Build to check for type errors
   → Bash: npm run build
   → If errors: Read the component again, Edit to fix, rebuild

7. Preview to verify visually
   → preview_start (or reuse running server)
   → preview_snapshot: check that hover elements render in the accessibility tree
   → preview_console_logs: check for runtime errors
   → preview_screenshot: capture visual proof
```

Steps 1-2 happen in parallel (multiple Reads at once). Steps 4's edits to three different files also happen in parallel. The build-fix cycle in step 6 may repeat 2-3 times if TypeScript catches issues like the `verbatimModuleSyntax` constraint requiring `import type`.

**Key insight:** Reading before writing is not optional. Claude Code reads the existing codebase to match its conventions — import style, CSS variable names, component patterns, data shapes. Writing without reading produces code that compiles but feels foreign to the project.

---

## Pattern 2: Auditing Data at Scale

When the user asks "audit all entries and tell me which need improvement," Claude Code cannot read 1,100+ files sequentially. Instead:

```
1. Launch parallel Explore agents
   → Agent 1: audit dictionary terms (Glob *.json in terms/, Read index, sample entries)
   → Agent 2: audit biography events (Read events.json, check each entry against style guide)
   → Agent 3: audit names + archive (Glob entities/, Read index, sample entries)

2. Each agent works independently
   Agent 1 does:
     → Glob site/public/data/dictionary/terms/*.json (finds 310 files)
     → Read index.json to get the full term list with mention counts
     → Read 10-15 sample term files to understand data quality patterns
     → Grep for common words that shouldn't be dictionary terms
     → Compile findings: 47 zero-mention orphans, 51 common-word entries

   Agent 2 does:
     → Read site/public/data/biography/events.json (119 entries, single file)
     → Check each entry against pkdbiostyle rules:
       - Is event text 8-16 words?
       - Is date format correct?
       - Does category use controlled vocabulary?
       - Are entities extracted?
     → Compile findings: 46 date range format issues, 4 missing locations

   Agent 3 does:
     → Read site/public/data/names/index.json
     → Glob entities/*.json, Read samples
     → Read site/public/data/archive/index.json
     → Compile findings: all 410 names missing linked_segments, 79 archive docs need summaries

3. Collect results from all three agents
   → Synthesize into a single audit report for the user
```

**Why agents instead of direct reads?** Context window management. Reading 310 dictionary term files would consume the entire conversation context. Each agent gets its own context, does its analysis, and returns a compact summary. The main conversation stays lean.

**Why three agents instead of four?** Names and archive are smaller datasets that fit comfortably in one agent's context. Dictionary and biography each need dedicated attention — dictionary because of the file-per-term structure, biography because of the detailed style guide checks.

---

## Pattern 3: Improving Entry Writing

When Claude Code improves the writing of data entries (like biography events or dictionary descriptions), each entry goes through:

```
1. Read the current entry
   → Parse JSON, extract the text field to improve

2. Evaluate against quality criteria
   For biography: pkdbiostyle rules (8-16 words, active voice, one clause, neutral tone)
   For dictionary: completeness of description, accuracy of category, mention count validity
   For archive: summary quality, metadata completeness

3. Generate improved text
   → Apply style rules
   → Preserve factual content
   → Fix structural issues (date formats, missing fields)

4. Edit the JSON file
   → Edit with exact string match of old value → new value
   → JSON must remain valid (quotes, commas, brackets all correct)

5. Rebuild dependent files
   → Bash: python scripts/build_all.py (regenerates search index, analytics)
   → Or: python scripts/export_json.py (exports from SQLite to JSON)
```

**The Edit tool's constraint:** It requires an exact match of the old string. This means Claude Code must have read the file recently enough to know the exact current content. If the file was modified by another process (like a build script), the edit fails and Claude Code must re-read before retrying.

**Batch operations:** When improving 119 biography entries, Claude Code doesn't make 119 separate Edit calls. It reads the entire events.json, constructs a new version with all improvements applied, and writes it once. This is faster and avoids the risk of partial updates corrupting JSON structure.

For file-per-entity structures (like dictionary terms), the approach differs: multiple Edit calls can run in parallel since they target different files. Claude Code groups these into batches of 5-10 parallel edits to balance speed against the risk of overwhelming the system.

---

## Pattern 4: The Build-Verify Loop

Every significant change triggers verification:

```
1. Edit source files (one or more)

2. Build
   → Bash: cd /c/QueryPat/site && npm run build
   → TypeScript compiler catches type errors, missing imports, syntax issues
   → If build fails: read error output, edit to fix, rebuild

3. Preview (if UI changed)
   → preview_start or confirm server is running
   → preview_eval: window.location.reload() (if not using HMR)
   → preview_snapshot: check accessibility tree for expected elements
   → preview_console_logs: check for runtime errors
   → preview_inspect: verify specific CSS properties if styling changed
   → preview_screenshot: capture visual proof for the user

4. Report to user
   → Share screenshot or snapshot results
   → Note any issues found and fixed
```

**Why snapshot before screenshot?** The accessibility tree (snapshot) is a text representation that Claude Code can parse programmatically — it can verify that specific elements exist, text content is correct, and links point to the right routes. Screenshots are for the user's benefit and for catching visual issues that don't show up in the tree (like overlapping elements or broken layouts).

---

## Pattern 5: Cross-File Refactoring

When a change touches multiple files (like adding tag links across all detail pages), Claude Code:

```
1. Read all affected files in parallel
   → Read TermDetail.tsx, SegmentDetail.tsx, NameDetail.tsx, ArchiveDetail.tsx

2. Plan the consistent change
   → Identify the pattern: tags should link to /tag/{encoded_tag_name}
   → Find each file's tag-related code

3. Edit all files in parallel
   → Edit TermDetail.tsx: wrap category tags in Link to /tag/
   → Edit SegmentDetail.tsx: wrap concept tags in Link to /tag/
   → Edit NameDetail.tsx: wrap allusion types in Link to /tag/
   → Edit ArchiveDetail.tsx: wrap category in Link to /tag/

4. Build once to verify all changes
```

Parallel edits to independent files are safe because there are no merge conflicts — each file is edited in isolation. This is significantly faster than sequential editing.

---

## Error Recovery

When things go wrong, the recovery pattern is:

**Type error after edit:**
```
Edit file → Build fails → Read error message → Read file again → Edit to fix → Rebuild
```
Common cause: `verbatimModuleSyntax` requiring `import type` for type-only imports. The fix is mechanical — change `import { X }` to `import type { X }` — but requires reading the build error to identify which import.

**Runtime error after build succeeds:**
```
Build succeeds → Preview shows error in console → Read console logs → Read source file → Edit to fix → Reload preview → Verify
```
Common cause: data shape mismatch (component expects `string[]`, data provides `string | null`). The fix is adding null checks or default values.

**Stale dev server state:**
```
Fix applied but error persists → preview_stop → preview_start → Verify
```
Vite's HMR occasionally caches stale module state. Restarting the dev server clears it. This happened during the Bookmark type import fix in this project.

---

## Performance Characteristics

| Operation | Typical Duration | Parallelizable |
|-----------|-----------------|----------------|
| Read a single file | <1s | Yes (up to ~10 concurrent) |
| Edit a single file | <1s | Yes (different files only) |
| Write a new file | <1s | Yes |
| Glob pattern search | <1s | Yes |
| Grep content search | 1-3s | Yes |
| npm run build | 5-15s | No (single process) |
| Launch subagent | 10-60s | Yes (up to 3-4 concurrent) |
| Preview screenshot | 2-5s | No |
| Full data audit (3 agents) | 30-90s | Agents run in parallel |

The biggest time savings come from parallelizing reads and agent launches. A naive sequential audit of all entity types would take 3-4 minutes; parallel agents complete it in under 90 seconds.

---

## What the User Sees vs. What Happens

When the user says "add hover previews to all detail pages," they see:

```
User sees:
  → "Adding HoverPreview component and integrating it across detail pages."
  → [progress indicator]
  → "Build passed. Verifying in preview..."
  → [screenshot]
  → "All detail pages now show hover previews on internal links."
```

What actually happens:

```
Behind the scenes:
  → Read 4 detail page files (parallel)
  → Read 2 sample data files (parallel)
  → Write HoverPreview.tsx
  → Edit 4 detail pages to integrate HoverPreview (parallel)
  → Edit App.css to add styles
  → Bash: npm run build (catches import type error)
  → Read HoverPreview.tsx again
  → Edit to fix import type
  → Bash: npm run build (succeeds)
  → preview_start
  → preview_snapshot (verify elements exist)
  → preview_console_logs (verify no errors)
  → preview_screenshot (capture proof)
  → Total: ~20 tool calls, ~45 seconds
```

The gap between what the user sees (4 messages) and what happens (20 tool calls) is the automation dividend. Each tool call is a decision — what to read, what to edit, what to verify — compressed into a workflow that would take a developer 15-30 minutes of manual work.
