# Handover: PKD universities, map, and timeline

## What changed

- Added an `Institutional site` geography layer for PKD-relevant universities, archives, and event venues.
- Expanded the California PKD map with:
  - UC Berkeley
  - CSU Fullerton University Archives & Special Collections
  - UC Riverside / Eaton Collection
  - San Francisco State University
  - UBC Faculty Club in the catalog
- Added biography events for:
  - PKD’s 1972 University of British Columbia lecture
  - PKD’s 1973 California State University, Fullerton talk with Willis E. McNelly
- Rebuilt timeline year files so the new university events land in the public timeline.
- Kept the map color-coded by category and retained hover tooltips for each marker.

## Current state

- `npm run build` passes in `C:\QueryPat\site`.
- The timeline export is regenerated and the university events appear in:
  - `C:\QueryPat\site\public\data\timeline\years\1972.json`
  - `C:\QueryPat\site\public\data\timeline\years\1973.json`
- The map source is in:
  - `C:\QueryPat\site\src\data\pkdGeography.ts`
  - `C:\QueryPat\site\src\pages\PKDMap.tsx`

## Important notes

- The workspace has many unrelated pre-existing modifications. Do not revert them.
- The changes relevant to this task are the PKD map / biography / timeline files plus this handover note.
- The repo already has a broad site regeneration footprint; that is expected here.

## Next good expansions

- Add more university-linked PKD appearances from interviews and letters.
- Expand the institutional site layer to non-California universities already in the archive/index data.
- Add dictionary entries for universities and archive institutions if you want them to be first-class browseable terms.

## Next-agent prompt

Continue expanding PKD’s university and institutional geography. Add any university PKD archive holders, conference venues, lecture sites, and university-related biography events that are already supported by the archive, letters, interviews, or scholarship. Keep the map in California-first mode for now, but make sure institutional sites are distinct from ordinary biography markers. Update the timeline whenever a university-related event is added, and keep the map legend and filter controls in sync with the new category.
