#!/usr/bin/env python3
"""
The authored dossier "Drugs in Philip K. Dick": essay, browse facets, card
groups, contradictions, open questions and structured fields.

Kept as Python so the prose stays readable and diffable. build_dossier.py
writes it to dossier.json, which is what the seeder reads.

Citations in {{double braces}} are finding ids from findings.py. The seeder
refuses to build if one does not resolve, and checks every quotation of 40+
characters against the sources the dossier cites.

Registers: A = PKD's own words, B = primary-source fact, C = scholarly
argument, D = portal-editor inference.
"""

import re

TITLE = 'Drugs in Philip K. Dick'

SUBTITLE = ("Twenty years of prescribed and street amphetamine, two or three LSD trips, "
            "one dose of mescaline, a month among heroin addicts — and the novels, "
            "letters and notebooks in which Dick argued about all of it, often with "
            "himself.")

CARD_DESCRIPTION = (
    "Amphetamines, LSD, mescaline, sodium pentothal and vitamins; Substance D, "
    "Can-D, Chew-Z and JJ-180; X-Kalay; and the biographers who disagree about how "
    "much, when and why — 105 sourced passages across the letters, interviews, "
    "Exegesis, novels and biographies.")

SECTIONS = [

 {"id": "note", "heading": "Drugs in Philip K. Dick", "register": "D", "body": [
  "Few subjects attract more legend in Philip K. Dick's life than drugs, and few "
  "are better documented by Dick himself. He wrote about his pills to friends "
  "while he was taking them {{DRG-LET-1964-BROCHURE}}, explained them to "
  "interviewers once he had stopped {{DRG-INT-1979-AMPH}}, built three novels "
  "around invented drugs, and in the Exegesis made intoxication a model of the "
  "human condition {{DRG-EX-1978-OCCLUSION}}. He also contradicted himself, and his "
  "biographers contradict one another.",

  "This page keeps those voices apart. It separates what Dick said about his own "
  "use (letters and interviews, lane E), what he theorised about it afterwards "
  "(the Exegesis, lane B), what his characters say (fiction, lane A), and what "
  "the biographers and critics conclude (lanes D and C). Where the sources "
  "disagree, the disagreement is recorded below as a contradiction, not settled.",

  "The essay runs roughly in order, from the first Semoxydrine around 1952 to the "
  "last interview in 1982. The index underneath runs the other way: pick a "
  "substance, a novel, a theme or a biographer and see every passage that turns "
  "on it. Every bracketed reference opens the card it cites. Two caveats about the "
  "archive itself: the texts of The Three Stigmata of Palmer Eldritch and Flow My "
  "Tears, the Policeman Said are not in it, so those novels appear only through "
  "Dick's comments and criticism; and Anthony Peake's biography is catalogued but "
  "its text is not, so his position is not represented."]},

 {"id": "amphetamines", "heading": "Twenty years of speed", "register": "A", "body": [
  "Dick's own account begins with a cure. Writing to Anthony Boucher in 1962 "
  "about the agoraphobia that had closed in on him since adolescence, he says "
  "that at twenty-four — around 1952–53 — he found a stimulant he spells "
  "semoxydrene, and that the first 5 mg cleared away the cobwebs from his brain "
  "{{DRG-LET-1962-SEMOX}}. The same letter has the \"little green pills\" first "
  "rescue him and then deliver him to a disastrous move. Kyle Arnold pushes the "
  "story back further, to an asthma medicine taken at six {{DRG-BIO-ARNOLD-EPHEDRINE}}.",

  "By 1964 the cure was a supply. In September he complains that his amphetamines "
  "have dried up despite two open prescriptions {{DRG-LET-1964-SUPPLY}}; in October "
  "a forgotten brochure tells him that semoxydrine hydrochloride is "
  "methamphetamine, and that he is on the strongest dose, six a day "
  "{{DRG-LET-1964-BROCHURE}}. By November 1970, in the house in Santa Venetia, he "
  "boasts of having taken a thousand methamphetamine tablets in two weeks "
  "{{DRG-LET-1970-THOUSAND}}.",

  "He gave two reasons, sometimes in the same breath. To a student in 1976: the "
  "amphetamines were prescribed for depression, used for about eighteen years, "
  "and taken for energy because he was paid so little per book "
  "{{DRG-LET-1976-BOGGS}}. To Charles Platt in 1979, only the second reason: "
  "sixteen novels in five years, sixty pages a day, and amphetamines the only way "
  "to do it {{DRG-INT-1979-AMPH}}.",

  "In the Exegesis the speed becomes part of the metaphysics. Around 1979 Dick "
  "reverses the usual story of 1974: he did not go mad then but sobered up, "
  "having gone mad in the 1950s or 1960s, \"perhaps due to the speed\" "
  "{{DRG-EX-1979-SPEEDSELF}}. Elsewhere decades of amphetamines have speeded up "
  "his internal clock until only timeless forms were visible "
  "{{DRG-EX-1978-FASTER}}, and a list of what drove him mad puts drugs second of "
  "three, between Nancy leaving and \"endogenous psychosis\" "
  "{{DRG-EX-1978-DRIVENMAD}}."]},

 {"id": "psychedelics", "heading": "Two trips, or three: LSD and mescaline",
  "register": "A", "body": [
  "Against his reputation, Dick's psychedelic record is short. He told Platt he "
  "took LSD twice, the second dose perhaps not acid at all; the first, Sandoz acid "
  "split with a friend, sent him \"straight to hell\" — a frozen landscape, God "
  "judging him, Latin — and \"That was in 1964\" {{DRG-INT-1979-TWICE}}. He had "
  "already dated it to 1964 in a letter of 1975, calling it a \"head trip\" "
  "unlike the events of 1974 {{DRG-LET-1975-HEADTRIP}}. The frozen landscape "
  "recurs in his letters {{DRG-LET-1977-ICE}}, the Latin and the Roman setting in "
  "a fanzine piece of 1967 that compares LSD with a psychotic episode and with "
  "the Bardo Thodol {{DRG-LET-1967-PSYCHOSIS}}.",

  "The witnesses do not agree on the count. Sutin has \"at least two occasions\" "
  "in 1964, one with Ray Nelson {{DRG-BIO-SUTIN-ACID}}; Anne R. Dick tells the "
  "Nelson trip as the only one {{DRG-BIO-ANNE-ONCE}}; Gregg Rickman says two or "
  "three times and not until about 1967 {{DRG-SCH-RICKMAN-FACTS}}. Dick himself "
  "helped the legend along — he quoted Oui's claim that he had experimented with "
  "LSD since the early fifties to his publisher as a selling point "
  "{{DRG-LET-1976-OUI}}, and confessed to Vertex that he had written his own "
  "blurbs about hallucinogens {{DRG-INT-1974-ACID}}.",

  "Did LSD affect the work? In 1973 his answer was \"none at all\" "
  "{{DRG-LET-1973-VERTEX}}; in 1976 he allowed one exception, a passage of A Maze "
  "of Death drawn from his first trip {{DRG-LET-1976-MAZE}}. By 1978 the verdict "
  "is moral: \"There's nothing good about drugs\" {{DRG-INT-1978-AQUARIAN}}.",

  "Mescaline is the one drug Dick credited with something good. One large dose in "
  "May 1970 gave him what acid never had, an overpowering love for other people, "
  "and he put it into Flow My Tears, the Policeman Said {{DRG-LET-1970-MESCALIN}}. "
  "In the Exegesis the same dose marks the moment a \"fugal\" personality took "
  "over {{DRG-EX-1978-DRIVENMAD}}."]},

 {"id": "eldritch", "heading": "Palmer Eldritch: the LSD novel written without LSD",
  "register": "A", "body": [
  "The Three Stigmata of Palmer Eldritch, written in 1964, was read as Dick's acid "
  "novel from the start. Its drugs are Can-D, which lets Martian colonists inhabit "
  "the doll-world of Perky Pat, and Chew-Z, which delivers them instead into "
  "Eldritch's world {{DRG-SCH-BUTLER-ELDRITCH}}; Fredric Jameson reads it as one of "
  "Dick's reversals, in which the hallucination, not reality, is degraded "
  "{{DRG-SCH-JAMESON-CHEWZ}}.",

  "Dick's account of its origin is consistent on one point: the novel came first. "
  "The face with slotted eyes was a vision of 1963, seen \"before I had seen any "
  "LSD, much less taken any\", which his first LSD trip then confirmed "
  "{{DRG-LET-1969-ELDRITCH}}. In 1974 he told Vertex he had written the book from "
  "reading about LSD's discovery {{DRG-INT-1974-BEFORE}}, and an English journalist "
  "that he was on no drug at the time of the vision {{DRG-INT-1974-CONTROL}}. In "
  "1979 the reading was \"an article by Aldous Huxley\" {{DRG-INT-1979-HUXLEY}}; "
  "Anne R. Dick, who lived with him while he wrote it, says it was reading about "
  "hallucinogenic mushrooms {{DRG-BIO-ANNE-MUSHROOMS}}.",

  "Other evidence pulls the other way. In 1967 Dick called the novel \"a 'trip' "
  "book\" and set its vision beside a second encounter \"under LSD\" "
  "{{DRG-LET-1967-TRIPBOOK}}. Sutin notes that at the time Dick described the 1963 "
  "vision as following \"certain chemicals\" and \"psychedelic drugs\" — not LSD, "
  "but perhaps amphetamines {{DRG-BIO-SUTIN-1963}}. And Harlan Ellison recalls "
  "that Dick assured him both Palmer Eldritch and \"Faith of Our Fathers\" were "
  "LSD-inspired; Sutin believes Dick's later denial {{DRG-BIO-SUTIN-ELLISON}}.",

  "By 1976 Dick had a third reading of his own: the novel is not about drugs at "
  "all, but about transubstantiation, and Chew-Z is a eucharist "
  "{{DRG-EX-1976-TRANSUB}}."]},

 {"id": "marin", "heading": "Santa Venetia, 1970–1972", "register": "D", "body": [
  "The worst years are the best attested, because so many people were in the "
  "house. In the late sixties, Sutin writes, acid, pot and hash held no special "
  "fascination for Dick, but pills did, from a rotating set of doctors "
  "{{DRG-BIO-SUTIN-PILLS}}; Nancy Hackett told Anne R. Dick it came to seventy a "
  "day {{DRG-BIO-ANNE-SEVENTY}}. After Nancy left in September 1970 the Santa "
  "Venetia house filled with young users, and the pills became jars of a thousand "
  "street white crosses {{DRG-BIO-SUTIN-PARANOIA}}. Cindy, one of the teenagers, "
  "remembered a thousand \"beans\" a week — and that Phil would not touch pot "
  "{{DRG-BIO-ANNE-POT}}.",

  "In the spring of 1971 Dick told a psychiatrist at Stanford the same figure, a "
  "thousand Methedrine tablets a week {{DRG-BIO-SUTIN-STANFORD}}; later that year "
  "his own psychiatrist, seeing no withdrawal, thought him a hypochondriac "
  "{{DRG-BIO-ANNE-DRA}}. Sutin, describing the paranoia of those months, refuses "
  "to choose between the real dangers of the house and the known effects of the "
  "drug {{DRG-BIO-SUTIN-PARANOIA}}.",

  "Dick's fiction of the period's end is VALIS, which opens in 1971 with a friend "
  "phoning Horselover Fat for Nembutals to kill herself; Fat does uppers, not "
  "sleeping pills {{DRG-FIC-VALIS-UPPERS}}. The narrator's verdict on the Bay Area "
  "of the sixties is that it was like a plague, and no one could tell how much was "
  "drugs {{DRG-FIC-VALIS-PLAGUE}}. In a letter of 1981 Dick remembers a junky from "
  "those years as the most humane person he had known {{DRG-LET-1981-JUNKY}}."]},

 {"id": "xkalay", "heading": "Vancouver and X-Kalay", "register": "A", "body": [
  "In February 1972 Dick went to Vancouver as a convention guest of honour and "
  "stayed. After a suicide attempt in March, a crisis line sent him to X-Kalay, a "
  "residential community run on Synanon lines for heroin addicts out of Canadian "
  "prisons. From inside it he wrote, \"I owe my life to them\" "
  "{{DRG-LET-1972-XKALAY}}. What he saw there — addicts who looked twice their age, "
  "a girl addicted at fourteen — made him an enemy of drugs and dealers "
  "{{DRG-LET-1972-HEROIN}}. That summer he named marijuana, hashish and LSD as "
  "causes of his wife's breakdowns, and so of his own collapse; his amphetamines "
  "are not on the list {{DRG-LET-1972-LINDA}}. On Los Angeles radio he refused to "
  "concede that good acid was fine {{DRG-LET-1973-RADIO}}.",

  "He told Gillespie he spent a month there {{DRG-LET-1972-HEROIN}}; Sutin says "
  "three weeks, and that Dick, who had told Vertex he posed as a heroin addict to "
  "get in, never touched heroin {{DRG-BIO-SUTIN-THREEWEEKS}}. Sutin credits X-Kalay "
  "with ending his regular use of speed after nearly twenty years "
  "{{DRG-BIO-SUTIN-NEVERAGAIN}}.",

  "Dick's own verdict changed. In 1975 he decided its education had been faulty — "
  "it had taught him that the individual alone is doomed {{DRG-LET-1975-FAULTY}}. "
  "In the Exegesis the Synanon game he had played there becomes \"the exact "
  "analog of CP brainwashing\" {{DRG-EX-1977-SYNANON}}, and in A Scanner Darkly the "
  "rehabilitation centre grows the drug {{DRG-FIC-SCANNER-FIELD}}."]},

 {"id": "scanner", "heading": "A Scanner Darkly", "register": "A", "body": [
  "A Scanner Darkly was finished in the spring of 1973, the week his ex-wife wrote "
  "that street drugs had caused her breakdowns {{DRG-LET-1973-NANCY}}, and "
  "published in 1977. Its drug is Substance D — dumbness, despair, desertion, "
  "and finally \"Slow Death\", as the undercover agent Fred says in a speech that "
  "gives him away {{DRG-FIC-SCANNER-SLOWDEATH}}. It opens with Jerry Fabin washing "
  "invisible aphids out of his hair {{DRG-FIC-SCANNER-BUGS}}; it gives the split "
  "between Fred and the man he watches, Bob Arctor, a neurology — competing "
  "hemispheres {{DRG-FIC-SCANNER-HEMISPHERES}}; and it ends in a field of blue "
  "flowers grown by the rehabilitation centre itself {{DRG-FIC-SCANNER-FIELD}}.",

  "Dick never quite decided whether the book was research or memoir. Joking to a "
  "radio friend in 1973, he presented his years in the subculture as research — "
  "\"I even had to (ugh) partake of dope\" {{DRG-LET-1973-RESEARCH}}. The Author's "
  "Note says the opposite, in his most quoted lines on the subject: drug misuse "
  "is \"not a disease, it is a decision\" {{DRG-NOTE-SCANNER-DECISION}}, and he is "
  "on the list of the dead and damaged, \"not a character in this novel; I am the "
  "novel\" {{DRG-NOTE-SCANNER-NOVEL}}. To others he called it a roll call of his "
  "friends {{DRG-LET-1975-ROLLCALL}}, every character a real doper "
  "{{DRG-LET-1977-DOPERS}}, written to record them and to attack drugs "
  "{{DRG-INT-1981-RECORD}}.",

  "In the Exegesis the novel keeps changing subject. Readers assume the government "
  "makes Substance D, and Dick and K. W. Jeter agree this can be inferred "
  "{{DRG-EX-1977-SLAVE}}; the Author's Note's \"punished entirely too much\" comes "
  "to mean the work camp, not the drug {{DRG-EX-1977-NOTE}}; the book is about "
  "the punishment for playing instead of toiling, \"not drugs\" "
  "{{DRG-EX-1978-PLAYING}}. Yet by 1978–80 nothing in his work outweighs its study "
  "of brain damage {{DRG-EX-1978-IMPAIRMENT}}, and Jeter's line — that the dopers "
  "on Substance D alone understood the reality situation — becomes a key "
  "{{DRG-EX-1978-JETER}}."]},

 {"id": "fiction", "heading": "JJ-180, Can-D and the others", "register": "A", "body": [
  "Dick's invented drugs share a structure. JJ-180, in Now Wait for Last Year "
  "(1966), addicts after a single dose and is supplied by an ally in a war to the "
  "people it is used to control: \"that's why we put you on it\" "
  "{{DRG-FIC-NOWWAIT-ADDICT}}. The party where it is passed round includes a "
  "wealthy author on mysticism for whom every new hallucinogen is \"allied with "
  "religion\" {{DRG-FIC-NOWWAIT-HASTINGS}}. Can-D and Chew-Z are sold by "
  "competitors; Substance D is grown by the rehabilitation centre. In each, a "
  "chemical gives someone else control of what the user takes to be real.",

  "Dick noticed the pattern himself. Around 1978 he lays Palmer Eldritch, A Maze "
  "of Death and A Scanner Darkly side by side as one diagnosis: a perception "
  "\"deliberately induced by a drug or drug-like substance\" that cannot test "
  "reality {{DRG-EX-1978-OCCLUSION}}. The VALIS he planned in 1977 had a character "
  "named Phil take STP to see the god, and fear that anything he saw would be put "
  "down to the drug {{DRG-LET-1977-STP}}; the VALIS he published begins instead "
  "with a death from LSD {{DRG-LET-1979-VALIS}}."]},

 {"id": "seventyfour", "heading": "1974: pentothal, vitamins, lithium",
  "register": "A", "body": [
  "The experiences of February and March 1974 had chemical neighbours, and Dick "
  "listed them himself. In February he was given sodium pentothal for a wisdom-"
  "tooth extraction. In the following weeks he took the \"orthomolecular\" "
  "water-soluble vitamins, on purpose: he had read Robert Ornstein on the right "
  "hemisphere, had just written a novel about drug-damaged brains, and set out to "
  "switch his own right hemisphere on {{DRG-LET-1975-SPLITBRAIN}} "
  "{{DRG-LET-1975-ORNSTEIN}} {{DRG-LET-1977-JAYNES}}. Sutin traces the formula to "
  "a Psychology Today article {{DRG-BIO-SUTIN-VITAMINS}}.",

  "The vitamins and the pentothal appear in nearly every causal account Dick "
  "gave. The vitamin C overdose was \"crucial\" for neural firing, and pentothal "
  "is the \"truth drug\" {{DRG-EX-1975-VITAMINC}}; the pentothal and the girl with "
  "the fish necklace were \"necessary causal agents\" {{DRG-EX-1975-CAUSAL}}; to "
  "his mother he lists the pentothal, the vitamin C and the girl together "
  "{{DRG-LET-1976-PENTATHOL}}. Later lists add lithium {{DRG-EX-1978-FLUSHING}}, "
  "and a political version in which a friend had predicted that pentothal would "
  "release a dissociated self {{DRG-EX-1978-HAL}}. Arnold adds Percodan, a "
  "diuretic and psychiatric drugs, and reports claims that Dick was still taking "
  "amphetamines {{DRG-BIO-ARNOLD-COVERT}}.",

  "What Dick never says is that the chemicals made the experience. They released "
  "it, disinhibited it, or prepared the ground. In February 1981 he insists that "
  "when the first-century world broke through he was no longer under the "
  "pentothal {{DRG-LET-1981-NOLONGER}}; six months later the pentothal is how he "
  "got in touch with his unconscious {{DRG-LET-1981-UNCONSCIOUS}}. In 1975 he "
  "conceded that a later vision was \"a mescaline type of experience\" and that he "
  "was \"loaded\", then denied that this explained it {{DRG-LET-1975-LOADED}}; by "
  "1977 the mescaline-like agent was a toxin secreted by his own brain "
  "{{DRG-EX-1977-TOXIN}}."]},

 {"id": "sacrament", "heading": "Intoxication as theology", "register": "A", "body": [
  "In the Exegesis the vocabulary of drugs becomes religious. The pentothal stood "
  "in for the trance of the ancient mysteries, \"perhaps even drug induced\" "
  "{{DRG-EX-1975-MYSTERIES}}. John Allegro, who derived Christianity from a "
  "mushroom cult, was \"partially correct\" {{DRG-EX-1976-ALLEGRO}}, and Dick's "
  "own psychedelic experience may have \"paved the way\" {{DRG-EX-1976-PAVED}}. "
  "LSD reaches one kind of altered time but not eternity, which he reached only "
  "in 2-3-74 {{DRG-EX-1978-THREESTATES}}.",

  "The positions are not consistent. In one entry he was intoxicated in 1974, but "
  "\"not by LSD - it wasn't a flash-back\": by Valis, and Dionysos smuggled the "
  "secret to us {{DRG-EX-1978-NOTLSD}}. In another he crossed into the other world "
  "\"as I had taken a pscyhedelic\" — a sentence that may mean \"as if\" "
  "{{DRG-EX-1978-MUSHROOM}}. In a third, the plasmate needs the sacred mushroom as "
  "catalyst, and \"the drugs I took reacted to the plasmate in me\" "
  "{{DRG-EX-1978-INGREDIENTS}}. Throughout, mankind is \"drugged\" and asleep, "
  "and Substance D is a picture of the human condition {{DRG-EX-1978-JETER}}.",

  "Outside the notebooks, Tim Powers remembered a night in March 1979 when Dick, "
  "having smoked some marijuana, demanded to see God and saw the Ark of the "
  "Covenant — though his visions, Powers adds, were \"generally not dope-related\" "
  "{{DRG-BIO-SUTIN-ARK}}."]},

 {"id": "after", "heading": "After 1972: sober, mostly", "register": "A", "body": [
  "In September 1976 Dick wrote that he took no drugs at all and recommended them "
  "to no one {{DRG-LET-1976-BOGGS}}. A year later, nervous about flying to the "
  "Metz festival, he scored a supply of speed — the only time in his last decade, "
  "Sutin says {{DRG-BIO-SUTIN-METZ}}. Around 1978 he counts among his blessings "
  "that he is \"no longer abusing drugs, legal or illegal\" "
  "{{DRG-EX-1978-NOLONGER}}. Doris Sauter remembered no amphetamines, but \"a "
  "little grass, a little coke\" {{DRG-BIO-ANNE-DORIS}}; and in his last interview "
  "Dick described buying marijuana in order to flush it, because he enjoyed "
  "scoring but did not want to take it {{DRG-INT-1982-FLUSH}}."]},

 {"id": "biographers", "heading": "What the biographers disagree about",
  "register": "C", "body": [
  "Lawrence Sutin (1989) is the most detailed and the most even-handed: he gives "
  "competing witnesses and often declines to choose. On the 1950s he sets a "
  "friend's memory of regular doses against Dick's first wife Kleo's insistence "
  "that he took nothing {{DRG-BIO-SUTIN-BERKELEY}}, and quotes a stepfather's note "
  "dating his use to a prescription from Kleo's father in 1951 "
  "{{DRG-BIO-SUTIN-STANFORD}}. By the Point Reyes years, for Sutin, Semoxydrine "
  "was \"a steady fuel for the writing\" {{DRG-BIO-SUTIN-FUEL}}.",

  "Anne R. Dick (1995), married to him from 1959 to 1964, remembers two "
  "prescribed Semoxydrine a day that she did not ask about "
  "{{DRG-BIO-ANNE-SEMOX}}, and dates recreational use to after he left her "
  "{{DRG-BIO-ANNE-RECREATIONAL}}. Kyle Arnold (2016), a clinical psychologist, reads "
  "the same marriage as a time of secret and escalating doses, and the paranoia "
  "Anne describes as amphetamine paranoia {{DRG-BIO-ARNOLD-ANNE}}.",

  "Arnold's larger thesis is that commentators blamed \"the wrong drug\": not LSD "
  "but amphetamines explain Dick's paranoia {{DRG-BIO-ARNOLD-WRONGDRUG}}, and "
  "everything taken as schizophrenia was amphetamine psychosis "
  "{{DRG-BIO-ARNOLD-PSYCHOSIS}}. Gregg Rickman (1984), the first to set out the "
  "facts, concluded almost the reverse about the novels: their collapsing "
  "realities come from imagination, not from any drugs "
  "{{DRG-SCH-RICKMAN-FACTS}}. Dick himself gave three causes for his madness, of "
  "which drugs were one {{DRG-EX-1978-DRIVENMAD}}.",

  "They also disagree on smaller facts: how many LSD trips, and when; whether "
  "regular speed ended in 1972; how long he stayed at X-Kalay. Each is listed "
  "under Contradictions below with the passages on both sides."]},

 {"id": "cautions", "heading": "What this page does not claim", "register": "D", "body": [
  "It does not say which drug, if any, caused the experiences of 1974. Dick "
  "himself offered pentothal, vitamins, lithium, mescaline-like toxins and "
  "intoxication by God, often in the same year, and never said a chemical "
  "produced them.",

  "It does not represent Anthony Peake. His A Life of Philip K. Dick (2013) is "
  "catalogued, but only its title page is in the archive, so the position "
  "attributed to him in the portal's older essay on this subject cannot be "
  "checked. The same essay mentions a temporal-lobe hypothesis in Arnold; the "
  "archive's text of Arnold does not contain one.",

  "It does not use the lexicon-scanned topic Amphetamine Use. That topic matched "
  "the word \"speed\", and most of its passages concern velocity or the speed of "
  "light. Every passage here was read before it was included.",

  "Dates for the Exegesis are those of the folder or section a passage is filed "
  "in, narrowed where the entry dates itself. Section 016 is filed under October "
  "1978 but runs to 1980; the folder filed under September 1976 runs to 1979."]},
]


# --------------------------------------------------------------------------
# Browse: card groups, facets, see-also
# --------------------------------------------------------------------------

GROUPS = [
    {'key': 'sixties', 'label': 'Letters, 1962–1969',
     'blurb': 'Semoxydrine, the first LSD, and the face in the sky.'},
    {'key': 'marin', 'label': 'Letters, 1970–1973',
     'blurb': 'Mescaline, the Santa Venetia house, Vancouver and X-Kalay, A Scanner Darkly.'},
    {'key': 'letters', 'label': 'Letters, 1975–1981',
     'blurb': 'Vitamins and pentothal; the novel, the legend, and second thoughts.'},
    {'key': 'ex1975', 'label': 'The Exegesis — 1975–76',
     'blurb': 'Pentothal and vitamin C as causes; Allegro; the mysteries.'},
    {'key': 'ex1976', 'label': 'The Exegesis — 1976–79',
     'blurb': 'A Scanner Darkly reread; X-Kalay as brainwashing; a toxin of his own.'},
    {'key': 'ex1978', 'label': 'The Exegesis — 1978–80',
     'blurb': 'The speed-self, the sacred mushroom, intoxication by God.'},
    {'key': 'interviews', 'label': 'Interviews, 1974–1982',
     'blurb': 'Dick answering the drug question in public.'},
    {'key': 'fiction', 'label': 'In the fiction',
     'blurb': "Characters speaking — not Dick — and A Scanner Darkly's Author's Note, which is Dick."},
    {'key': 'biography', 'label': 'The biographers',
     'blurb': 'Sutin, Anne R. Dick and Arnold, and the witnesses they quote.'},
    {'key': 'criticism', 'label': 'Criticism',
     'blurb': 'Rickman, Butler and Jameson — not Dick.'},
]


def group_of(source_type: str, dated: str | None) -> str:
    """Which GROUPS key a card belongs to, from its source and its date."""
    dated = dated or ''
    if source_type == 'interview':
        return 'interviews'
    if source_type in ('fiction', 'paratext'):
        return 'fiction'
    if source_type == 'biography':
        return 'biography'
    if source_type == 'criticism':
        return 'criticism'
    years = [int(y) for y in re.findall(r'19\d\d', dated)]
    if source_type == 'letter':
        if years and max(years) < 1970:
            return 'sixties'
        return 'marin' if years and max(years) < 1975 else 'letters'
    if '1978' in dated or '1980' in dated:
        return 'ex1978'
    if years and min(years) >= 1977 or '1976–79' in dated:
        return 'ex1976'
    return 'ex1975'


# Facets are the browsable vocabulary of the card `concepts`. `link` points at
# the portal page for the facet where one exists. The dictionary has no entries
# for any substance, so substance facets mostly have none.
FACETS = [
    # Substances
    {'label': 'Amphetamines', 'kind': 'substance',
     'aliases': ['Semoxydrine', 'Methedrine', 'Speed']},
    {'label': 'LSD', 'kind': 'substance', 'aliases': ['Acid']},
    {'label': 'Mescaline', 'kind': 'substance'},
    {'label': 'Psychedelics', 'kind': 'substance'},
    {'label': 'Sacred mushroom', 'kind': 'substance'},
    {'label': 'Marijuana', 'kind': 'substance'},
    {'label': 'Heroin', 'kind': 'substance'},
    {'label': 'Sodium pentothal', 'kind': 'substance'},
    {'label': 'Vitamins', 'kind': 'substance', 'aliases': ['Orthomolecular vitamins']},
    {'label': 'Lithium', 'kind': 'substance'},
    {'label': 'Substance D', 'kind': 'substance'},
    {'label': 'Can-D and Chew-Z', 'kind': 'substance'},
    {'label': 'JJ-180', 'kind': 'substance'},
    # Dick's works
    {'label': 'A Scanner Darkly', 'kind': 'work',
     'link': '/exegesis/works/a-scanner-darkly'},
    {'label': 'The Three Stigmata of Palmer Eldritch', 'kind': 'work',
     'link': '/exegesis/works/the-three-stigmata-of-palmer-eldritch'},
    {'label': 'Now Wait for Last Year', 'kind': 'work',
     'link': '/works/now-wait-for-last-year'},
    {'label': 'A Maze of Death', 'kind': 'work', 'link': '/exegesis/works/a-maze-of-death'},
    {'label': 'Flow My Tears', 'kind': 'work',
     'link': '/exegesis/works/flow-my-tears-the-policeman-said'},
    {'label': 'VALIS', 'kind': 'work', 'link': '/exegesis/works/valis'},
    {'label': 'Faith of Our Fathers', 'kind': 'work', 'link': '/works/faith-of-our-fathers'},
    # Themes
    {'label': 'Productivity', 'kind': 'theme'},
    {'label': 'Prescription', 'kind': 'theme'},
    {'label': 'Self-medication', 'kind': 'theme'},
    {'label': 'Drug culture', 'kind': 'theme'},
    {'label': 'Rehabilitation', 'kind': 'theme', 'aliases': ['X-Kalay', 'Synanon']},
    {'label': 'Sobriety', 'kind': 'theme'},
    {'label': 'Suicide', 'kind': 'theme'},
    {'label': 'Paranoia', 'kind': 'theme', 'link': '/studies/psychology/paranoia'},
    {'label': 'Psychosis', 'kind': 'theme', 'link': '/studies/psychology/psychosis'},
    {'label': 'Split brain', 'kind': 'theme', 'link': '/studies/psychology/split-brain'},
    {'label': 'Reputation', 'kind': 'theme'},
    {'label': '2-3-74', 'kind': 'theme', 'link': '/theophanies'},
    {'label': 'Anamnesis', 'kind': 'theme', 'link': '/dictionary/anamnesis'},
    {'label': 'Mystery religions', 'kind': 'theme'},
    {'label': 'Eucharist', 'kind': 'theme', 'link': '/dictionary/eucharist'},
    {'label': 'Dionysos', 'kind': 'theme', 'link': '/dictionary/dionysos'},
    {'label': 'Plasmate', 'kind': 'theme', 'link': '/dictionary/plasmate'},
    # People, real and fictional
    {'label': 'Nancy Hackett', 'kind': 'person', 'link': '/names/nancy'},
    {'label': 'Kleo Apostolides', 'kind': 'person', 'link': '/names/kleo'},
    {'label': 'Tessa', 'kind': 'person', 'link': '/names/tessa'},
    {'label': 'Ray Nelson', 'kind': 'person', 'link': '/names/ray-nelson'},
    {'label': 'K. W. Jeter', 'kind': 'person', 'link': '/names/kw-jeter'},
    {'label': 'Hal', 'kind': 'person', 'link': '/names/hal'},
    {'label': 'Timothy Leary', 'kind': 'person', 'link': '/names/timothy-leary'},
    {'label': 'John Allegro', 'kind': 'person', 'link': '/names/john-allegro'},
    {'label': 'Palmer Eldritch', 'kind': 'person', 'link': '/dictionary/palmer-eldritch'},
    {'label': 'Bob Arctor', 'kind': 'person', 'link': '/names/bob-arctor'},
    {'label': 'Donna', 'kind': 'person', 'link': '/names/donna'},
    {'label': 'Kathy Sweetscent', 'kind': 'person', 'link': '/names/kathy-sweetscent'},
    {'label': 'Horselover Fat', 'kind': 'person', 'link': '/names/horselover-fat'},
    {'label': 'Gloria Knudson', 'kind': 'person', 'link': '/names/gloria-knudson'},
    # Biographers and critics: link to the book in the archive
    {'label': 'Lawrence Sutin', 'kind': 'biographer',
     'link': '/archive/divine-invasions-a-life-of-phi-lawrence-sutin'},
    {'label': 'Anne R. Dick', 'kind': 'biographer',
     'link': '/archive/oceanofpdf-com-the-search-for-philip-k-dick-anne-r-dick'},
    {'label': 'Kyle Arnold', 'kind': 'biographer',
     'link': '/archive/oceanofpdf-com-the-divine-madness-of-philip-k-dick-kyle-arnold'},
    {'label': 'Gregg Rickman', 'kind': 'biographer',
     'link': '/archive/philip-k-dick-in-his-own-words-gregg-rickman-1984'},
]

FACET_KINDS = [
    ('substance', 'Substances'),
    ('work', "Dick's works"),
    ('theme', 'Themes'),
    ('person', 'People and characters'),
    ('biographer', 'Biographers'),
]

SEE_ALSO = [
    {'label': 'Psychology: Paranoia', 'to': '/studies/psychology/paranoia'},
    {'label': 'Psychology: Split brain', 'to': '/studies/psychology/split-brain'},
    {'label': 'Philip K. Dick and the Bible', 'to': '/studies/intertexts/pkd-and-the-bible'},
    {'label': 'Burroughs and the Word Virus', 'to': '/studies/intertexts/burroughs-word-virus'},
]

# Wording for the page's table-of-contents link ("Browse all N passages by ...").
# Read by TopicDetail once the toc_label patch lands (see README); until then
# the page shows its built-in "book & theme".
TOC_LABEL = 'substance, novel & theme'

BROWSE_INTRO = (
    "{n} passages in the archive turn on drugs. Each card summarises the whole "
    "passage and where it sits, then quotes the sentence it turns on; every "
    "quotation is machine-checked against the underlying text before the page is "
    "published. Pick a substance, novel, theme, person or biographer to see only "
    "the passages about it, or a lane to see only one kind of source.")


# --------------------------------------------------------------------------
# Contradictions: (summary, explanation, type, fragment_a, fragment_b).
# The fragments locate the two passages; the seeder refuses to drop one silently.
# --------------------------------------------------------------------------

CONTRADICTIONS = [
    # --- the biographers ---
    ("Between biographers — Point Reyes, 1959–64: two prescribed pills a day, or secret escalating doses?",
     "Anne R. Dick, who was married to him, remembers two Semoxydrine a day and "
     "dates recreational amphetamine use to after he left her in 1964. Kyle Arnold "
     "reads the same marriage as a time of secret and increasingly massive doses, "
     "and her account of his fear of her as amphetamine paranoia. Sutin, between "
     "them, calls Semoxydrine \"a steady fuel for the writing\" by 1960.",
     'interpretive',
     'started taking amphetamines',
     'secretly wolfed down'),

    ("Between biographers — how many LSD trips? Sutin: at least two in 1964. Anne R. Dick: one, after which "
     "he never tried it again.",
     "Both biographers tell the same trip with Ray Nelson — sweating, a spear "
     "thrust, Latin, a Roman gladiator. Sutin adds an earlier dose from Jack Newkom. "
     "Dick told Platt he took it twice.",
     'factual',
     'at least two occasions',
     'he never tried LSD again'),

    ("When did Dick first take LSD? He says 1964; Rickman says not until about 1967.",
     "Dick dated his first trip to 1964 in a 1975 letter and to the month before the "
     "Palmer Eldritch galleys in 1979, and Sutin agrees. Rickman's 1984 "
     "introduction puts it 'about 1967', which makes Palmer Eldritch years earlier "
     "than any LSD.",
     'self_vs_critic',
     'That was in 1964',
     'not ’til about 1967'),

    ("Between biographers — after X-Kalay: no more regular speed, or covert use?",
     "Sutin credits X-Kalay with ending nearly twenty years of regular amphetamine "
     "use in 1972, with one lapse in 1977. Arnold reports that some sources say Dick "
     "was still abusing amphetamines in 1974; his wife Tessa did not see it.",
     'factual',
     'Never again did Phil take speed on a regular basis',
     'Some assert that he was still abusing amphetamines'),

    ("Amphetamine psychosis, or one cause among three?",
     "Arnold holds that every symptom read as schizophrenia is explained by the "
     "amphetamine psychosis Dick 'beyond a shadow of a doubt' had. Dick's own list "
     "puts drugs second, between his wife leaving and an endogenous psychosis.",
     'self_vs_critic',
     'explained by the amphetamine psychosis',
     'endogenous psychosis'),

    ("Between biographers — imagination or drugs? Rickman: the collapsing realities come from imagination. "
     "Arnold: the paranoia comes from speed.",
     "The two are not strictly about the same thing — Rickman speaks of the novels, "
     "Arnold of the man — but they assign the drugs opposite weight. Rickman wrote "
     "to correct the 'acid head' legend; Arnold to correct a focus on 'the wrong "
     "drug'.",
     'interpretive',
     'than from any drugs he ingested',
     'many have focused on the wrong drug'),

    ("Berkeley in the 1950s: no drugs but one sample (Kleo), or Benzedrine since 1951 "
     "(the stepfather's notes)?",
     "Both are witnesses quoted by Sutin. Kleo, Dick's wife at the time, insists he "
     "took nothing but one Semoxydrine sample from her father; the notes of Dick's "
     "stepfather in 1971 record Dick saying he had been on Benzedrine since 1951, "
     "on a prescription from that same father.",
     'factual',
     'Phil took no drugs but Serpasil',
     'on Benzedrine and other drugs since 1951'),

    ("A month at X-Kalay, or three weeks?",
     "Dick wrote that he spent a month there; Sutin says three weeks. Arnold has him "
     "in treatment until March 1972, which conflicts with both.",
     'factual',
     'spent a month there',
     'X-Kalay stay lasted only three weeks'),

    # --- Dick against Dick ---
    ("Did LSD influence his writing? 'None at all' (1973) — except a passage of A "
     "Maze of Death (1976).",
     "In 1973 Dick told Vertex LSD had no influence. In 1976 he named one passage "
     "drawn from his first trip, which Sutin says Dick had in 1974 called his 1964 "
     "vision 'depicted with exact accuracy'.",
     'early_vs_late',
     'none at all',
     'except a small passage in my novel A MAZE OF DEATH'),

    ("Was Palmer Eldritch written with LSD? Dick: before he had ever seen it. Harlan "
     "Ellison: Dick told him it was LSD-inspired.",
     "Ellison's 1967 introduction to Dangerous Visions printed the claim, and Dick "
     "did not correct the galleys; from 1975 he rebutted it. In a 1967 letter he "
     "himself called the novel 'a trip book'. Sutin believes the later denial.",
     'self_vs_critic',
     'I wrote that before I had ever seen LSD',
     'Ellison recalls that Phil assured him'),

    ("Where did Palmer Eldritch's drugs come from? An article by Aldous Huxley, or "
     "reading about hallucinogenic mushrooms?",
     "Dick told Platt in 1979 he had only a Huxley article to go on. Anne R. Dick, "
     "who lived with him while he wrote it, says mushrooms — Chew-Z is made from a "
     "fungus. Both could be true.",
     'interpretive',
     'an article by Aldous Huxley',
     'reading about hallucinogenic mushrooms'),

    ("Was he on anything when he saw the face in the sky in 1963?",
     "In 1974 Dick said he was on no drug at the time. Sutin reports that his "
     "contemporary accounts mentioned 'certain chemicals' and 'psychedelic drugs', "
     "and that the drugs dropped out of later tellings.",
     'self_vs_critic',
     'any other drug, not at the time',
     'certain chemicals'),

    ("LSD since the early fifties (Oui, quoted by Dick to his publisher) — or first "
     "in 1964 (Dick).",
     "Dick passed on Oui's claim as a marketing point in the same letter in which he "
     "complained about Harlan Ellison's. Every other source, his own included, puts "
     "his first LSD in 1964 or later.",
     'self_vs_critic',
     'experimenting with LSD in the early fifties',
     'That was in 1964'),

    ("2-3-74 was not a drug experience — or the drugs he took reacted with the "
     "plasmate.",
     "Two Exegesis entries of 1978–80. In one he was intoxicated 'not by LSD', and "
     "not by a flashback, but by God. In the other the sacred mushroom is a second "
     "ingredient and his own drugs set the plasmate alive. A third entry says he "
     "crossed over 'as I had taken' a psychedelic, which may mean 'as if'.",
     'interpretive',
     'intoxicated, not by LSD',
     'the drugs I took reacted to the plasmate'),

    ("A Scanner Darkly: an attack on drugs, or 'not drugs'?",
     "In 1981 Dick told Rickman he wrote the novel to record the dead and as an "
     "attack on drugs. In the Exegesis around 1978 he decided it was about the "
     "punishment for playing instead of toiling, 'not drugs'.",
     'interpretive',
     'as an attack on drugs',
     'instead of toiling, not drugs'),

    ("A Scanner Darkly as research, or as life?",
     "In 1973 Dick joked that he had to 'partake of dope' to research the novel. The "
     "Author's Note says he was one of the children playing in the street, and is on "
     "the list of the punished. The letter's own jokes undercut its claim.",
     'interpretive',
     'partake of dope to get the true sense of it',
     'one of these children playing in the street'),

    ("X-Kalay saved his life — and was brainwashing.",
     "From inside it in 1972: 'I owe my life to them.' In 1975 its education was "
     "'faulty'; in the Exegesis its Synanon game is the equivalent of Communist "
     "brainwashing, and in A Scanner Darkly the rehabilitation centre grows the drug.",
     'early_vs_late',
     'I owe my life to them',
     'the exact analog of CP brainwashing'),

    ("No drugs at all (1976) — speed for Metz (1977).",
     "Dick told a student in September 1976 that he took no drugs. A year later, "
     "according to Sutin, he scored amphetamines for the trip to France. Not "
     "necessarily a lie; a statement and a later lapse.",
     'self_vs_critic',
     'I take no drugs now at all',
     'score a supply of speed'),

    ("Seven grams of vitamin C a day, seven grams by accident, or seven grams more "
     "than called for?",
     "The Exegesis (1975) says an overdose of seven grams a day; the letter to his "
     "mother (1976) that he had accidentally taken seven grams; Sutin, from the "
     "formula, seven grams more than it prescribed.",
     'factual',
     '7 grams a day',
     'seven more grams of vitamin C than called for'),

    ("He hated pot (Cindy, of 1970) — 'a little grass' (Doris Sauter, of the late "
     "1970s).",
     "Two witnesses in Anne R. Dick's book, describing different periods. Not "
     "necessarily incompatible, but the book does not reconcile them, and Dick's "
     "last interview has him buying marijuana to flush it.",
     'factual',
     'touch pot, he hated it',
     'a little grass'),
]


OPEN_QUESTIONS = [
    "What drugs, if any, preceded the 1963 vision of Palmer Eldritch? — raised under "
    "Palmer Eldritch. Dick denied any; Sutin cites contemporary mentions of "
    "'certain chemicals'. Resolvable by: the 1963–64 letters themselves, which "
    "Sutin cites but this archive does not hold.",
    "When was the first LSD trip, and how many were there? — raised under LSD and "
    "mescaline. 1964 or 1967; one, two or three. Resolvable by: Ray Nelson's and "
    "Jack Newkom's own accounts.",
    "What does Anthony Peake say? — raised in the cautions. His biography is "
    "catalogued but its text is not in the archive, so the portal's older "
    "description of his position cannot be checked. Resolvable by: ingesting the "
    "book.",
    "Did Dick take amphetamines after 1972? — raised under After 1972. Sutin says "
    "once, in 1977; Arnold reports unnamed sources who say he was still abusing "
    "them in 1974. Resolvable by: Arnold's sources, which the passage does not "
    "name.",
    "How long was the X-Kalay stay? — a month (Dick), three weeks (Sutin), or to "
    "March (Arnold). Resolvable by: X-Kalay's records, or dated letters from "
    "March–April 1972.",
    "Which passage of A Maze of Death is the LSD vision? — Dick names the novel; "
    "Sutin quotes a 1974 letter identifying it, which this archive does not hold. "
    "Resolvable by: that letter.",
    "What is the drug in Flow My Tears, the Policeman Said? — the novel's text is "
    "not in the archive, so the page cannot quote it. Resolvable by: ingesting the "
    "novel.",
]

RELATED_THINKERS = [
    'John Allegro', 'Albert Hofmann', 'Aldous Huxley', 'Timothy Leary',
    'Carlos Castaneda', 'Robert Ornstein', 'Joseph Bogen', 'Julian Jaynes',
    'Harvey Ross', 'Lawrence Sutin', 'Anne R. Dick', 'Kyle Arnold', 'Gregg Rickman',
]

FIELDS = {
    'definition': (
        "Philip K. Dick's use of and writing about drugs: prescribed and street "
        "amphetamines from the early 1950s to 1972; LSD on two or three occasions "
        "from 1964 and one large dose of mescaline in 1970; a month at the X-Kalay "
        "rehabilitation house in 1972; the sodium pentothal and vitamins around "
        "February–March 1974; and the drugs of his fiction — Can-D and Chew-Z, "
        "JJ-180, Substance D."),
    'pkd_relevance': (
        "Amphetamines paced the writing of the 1950s and 1960s, by Dick's own "
        "account; LSD shaped his reputation more than his work; A Scanner Darkly "
        "records the drug culture of 1970–72; and in the Exegesis intoxication "
        "becomes a model of the human condition and a candidate cause of 2-3-74."),
    'in_the_fiction': (
        "Now Wait for Last Year (JJ-180), The Three Stigmata of Palmer Eldritch "
        "(Can-D, Chew-Z), A Scanner Darkly (Substance D), VALIS (the Bay Area of "
        "1971). In each, a drug hands control of the user's reality to someone "
        "else. Characters speaking, not Dick."),
    'in_the_exegesis': (
        "1975–80: pentothal and vitamins as disinhibitors; LSD below eternity; "
        "Allegro's sacred mushroom and Dionysian intoxication; the 'speed-self' that "
        "collapsed in 1974; A Scanner Darkly reread as a picture of a drugged "
        "mankind."),
    'intellectual_background': (
        "Mid-century amphetamine prescribing; the psychedelic literature (Huxley, "
        "Hofmann, Leary); orthomolecular psychiatry and split-brain research "
        "(Ross, Ornstein, Bogen); Synanon-model rehabilitation; Allegro's The Sacred "
        "Mushroom and the Cross."),
    'scholarly_debate': (
        "How much of Dick's paranoia was amphetamine psychosis (Arnold) and how much "
        "of the fiction owes to drugs at all (Rickman); the chronology of use during "
        "the Point Reyes marriage (Anne R. Dick against Arnold); the count and date "
        "of the LSD trips (Sutin, Anne R. Dick, Rickman)."),
    'chronology_summary': (
        "c. 1952: first Semoxydrine. 1958–64: two a day at Point Reyes. 1964: "
        "recreational amphetamine; first LSD. 1964–70: pills from several doctors. "
        "May 1970: mescaline, Flow My Tears. 1970–72: the Santa Venetia house; a "
        "thousand tablets a week. March 1972: Vancouver, X-Kalay. 1973: A Scanner "
        "Darkly finished. February–March 1974: pentothal, vitamins, 2-3-74. 1976: "
        "'I take no drugs now at all.' 1977: speed for Metz. 1978–80: the Exegesis "
        "on intoxication. 1982: marijuana bought and flushed."),
    'contradictions_summary': (
        "Twenty, kept rather than resolved: four between biographers (Point Reyes "
        "doses, LSD count, sobriety after 1972, paranoia's cause), others between "
        "Dick and his biographers and witnesses (the LSD date, Palmer Eldritch and "
        "LSD, the 1963 vision), and Dick against himself (LSD's influence, 2-3-74 and "
        "drugs, A Scanner Darkly's subject, X-Kalay)."),
    'editorial_notes': (
        "Every passage was chosen by reading it, from a sweep of the whole corpus "
        "with scripts/research/sweep_corpus.py --profile drugs. The lexicon topic "
        "Amphetamine Use, which matched the word 'speed', was not used. Fiction is "
        "lane A; the Exegesis lane B; criticism lane C; biography lane D; letters, "
        "interviews and A Scanner Darkly's Author's Note lane E."),
}
