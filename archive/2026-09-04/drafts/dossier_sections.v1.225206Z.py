#!/usr/bin/env python3
"""
The authored essay, section by section, in chronological order.

Kept as Python rather than raw JSON so the prose stays readable and diffable in
git history, the same way mention_cards.py holds the card text. Run
`build_dossier.py` to merge it into dossier.json, which is what the seeder reads.

Citations in {{double braces}} are finding ids from evidence-inventory.json. The
seeder refuses to build if one does not resolve, and verifies every quotation of
40+ characters against the source it comes from.

Registers: A = PKD's own words, B = primary-source fact, C = scholarly argument,
D = portal-editor inference.
"""

SUBTITLE = ("Five years of argument with one idea, told in order — from a jacket "
            "blurb in January 1976 to the last letter of August 1981.")

SECTIONS = [

 {"id": "note", "heading": "Burroughs and the Word Virus", "register": "D", "body": [
  "For the last five years of his life Philip K. Dick argued with an idea he had got "
  "from William S. Burroughs: that language is a virus. Burroughs’s proposition, "
  "developed across the Nova trilogy and stated most compactly in The Ticket That "
  "Exploded (1962), is that words are a parasitic organism which entered the human "
  "nervous system from outside, replicates through speech and print, and holds its hosts "
  "in a condition they cannot perceive — because the apparatus that would perceive it "
  "is itself infected. Dick read it in September 1976, two and a half years after the "
  "experiences he called 2-3-74, and recognised it immediately as a description of what "
  "he thought had happened to him.",

  "What he did with it is the subject of this page, and it is not what “influence” "
  "usually means. He took the vocabulary whole — word virus, information virus, Nova "
  "Mob, Nova police, latent message — and never gave it up; he is still using the term "
  "“information virus” in the sentence where he denies there is one. But he began "
  "revising the mechanism within hours of first reading it, and over five years produced "
  "at least seven incompatible accounts of what the thing is: an infection he had thrown "
  "off, a jamming device that blocks reception rather than carrying anything, a cure, an "
  "enslaving life form that “kills us”, a blindness that is not a virus at all, an "
  "escaped Soviet technology, and Satan’s beauty. He never chose between them.",

  "The Burroughs material also collects the themes Dick worked on hardest. Occlusion — "
  "the impairment that prevents us noticing we are impaired — appears in eleven of "
  "these passages, more often than any other idea, and A Scanner Darkly is the novel he "
  "reaches for each time. Living information, the plasmate, and the Logos come through "
  "the same door: the phrase “living information” is coined in a passage about "
  "Burroughs. So do the Black Iron Prison, Zebra, Thomas and Firebright; the cut-up "
  "method and the latent message; the Torah as a programming system; paranoia, both "
  "Burroughs’s and his own; and the question of whether Ubik, Flow My Tears and The "
  "Three Stigmata of Palmer Eldritch had been reporting on reality rather than inventing "
  "it. Burroughs is also, quite separately, a prose model: Dick names him twice as an "
  "ingredient of VALIS, once on a five-name reading list for a beginner, and once as "
  "worth more than philosophy — “Ponderous books of philosophy won’t help me; "
  "Burroughs’ ‘Junky’ will.”",

  "The evidence is almost entirely in Dick’s own hand and almost entirely private. "
  "Thirty-eight passages of Exegesis, twelve letters, one interview and one essay; four "
  "scholars and the edition’s own editors have written about the connection, and no "
  "work of Dick’s fiction mentions Burroughs at all. Nothing in the archive records "
  "Burroughs ever reading or commenting on Dick. It is a one-sided conversation, "
  "conducted mostly at night in a notebook.",

  "One question has to be raised before the chronology can start, because it decides "
  "what kind of relationship this is. Writing in April 1981, Dick says he had noticed "
  "the drug-users’ occlusion “Back in 1971 before I knew of Burroughs”, and had put "
  "it into A Scanner Darkly {{BWV-LET-1981-04}}. If that is right, the central idea was "
  "his before he encountered Burroughs at all, and what Burroughs supplied in 1976 was "
  "not a discovery but a name and a mechanism for something already observed. The "
  "archive neither confirms nor refutes it. No document here mentions Burroughs before "
  "January 1976; Sutin places him in Dick’s lifelong reading without giving a date "
  "{{BWV-SCH-SUTIN-02}}; and the 1971 claim is itself made ten years after the fact, by "
  "a man reconstructing his own history. All three statements can be true together. What "
  "they agree on is the order: the observation first, the vocabulary afterwards. That is "
  "a confirmation rather than an influence, and it is why this page is organised as an "
  "argument Dick has with a book rather than as a debt he owes it.",

  "A note on dates, because the order took some establishing. Our records give each "
  "Exegesis container document a single date, and for the section labelled “October 10, "
  "1978” that date is wrong for most of its contents: six of its passages carry internal "
  "stamps from September to December 1980 — “9-10-80”, “10-20-80”, “11-17-80” — "
  "and the published edition independently places three of them in late 1980. What had "
  "looked like a middle phase in 1978 is mostly a burst in the autumn of 1980, eighteen "
  "months later and much closer to the VALIS letters. Every passage below carries its "
  "date and the evidence for it; where nothing settles a date, the page says so. A "
  "related question the archive cannot answer: why the 2011 Jackson and Lethem edition "
  "prints only eight of our thirty-four Exegesis passages, omitting the anti-information "
  "redefinition, the 1978 revaluation of the virus as a cure, and the whole persistence "
  "of the occluding reading in 1981.",
 ]},

 {"id": "blurb", "heading": "January 1976: a name on a list", "register": "A", "body": [
  "The first time Burroughs appears in Dick's papers, he is a marketing problem. "
  "Doubleday had taken A Scanner Darkly and wanted endorsements from writers with "
  "standing among college readers. On 12 January 1976 Dick explained the plan to his "
  "friend Bill Sarill: they intended to run off Xerox copies of the manuscript and "
  "“get prominent American literary figures known to the college people to read them "
  "and respond with comments”. The names were not his: “They want people like William "
  "Burroughs, Kurt Vonnegut—all the counterculture cult heroes to read it.” "
  "{{BWV-LET-1976-01}}",

  "Then the difficulty, stated without self-pity: “BUT, and here is the rub: it is up "
  "to me to approach such people, these literary greats, and in point of fact I don't "
  "know any of them at all. Only people I know are other s-f writers.” The same day he "
  "wrote to his agent Sharon Jarvis, falling back on review quotations because he could "
  "not reach the writers themselves, and copying out a line from Oui: “In many ways, "
  "Phil Dick is to psychedelics and science fiction what William Burroughs is to hard "
  "drugs and mainstream literature.” {{BWV-LET-1976-02}} The comparison that would "
  "follow both men for decades starts here, and it is a magazine's, not his.",

  "Two things are worth holding on to. Dick did not know Burroughs, and nothing in the "
  "archive suggests he had yet read him. And whether the approach ever reached Burroughs "
  "— whether Burroughs ever read or said anything about Dick — has no answer here. No "
  "reply appears in this archive, and no statement by Burroughs about Dick appears "
  "anywhere in it. As documented, the relationship runs one way. The Burroughs papers at "
  "Ohio State and the Berg Collection would be the place to look.",
 ]},

 {"id": "ticket", "heading": "September 1976: the book arrives", "register": "A", "body": [
  "Eight months later Burroughs stops being a name and becomes an argument. Sutin "
  "supplies the intermediary: the “KW” credited throughout the September 1976 entries is "
  "the writer K. W. Jeter, who had resumed his friendship with Dick in late 1976 and who "
  "“called attention to the similarities between Phil's novels and those of William "
  "Burroughs-such as an invading alien virus occluding human faculties (for Burroughs, "
  "the virus is language)” {{BWV-SCH-SUTIN-01}}.",

  "The entries read like a man checking a book against his own life and finding the "
  "pages match. Burroughs's Nova Mob are parasites who move from host to host and betray "
  "themselves by keeping the same habits, down to a taste for peanut butter; Dick had "
  "felt something take him over in 3-74 and had named it Thomas. “This was exactly true "
  "about Thomas,” he writes, and then turns it on his own body: “I've subjectively felt "
  "myself as a female, a womb into which something like an egg (Firebright) was "
  "deposited—like a cuckoo egg. Was Thomas a saprophyte turned parasite, and deposited "
  "his 'egg' in me?” The question he reaches is not literary: “Does this mean that "
  "Burroughs is either intentionally or unintentionally describing something which is "
  "true?” {{BWV-EX-1976-01}}",

  "The thesis arrives in a sentence — “Burroughs speaks of a virus—a word became a "
  "neural-cell virus, infecting us” — followed by what he did next: “After reading "
  "Burroughs, I dipped into Ubik. It certainly would be easy— and reasonable—for a "
  "reader to think that both Burroughs and I know something, and we want our novels to "
  "be taken as at least partly true.” {{BWV-EX-1976-02}}",

  "Within the same sitting the whole apparatus has been mapped onto his own. The power "
  "that intervened in 3-74 is “Equal to Burroughs' nova police” {{BWV-EX-1976-07}}. The "
  "concealment that hides Rome from ordinary sight “fits the \"replicating virus\" theory "
  "of Burroughs - I would say as Gestalt, as shaping” {{BWV-EX-1976-11}}. The two warring "
  "transtemporal organisms are “very much like Burroughs' formulation (the Nova Mob vs "
  "the pursuing Nova police - + he has the latent message theory, too)” "
  "{{BWV-EX-1976-12}}. The world's concealed hostile entities fit “the theory (Burroughs' "
  "included) that this world contains evil entities wearing ordinary human semblance” "
  "{{BWV-EX-1976-05}}. And the covert agent who must not know he is an agent becomes “a "
  "cop tracking down some evil (enslaving BIP) criminals - shades of Burroughs' nova Mob "
  "+ the Nova police whom come after them! A cop with amnesia.” {{BWV-EX-1976-10}} In one "
  "entry he changes sides entirely and becomes the quarry: “Burroughs is right about the "
  "Nova police + their tracking down their quarry.” {{BWV-EX-1976-09}}",

  "The hinge is his reading of 3-74 as a remission. Burroughs “may have got the real "
  "situation down” in The Ticket That Exploded — “the criminal virus related to words, "
  "submessages, the nova police” — and if that is right, then “what happened to me in "
  "3-74 is that I temporarily got well - was somehow able to throw off the word virus "
  "which had entered me + infected me - or it was done for me” {{BWV-EX-1976-06}}. The "
  "entry does not end in triumph: “But finally I was reinfected + again blinded.”",

  "How much Burroughs he had actually read is the first thing the archive will not "
  "settle. Only two titles are ever named across the whole corpus — The Ticket That "
  "Exploded here, and Junky four years later {{BWV-EX-1978-08}} — yet the Nova Mob "
  "material he uses runs through Nova Express and The Soft Machine as well, and the "
  "cut-up method through The Third Mind. He may have read the trilogy; he may have had "
  "its apparatus from Jeter and one novel. An inventory of his library, if one survives, "
  "would answer it.",
 ]},

 {"id": "antiinformation", "heading": "The same sitting: anti-information",
  "register": "A", "body": [
  "Then, without pausing, he changes it. Burroughs's virus is information that infects. "
  "Dick's is a block on reception: “The virus (of Burroughs) is an information (or word) "
  "virus, but in this sense: it blocks to reception of information. So it is an "
  "anti-information virus.” {{BWV-EX-1976-03}} He illustrates it at once from his own "
  "fiction — the erased instruction tape in A Maze of Death, the recording that would "
  "have told the characters what they were for.",

  "He works out how the jamming operates on both channels, taking from Burroughs the "
  "observation that inner silence cannot be held: “as burroughs points out, over 10 "
  "seconds of inner silence is impossible: innerchatter occurs. There is an inner "
  "raving, howling, clamaring bug, which deliberately creates derogatory noise on the "
  "line at all times.” {{BWV-EX-1976-04}} If we receive a bare-bones transmission and "
  "complete it ourselves, that also explains the cut-ups: “This would explain Burroughs' "
  "results in obtaining living, latent messages normally passing us by” "
  "{{BWV-EX-1976-08}} — the messages are latent because we supply the surface.",

  "And in the same sitting the borrowed term becomes his own. Starting from the printed "
  "words KING FELIX seen carrying “the red + gold plasmic” energy, he notes that "
  "“Burroughs posits an information virus”, records Jeter's dissent in a parenthesis — "
  "“(Not so, K.W. says.)” — and arrives at the phrase he will use for the rest of his "
  "life: “If that plasmic energy is alive, + it is (or it carries) information, then we "
  "have living information. Logos?” {{BWV-EX-1976-13}}",

  "This is the most consequential move in the whole relationship and it happens on day "
  "one. Once the virus is defined by what it prevents rather than by what it carries, "
  "the question of whether information is friend or enemy is wide open. He spends five "
  "years failing to close it.",
 ]},

 {"id": "y1978", "heading": "1977–1978: the cut-up, and a criminal virus",
  "register": "A", "body": [
  "The next stretch is thinly dated and has to be reconstructed. One passage, printed in "
  "the 2011 edition at folio 15:100 and absent from our transcriptions, can be bracketed "
  "only between March 1977 and September 1978. It is the fullest thing Dick ever wrote "
  "about the cut-up. Asking whether the latent story inside Flow My Tears might be “a "
  "sort of living DNA” guiding an entelechy through its growth, he reaches for Bateson's "
  "immanent mind and reads his own novel as an object to be divined: it shows “bench "
  "marks” of the mind that fashioned me and all other life; it is mind perhaps, exerted "
  "directly on the novel (incised form) as if not through me—it is direct arrangement. "
  "(Like tea leaves, or animal entrails.) (Cf. Burroughs' cut-up message pieces latent "
  "meaning-extraction method.)” The paragraph ends in the eucharist, and in the "
  "formulation that governs the late work: “A living word-entity is here with us, taking "
  "us over via messages we receive; we act as hosts to it (perhaps temporarily). We "
  "become it.” {{BWV-EXP-15-100}}",

  "Sutin reports that Dick and Jeter did not only theorise about the method: they "
  "“performed their own Burroughsinfluenced “cut-up” writing experiment, scrambling "
  "texts from Roderick Thorp's The Detective, Melville's Moby Dick, and the New "
  "Testament Book of Acts” {{BWV-SCH-SUTIN-01}}. Sutin gives no date; the glossary to "
  "the published edition does, and says 1978 {{BWV-EXP-90-6A}} — the only dating of it "
  "anywhere in the archive. Nobody remarks on how close two of Dick's convictions sit "
  "here: the Book of Acts is the source of exactly the material he insists, repeatedly, "
  "assembled itself into Flow My Tears without his intending it. Whether the experiment "
  "produced that conviction, tested it, or followed it is unresolved. Jeter was "
  "interviewed by Andy Watson; his account would be the place to start.",

  "Two passages sit in the autumn of 1978, bracketed by dated entries on either side. "
  "The first is the strongest endorsement Dick ever gives. Reading 3-74 as a "
  "detoxification, he settles the question of whether human faculties are impaired or "
  "merely undeveloped: “Then it is evident that our proper full functioning is impaired, "
  "rather than just not (yet) achieved. Then we are \"cursed.\" William Burroughs is "
  "correct. + not just me qua me but us as a species, a race - all of us” "
  "{{BWV-EX-1978-01}}.",

  "The second, printed at folio 19:35, is the most precise account he gives of why the "
  "impairment cannot notice itself — and the passage that most deserves to be better "
  "known. “Axiomatically, if you derange the brain in precise ways, not only will it be "
  "deranged, but if you have affected precisely the correct circuits it will be unaware "
  "that it is impaired and so not seek to rectify the damage. It is as if the immune "
  "system has failed to detect an invader, a pathenogen (shades of William Burroughs: a "
  "criminal virus!). Yes, the human brain has been invaded, and once invaded, is "
  "occluded to the invasion and the damage resulting from the invasion.” "
  "{{BWV-EXP-19-35}} He names A Scanner Darkly in the same breath as “the Key Book in "
  "the sequence”.",

  "A third passage from the same folders performs the reversal that everyone dates to "
  "1981, three years early. Working from The Three Stigmata of Palmer Eldritch and "
  "transubstantiation, Dick keeps the phrase and flips its sign: “But this is not an "
  "occluding, toxifying \"virus\" - it is an antitoxic, de-occlusive.” The information "
  "virus has become Zebra, and he maps it onto four of his own novels — it abolishes the "
  "counterfeit world, “abolishes the inner occlusion” of A Scanner Darkly, breaks the "
  "astral determinism of The Electric Ant, and “removes amnesia” in Impostor "
  "{{BWV-EX-1978-02}}. Nothing in 1981 says it more plainly.",

  "In the same period he wrote the clearest statement he ever made about language and "
  "control, and Burroughs is nowhere in it: “The basic tool for the manipulation of "
  "reality is the manipulation of words. If you can control the meaning of words, you "
  "can control the people who must use the words.” The authority he cites is Orwell "
  "{{BWV-ESS-1978-01}}. That omission will matter later, when a scholar reads the same "
  "sentence as evidence of Burroughs's proximity.",

  "Three further passages from this container cannot be dated at all: a random sentence "
  "generator producing the second Advent {{BWV-EX-1978-03}}, the plasmate's messages "
  "reconsidered {{BWV-EX-1978-05}}, and message collages “related to william Burroughs "
  "latent messages + info virus” whose syntax only Valis can read {{BWV-EX-1978-11}}.",
 ]},

 {"id": "y1979", "heading": "October 1979: “of which I was one”", "register": "A", "body": [
  "A gap of a year, and then a small letter that says something none of the others do. "
  "The first issue of Rolling Stone College Papers had carried Dick's story “Strange "
  "Memories of Death” alongside an article on Burroughs and an interview with him. "
  "Thanking the editor, Dick notices the fit: “The material on William Burroughs—the "
  "article and then the interview—is/are fascinating, and his interview leads right into "
  "my story inasmuch as he discusses the rebellion during the Fifties and the Beats, of "
  "which I was one.” {{BWV-LET-1979-01}}",

  "It is the only place in the archive where Dick claims the Beat affiliation for "
  "himself, and he does it in passing, as a reason two pieces of magazine copy sit well "
  "together. Whatever else Burroughs was to him, by 1979 he was also a contemporary — "
  "someone Dick could be printed next to.",
 ]},

 {"id": "y1980", "heading": "Autumn 1980: five accounts in five months",
  "register": "A", "body": [
  "This is the material our records had filed under 1978, and re-dating it changes the "
  "story. Between August and December 1980 — the months immediately before the VALIS "
  "letters — Dick writes four mutually exclusive accounts of the same idea and does not "
  "choose between them.",

  "In August or September, the qualified endorsement. The Acts material in Flow My Tears "
  "was self-generating, and the KING FELIX cipher is “a tracing, but this information is "
  "alive or semi-alive like a virus; Burroughs is right but he has only a bit of the "
  "whole picture...still, there is such a thing as living latent information” "
  "{{BWV-EX-1978-04}}.",

  "On 10 September, the darkest version. Asking what the stolen secret of his visionary "
  "material was, he answers with visible reluctance: “It is (I hate to say this, but...): "
  "there is an occluding life form here; it not only occludes us, but it enslaves us and "
  "Kills us. We can't see it; that's part of the occlusion. Bur¬ roughs is right. Is it "
  "the plasmate? maybe so. An \"information virus.\"” {{BWV-EX-1978-06}} That last "
  "question is the whole problem in five words: the entity he elsewhere calls the "
  "physician may be the disease.",

  "Later in September, the opposite. The sacred narrative replicates itself in newly "
  "generated information, and “This is what William Burroughs discovered (but interprets "
  "differently)” {{BWV-EX-1978-07}} — the same phenomenon, read as the ground of being "
  "rather than as an infection. Somewhere in the same stretch he performs a rare audit "
  "of one of his own convictions, abandoning his long-held reading of the plasmate's "
  "messages as a contamination: “It has been my view for several years that the "
  "plasmate’s messages were a \"contamination,\" but this view is based on (1) Eurrough's "
  "information virus theory; and (2) paranoia and paranoiac fear.” {{BWV-EX-1978-05}} He "
  "is treating an influence as a possible contaminant in its own right.",

  "On 20 October, he throws the frame out altogether. “We're under a spell. This is no "
  "information virus; this is blindness. Exactly as in EYE; private worlds. Idios "
  "kosmos.” {{BWV-EX-1978-09}} If the problem is blindness there is nothing to throw "
  "off, and the diagnosis becomes enchantment — “It's the work of a magician.”",

  "And in November or December, the most literal-minded version of all, complete with "
  "its question mark: “Some kind of living information (Burrough's information virus) "
  "got away from the Soviets + is replicating as a life form?” {{BWV-EX-1978-10}} Around "
  "the same time, on method rather than doctrine: “The long path is the short path. "
  "Ponderous books of philosophy won't help me; Burroughs' \"Junky\" will.” "
  "{{BWV-EX-1978-08}}",

  "Five readings, five months, none discarded. It is tempting to call this thinking "
  "aloud, but Dick writes elsewhere in the Exegesis that “we are going to have to deal "
  "with propositions which are simultaneously both true and false”. Taking that "
  "seriously would change how the whole notebook should be read, and not only this "
  "topic — a question for the portal's other studies as much as this one.",
 ]},

 {"id": "y1981feb", "heading": "February 1981: what VALIS was made of",
  "register": "A", "body": [
  "With VALIS about to appear, Dick twice describes what went into it, and Burroughs is "
  "named both times — as a source of prose, not of doctrine. To the fanzine editor "
  "Richard E. Geis, defending the book against the charge of being simple autobiography, "
  "he sets out the intention: “my purpose was to achieve a new kind of prose, a new kind "
  "of blending of the ancient picaresque form with certain modern elements associated "
  "with Hunter S. Thompson and William S. Burroughs, as well as my own 1977 novel A "
  "SCANNER DARKLY” {{BWV-LET-1981-02}}.",

  "Three days later, to the scholar Patricia Warrick, the same account with the politics "
  "attached: “my writing is protest art pitted against official culture, formal culture. "
  "Hence my use of the vernacular in VALIS. It is a picaresque novel blended with new "
  "elements derived from William Burroughs, Hunter S. Thompson and my own earlier novel, "
  "A SCANNER DARKLY.” {{BWV-LET-1981-03}} A month earlier, advising a beginning writer, "
  "he had put Burroughs on a short reading list — “read the great prose writers: "
  "Faulkner, Hemingway, Hunter S. Thompson, William Burroughs, Saul Bellow, Herbert "
  "Gold.” — every one of them outside science fiction {{BWV-LET-1981-01}}.",
 ]},

 {"id": "y1981apr", "heading": "15 April 1981: the letter to Brig Elliot",
  "register": "A", "body": [
  "Then a stranger writes to him, and Dick sets out his position more completely than he "
  "ever manages in the notebooks. We know almost nothing about Brig Elliot. He "
  "recommended Flann O'Brien's The Third Policeman, he had read The Tibetan Book of the "
  "Dead, and Dick answered him at length and with unusual care. His original letter is "
  "not in the archive, so we cannot see what was actually asked — a pity, because the "
  "reply is the single most useful document in this dossier.",

  "He begins by conceding the reading and dating his own observation: “Yes, to a degree "
  "I am familiar with William Burroughs' writing (e.g. TEIE TICKET THAT EXPLODED); I am "
  "familiar with his theory of an information virus. And, in respect to that, the "
  "concept of latent information riding our ostensible traffic. Back in 1971 before I "
  "knew of Burroughs I noted a thinking dysfunction or occlusion in people involved with "
  "drugs; I deal with this in A SCANNER DARKLY.” {{BWV-LET-1981-04}}",

  "That sentence carries the second thing the archive will not settle. Dick places the "
  "observation in 1971 and the reading later; Sutin places Burroughs in his lifelong "
  "reading and gives no date {{BWV-SCH-SUTIN-02}}; and no document here mentions "
  "Burroughs before January 1976. The three are compatible with several chronologies. "
  "What they agree on is the direction: the observation came first, and Burroughs "
  "arrived afterwards to name it. That is a confirmation, not an influence.",

  "Then the balance, and it is the fairest thing Dick ever wrote about someone he "
  "disagreed with: “I cannot accept Burroughs' view that we have been invaded by an "
  "alien virus, an information virus, yet on the other hand I cannot readily dismiss "
  "this bizarre theory as mere paranoia on his part. I think he is onto something real "
  "and important, and that his statements do more good—far more good— than harm (that "
  "is, he states the problem correctly, although perhaps his analysis of the cause is "
  "faulty; still, merely to be aware of the problem is to achieve a great deal).” "
  "{{BWV-LET-1981-05}}",

  "Having found the same occlusion described in ancient sources, he removes the need for "
  "an invasion — if the condition exists it is very old — and reduces the disagreement "
  "to a single question of valence: “Where Burroughs and I sharply disagree is that my "
  "supposition is that if— if—an information life form exists (and this is indeed a "
  "bizarre and wild supposition), it is benign; it does not occlude us; on the contrary: "
  "it informs us (or perhaps it has no interest in doing either, but simply rides our "
  "own information traffic, using our media as a carrier; that is entirely possible).” "
  "{{BWV-LET-1981-06}} The parenthesis is a third position, offered and not pursued: an "
  "information life form indifferent to us.",

  "And then the letter does something the notebooks never manage. It turns the "
  "hypothesis on the person holding it. “[i]f you grant an occluding information virus, "
  "are you not then yourself occluded in your very analysis of it, as well as your "
  "perception of its existence? There is a paradox involved. I’m sure you can see that. "
  "And I try to deal with it in VALIS.” {{BWV-LET-1981-06B}} That is the sharpest "
  "sentence in the dossier and it is not a flourish: it is why the late novels are built "
  "around a narrator who cannot be trusted about the thing he is narrating. Whether "
  "VALIS contains a solution or only a dramatisation of the trap is a question about the "
  "novel that the Exegesis raises and does not answer.",
 ]},

 {"id": "y1981apr16", "heading": "16 April 1981: the reversal, and its refusal to hold",
  "register": "A", "body": [
  "The next day, the Exegesis states the inversion outright. “Man is not occluded by an "
  "\"information virus,\" i.e. living information; on the contrary: man is occluded and "
  "the living information is sent to tell him the true situation, that Christ is here.” "
  "Burroughs, he writes, “has discerned (1) living information; and (2) an occlusion and "
  "leaped to the pessimistic conclusion that there is a cause-and-effect relationship; "
  "the living information causes the occlusion. This is a very traditional \"they're "
  "invading us secretly\" s-f view.” {{BWV-EX-1981-02}} He has diagnosed the error as a "
  "genre habit — and still concedes, in the next clause, that Burroughs is onto the "
  "truth.",

  "Elsewhere in the same sitting he ranks his authorities, and Burroughs comes second to "
  "a theologian: “Then there is an occlusion, as Calvin says. And only Christ can lift "
  "the occlusion. Burroughs, too, in his own way is right. I was right when I wrote "
  "SCANNER.” {{BWV-EX-1981-01}}",

  "The one-day gap between the letter and the entry is worth recording and worth not "
  "over-reading. Both documents survive with those dates and the letter is the earlier; "
  "that is all the archive establishes. It does not show that writing to a stranger "
  "forced the formulation, and it does not show that the notebook came first and the "
  "letter reported it. Dick had been circling the problem since 1976, and these may be "
  "one train of thought surfacing twice in two days. Brig Elliot's original letter would "
  "help; it is not here.",

  "What is clearer, and much less often noticed, is that the reversal does not survive "
  "its own sitting. Torah takes over the role of the virus: “Thus Torah assumes the role "
  "of Fate: \"the book of the spinners\". It programs + controls us. So it is like an "
  "occluding information virus; it keeps us enslaved at the level of machines.” "
  "{{BWV-EX-1981-03}} The living information does too: “This living info is divine but "
  "so am I. + it controls us (as Burroughs teaches); more, it assumes the guise of "
  "[being a] world (my view here is a radical acosmism).” {{BWV-EX-1981-09}} And in the "
  "darkest turn in the whole dossier, the beauty he saw in 3-74 becomes a trap: “I "
  "[saw/say] Satan won, he ensnared him as the info virus of Burroughs, ensnared him "
  "with beauty. So: Manichaenism, Burroughs + the story of Satan (world) tempting "
  "Christ.” {{BWV-EX-1981-07}}",

  "He does not choose between them. He sets a second information against the first: "
  "“Thus in a sense as the \"information virus\" controls + occludes + enslaves us, it "
  "itself has been penetrated by a living hyper-information (which I associate with "
  "Christ's sacrificial blood).” {{BWV-EX-1981-04}} Frozen information against living "
  "information, and the combat left running.",

  "The same sitting contains his own instructions for reading VALIS against Burroughs. "
  "“Someone in reading \"Valis\" will see the correlation to Burroughs” — and then the "
  "distance, in five words: “But W. Burroughs not Valentinus.” {{BWV-EX-1981-05}} The "
  "gnostic lineage matters more to him than the Beat one. He argues that the book was "
  "split into dual messages by the very thing it describes, and that Burroughs missed "
  "the scale: “Burroughs never guessed this: his info virus creates a whole spurious "
  "universe for us - but in 3-74 I saw it as it is” {{BWV-EX-1981-06}}. And when he "
  "finally names a frame he prefers, it is not Burroughs: “Only when I read Jonas on "
  "Manichaeism did I understand. This very slightly resembles Burroughs, but is much "
  "more radical (ontologically speaking).” {{BWV-EX-1981-08}}",

  "One further passage from the same days gives the cut-up its cause. If Hagia Sophia "
  "reads the Torah aloud and that reading is the world, then any fragment of text is "
  "already inside the narration: “This is why -as William Burroughs found- when any "
  "written text is cut up + rejoined at random, a narrative results.” {{BWV-EX-1981-10}} "
  "The randomness is not making meaning; it is exposing meaning already there.",
 ]},

 {"id": "y1981aug", "heading": "August 1981: the last word", "register": "A", "body": [
  "Four months later, writing to Patricia Warrick, Dick gives the calmest formulation of "
  "all, and corrects his own novel while he is at it. What he should have said in VALIS, "
  "he decides, is that rolling the universe back to its ontological source yields “the "
  "Word or Torah, which shows up here visibly as Scripture, but exists in latent—that "
  "is, invisible to us—form ubiquitously”. The disagreement with Burroughs is no longer "
  "about the creature's temperament but about where it stands: “This life form has not "
  "invaded our universe (as William Burroughs supposes) but is the source of our "
  "universe, one level higher.” {{BWV-LET-1981-07}}",

  "The letter closes the argument with an exclamation mark: “It is as if God spoke (or "
  "rather thought) a complex idea, and from this living idea (Logos) the universe came "
  "into being, was derived. This view is a far cry from Burroughs’ notion that we have "
  "been invaded by an information virus that is making us stupid!” {{BWV-LET-1981-08}} "
  "The same passage appears in the Exegesis at folio 91:19, so here the letter and the "
  "notebook are demonstrably one text. It is the last dated Burroughs reference in the "
  "archive.",

  "One undated document belongs beside it. Talking to Gregg Rickman — the interviews "
  "were made in Dick's last years — he sorts conspiracies into two kinds and files "
  "Burroughs under the wrong one: “An example is (William S.) Burroughs’ conviction "
  "about the parasitic information virus which has afflicted our minds and made us all "
  "stupid. They’ve taken over the planet. That’s cool.” He and Robert Anton Wilson, he "
  "says, prefer benign conspiracies — and then notes that a benign conspiracy is much "
  "harder to account for psychologically than a paranoid one {{BWV-INT-1981-01}}. It is "
  "the same judgement he posted to Warrick, said aloud and lightly.",
 ]},

 {"id": "fiction", "heading": "What is not there: the fiction", "register": "B", "body": [
  "Nowhere in the chronology above does a novel appear. That is not an omission. A "
  "full-text sweep of every work of Dick's fiction in this archive — A Scanner Darkly, "
  "the VALIS trilogy, The Man in the High Castle, The Unteleported Man, Do Androids "
  "Dream of Electric Sheep?, the collected stories, the Scanner screenplay — returns no "
  "reference to Burroughs, no allusion to his titles, and no use of his coinages. Every "
  "apparent match is ordinary English: “junkie” for a drug user, “cut up” in its literal "
  "sense.",

  "The traffic runs the other way. Where the Exegesis connects Burroughs to Ubik, The "
  "Three Stigmata of Palmer Eldritch, A Maze of Death, Flow My Tears and A Scanner "
  "Darkly, it is rereading finished books through one Dick encountered years after "
  "writing most of them. The closest thing to an exception is a phrase. Writing about "
  "Angel Archer's inability to pass from words to the non-verbal, he sets down “I am a "
  "word junky, a word disease” {{BWV-EXP-90-16A}} — in quotation marks, and the "
  "surrounding note suggests he is quoting his character rather than himself. The "
  "vocabulary is Burroughsian; the debt cannot be shown.",
 ]},

 {"id": "scholarship", "heading": "What the scholarship says", "register": "C", "body": [
  "Four sources in this archive engage the connection. Sutin's Divine Invasions (1989) "
  "supplies the biography already drawn on above, and three judgements besides: he uses "
  "a Burroughs anecdote to frame Ubik — “A student once asked William Burroughs if he "
  "believed in life after death. Burroughs asked back: How do you know you’re not dead "
  "already?” {{BWV-SCH-SUTIN-03}} — rates Dick's drug dialogue above Burroughs's own, "
  "which is “Vivid and sharp, but not the way it sounded at the time” "
  "{{BWV-SCH-SUTIN-04}}, and argues that the two late novels “were marketed as SF, but "
  "if, say, William Burroughs and Thomas Pynchon, respectively, had written them, they "
  "would have been mainstream” {{BWV-SCH-SUTIN-05}}.",

  "David Lapoujade's Worlds Built to Fall Apart offers the only sustained argument. He "
  "sets Dick's sentence about the manipulation of words beside Burroughs's “Word begets "
  "image and image is virus”, and concludes that “On this point, Dick is rather close to "
  "William S. Burroughs, for whom the words of a language are tools used for taking "
  "control of brains and taking over their ability to construct realities” "
  "{{BWV-SCH-LAPO-01}}. Then the causal claim: “This proximity between Dick and "
  "Burroughs stems in part from their readings of Alfred Korzybski” {{BWV-SCH-LAPO-02}}. "
  "This is worth flagging. The Dick sentence Lapoujade quotes is from the 1978 essay, "
  "where Dick credits Orwell {{BWV-ESS-1978-01}}, and this archive holds no direct "
  "evidence that Dick read Korzybski at all. A citation search of the full Exegesis and "
  "the Shifting Realities essays — for Korzybski, for general semantics, or for A. E. "
  "van Vogt, through whom Korzybski reached most science-fiction writers — would settle "
  "it. Lapoujade's reading is an argument; Dick's attribution is a fact; they should not "
  "be merged. Lapoujade also finds Burroughs behind Dick's proliferating trash "
  "{{BWV-SCH-LAPO-03}}, his drugs {{BWV-SCH-LAPO-04}} and his bureaucracies "
  "{{BWV-SCH-LAPO-05}}.",

  "Andrew M. Butler compares the Author's Note of A Scanner Darkly to “William S "
  "Burroughs’ testimony about his own sickness and the word to the wise which forms a "
  "health warning to _Naked Lunch._” {{BWV-SCH-BUTLER-01}} And the published Exegesis "
  "carries its editors' own verdict: Burroughs's “notions of reality as a control system "
  "and language as an extraterrestrial virus clearly resonated with Dick, who, in 1978, "
  "experimented with the cut-up method” {{BWV-EXP-90-6A}} — more confident than anything "
  "Dick says about himself, and, in the same sentence, wrong about Brion Gysin's "
  "nationality.",

  "Beyond these, nothing. Kripal, Erik Davis's TechGnosis, Jameson, Spinrad, the Essays "
  "of the Here and Now collection and Anne R. Dick's memoir all mention Burroughs "
  "without connecting him to Dick, and several apparent hits are Edgar Rice Burroughs. "
  "Erik Davis's much-reprinted jacket line — “If the ’70s and ’80s…belonged to William "
  "Burroughs, the millennium belongs to Philip K. Dick.” {{BWV-REC-DAVIS-01}} — is "
  "reception, not analysis.",
 ]},

 {"id": "synthesis", "heading": "What Burroughs meant to Dick", "register": "D", "body": [
  "Burroughs gave Dick one thing, and it was not an idea he adopted. It was a hypothesis "
  "precise enough to be wrong in an interesting way.",

  "Laid out in order, the five years have a shape the thematic version obscures. January "
  "1976: a name on a publisher's wish list, unknown to him. September 1976: the book "
  "arrives through Jeter, is accepted wholesale, and is rewritten the same afternoon "
  "into its opposite — not information that infects but a block on reception. 1977 to "
  "1978: the cut-up gets a theology and the impairment gets its sharpest statement. "
  "Autumn 1980, the months before VALIS: four incompatible readings in four months, none "
  "discarded. April 1981: the position stated cleanly to a stranger and abandoned in his "
  "own notebook the next day. August 1981: the argument closed with an exclamation mark.",

  "What the archive does not show is a man converted, and it does not show a man "
  "dismissing a source. It shows a five-year argument with a book in which the "
  "opponent's terms are never given up. Dick is still saying “information virus” in the "
  "sentence where he denies there is one.",

  "The portal's reading, offered as such: what Burroughs supplied was a question that "
  "could be asked at all. Once you can say the world is a signal and something is "
  "interfering, you can ask which side the signal is on. Dick asked for five years and "
  "returned different answers, and then saw why the asking might be hopeless — that a "
  "mind inside the occlusion cannot verify its own account of the occlusion "
  "{{BWV-LET-1981-06B}}. He took that not as a defeat but as a design brief, and wrote "
  "VALIS. The honest form of this topic is the disagreement, not a resolution of it.",
 ]},
]
