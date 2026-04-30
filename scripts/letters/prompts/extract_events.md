You are extracting biographical events from a Philip K. Dick letter.

Letter date: {date}
Recipient: {recipient}
Body:
---
{body}
---

Extract events from this letter that touch any of these nine target themes:

- **drugs** — amphetamines, vitamin regime, hallucinogens, sodium pentothal, drug rehab, Synanon, X-Kalay, Heroin Reform Society, drug-related police interaction, Substance D parallels in life.
- **music** — composer/song mentions tied to a circumstance (listening, attending, buying records, KOIF/KPFA work, Linda Ronstadt, the Fox/Asher generative period for *The Divine Invasion*, Wagner, Beethoven, Dowland, etc.).
- **career** — manuscripts written/sold/rejected, advances, contracts, agent changes (Meredith → Russ Galen), award nominations and wins (Hugo, Campbell), film options including *Blade Runner*, foreign rights, panel appearances, the Metz speech.
- **relationships** — marriages, separations, affairs, the Dark-Haired Girls (Linda Levy, Tessa Busby/Dick, Doris Sauter, Joan Simpson), spouses (Kleo, Anne, Nancy, Tessa), friendships outside SF.
- **politics** — FBI letters, the November 1971 break-in attribution shifts, Vietnam War commentary, Black Panther interactions, conservative late turns, the Lem-as-front "committee" theory, the Ford/Carter/Reagan administrations as referenced.
- **religion** — Bishop Pike conversations, Episcopal church attendance, the 2-3-74 vision's theological aftermath, Pike's son's death, the apostle Thomas correspondence theory, gnostic texts, Nag Hammadi.
- **philosophy** — philosophical reading (Heidegger, Wittgenstein, Hume, Spinoza, Plato, Schopenhauer, Boehme, Eckhart, Tillich, Bonhoeffer, Robert Anton Wilson, Pre-Socratics), the cosmogony/cosmology paper, philosophical correspondence about idealism, materialism, time, identity.
- **visionary** — 2-3-74 and after, the "pink beam," Zebra, the AI Voice, dream visions, anomalous cognition, distinctness from drug states; the Festschrift speech "If You Find This World Bad, You Should See Some of the Others."
- **sf_community** — interactions with other SF authors. Watch carefully for any mention of: Stanislaw Lem, Ursula K. Le Guin, James Tiptree Jr. (Alice Sheldon), Robert Heinlein, Isaac Asimov, K.W. Jeter, Tim Powers, John Varley, Norman Spinrad, Robert Silverberg, Roger Zelazny, Theodore Sturgeon, Harlan Ellison, Brian Aldiss, Thomas Disch, John Brunner, Kate Wilhelm, Terry Carr, Damon Knight, Frederik Pohl, Algis Budrys, Larry Niven, Jerry Pournelle. Also: SFWA business, conventions attended, panels, blurbs, anthology contributions, the alleged Lem-as-front incident.

A single event can be tagged with multiple themes (and frequently will be — "I wrote to Julian Jaynes about *Origin of Consciousness*" is philosophy + visionary + sf_community-adjacent).

**Watch especially for these notable letter-writing events** if the letter contains them:
- A letter to or from **Julian Jaynes** about *The Origin of Consciousness in the Breakdown of the Bicameral Mind*.
- Commentary on **Star Wars** (1977) — PKD's reaction is documented in correspondence.
- The **letter to the FBI** (October 28, 1972) accusing fellow SF authors of being a Soviet front.
- The **Lem affair** (1974–1977) — Lem's expulsion from SFWA, PKD's role in it.
- Letters about the **November 1971 break-in**.
- Letters describing the **2-3-74 events** (Feb–Mar 1974 onward) — first communications of the visions.
- Letters about **Bishop Pike** (death of, séances with, theological correspondence).
- Letters to **Russ Galen** (his agent at Meredith) about contracts, advances, foreign rights.
- Letters to **Tim Powers** and **K.W. Jeter** as protégés.
- The **Metz, France speech** (September 1977) and its aftermath.
- **Blade Runner / Do Androids Dream** correspondence with Hampton Fancher and Ridley Scott.
- The **Festschrift** (1980) and the speech in it.
- Health crises mentioned to friends — the 1972 Vancouver suicide attempt aftermath, the 1974 hospitalization, the February 1982 stroke onset.

Skip routine pleasantries, weather, plot summaries of his fiction (unless the letter explicitly ties the fiction to a real-life event), and editorial annotations.

Return a JSON array. No prose, no markdown, no preamble. If the letter has no qualifying events, return `[]`.

Schema for each event:
```
{
  "summary": "one sentence stating the event in declarative voice",
  "themes": ["drugs"|"music"|"career"|"relationships"|"politics"|"religion"|"philosophy"|"visionary"|"sf_community", ...],
  "date_start": "YYYY-MM-DD" | "YYYY-MM" | "YYYY",
  "date_confidence": "exact" | "month" | "year" | "approximate",
  "event_type": "move|publication|meeting|health|relationship|creative|vision|financial|legal|drug_use|listening|reading|writing|correspondence|speech|reception|other",
  "location": "city, state" or null,
  "people": ["names mentioned"],
  "evidence_quote": "the exact line or short passage from the letter",
  "interpretation_lane": "fact" | "self_report",
  "importance": "high" | "medium" | "low",
  "notable_correspondence": "jaynes|star_wars|fbi_letter|lem_affair|71_break_in|2_3_74|pike|galen|powers|jeter|metz|blade_runner|festschrift|stroke" or null
}
```

Rules:
- `themes` must be a non-empty subset of the nine themes above.
- `date_start` defaults to the letter date unless the letter says the event happened on a different specific date.
- `evidence_quote` must be a real substring from the letter body (max 240 chars).
- `interpretation_lane`: `fact` = checkable event ("I moved to Santa Ana"); `self_report` = his belief/feeling/claim ("I felt the presence of God").
- `importance: high` = events on a known dispute zone OR notable_correspondence is non-null. `medium` = first-time-mentioned facts. `low` = passing mentions.
- `notable_correspondence`: set this if the letter is one of the well-known cited letters in the secondary literature; otherwise leave null. The strings above are slugs.
- Be specific. "He talks about religion" is not an event. "He reports finishing reading Bonhoeffer's *Letters and Papers from Prison* on March 14" is.
- The letter writing itself is an event — if the letter is to Jaynes about *Origin of Consciousness*, emit an event with `event_type: correspondence`, `notable_correspondence: jaynes`, `themes: [philosophy, visionary]`.

Return only the JSON array.
