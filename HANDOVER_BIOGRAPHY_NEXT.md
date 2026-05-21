# Handover: PKD Biography Experience Taxonomy

## Current State

We expanded the biography experience taxonomy so the site can surface PKD's religious, mystical, gnostic, paranormal, and voice-hearing material as distinct filters.

### Files updated in this pass

- `site/src/pages/Biography.tsx`
- `site/src/pages/People.tsx`
- `site/src/pages/PeopleDetail.tsx`
- `site/public/data/biography/curated.json`
- `scripts/biography/add_pkd_expansion_events.py`

### What changed

- Added biography category labels for:
  - `paranormal_experience`
  - `mystical_experience`
  - `gnostic_experience`
  - `hearing_voices_experience`
- Reclassified several curated biography events around:
  - Arnold's 2-3-74 reconstruction
  - Zebra / Black Iron Prison / Exegesis theology
  - Jaynes / bicameral voice theory
  - Later mystical and gnostic reading and lecture material
- Updated the people pages so these categories render with human-readable labels instead of raw ids.

## Key counts

Current curated biography category counts now include:

- `gnostic_experience`
- `mystical_experience`
- `hearing_voices_experience`
- `paranormal_experience`

The biography page now has visibly denser coverage of PKD's late visionary period.

## Validation

- `npm run build` passed in `C:\QueryPat\site`

## Remaining ideas

1. Add a dedicated biography sidebar section that groups these categories into:
   - Religion / gnosis
   - Voices
   - Paranormal / visionary
2. Mine more explicit voice and revelation events from Exegesis and unpublished letters.
3. Add cross-links from these biography entries into the `Themes` and `Works` pages where relevant.

## Prompt for a new window

Continue the PKD biography work by deepening the curated experience taxonomy. Focus on adding and refining biography events for religious experience, mystical experience, gnostic experience, paranormal experience, and hearing-voices experience. Prefer evidence from Kyle Arnold, Lawrence Sutin, Selected Letters, and the Exegesis. Keep the taxonomy consistent across `site/public/data/biography/curated.json`, `scripts/biography/add_pkd_expansion_events.py`, and the React pages that render biography and people metadata. After editing, run the site build and report which new or reclassified events were added.
