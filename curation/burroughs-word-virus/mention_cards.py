#!/usr/bin/env python3
"""
Reader-facing card for every Burroughs mention.

Each card carries:
  * `context` — editorial summary of the whole passage and where it sits in the
    work. Portal-editor prose (register D), written from the full passage.
  * `pith`    — a short verbatim quotation of the sentence the passage turns on.
  * `speaker` — who is being quoted, so a biographer's sentence is never mistaken
    for Dick's.

The pith strings are machine-verified against the extracted passage text by
`scripts/studies/seed_burroughs_word_virus.py`, which refuses to seed if any
quotation is not verbatim. Transcription irregularities are preserved exactly as
they stand in the source.

Imported by build_inventory.py.
"""

PKD = 'Philip K. Dick'

# id: (context, pith, speaker)
CARDS = {

    # ---- Exegesis, 15 September 1976 -----------------------------------
    'BWV-EX-1976-01': (
        "Dick's first recorded sitting with The Ticket That Exploded. He is reading "
        "Burroughs's account of the Nova Mob — parasites who move from one human host "
        "to another and give themselves away by keeping the same habits — and testing "
        "it directly against Thomas, the personality he believes took him over in 3-74. "
        "Within a few lines the borrowed apparatus has become an account of his own "
        "body: he describes feeling himself a womb into which something was deposited "
        "like a cuckoo's egg. The question he arrives at is not literary but factual.",
        "Does this mean that burroughs is either intentionally or unintentionally "
        "describing something which is true?", PKD),

    'BWV-EX-1976-02': (
        "The word virus stated in its compact form, followed immediately by what Dick "
        "did next: he put Burroughs down and opened Ubik. The passage is where he first "
        "entertains the thought that the two of them are reporting rather than "
        "inventing — that both novels have, as he puts it, a strange ring of revealed "
        "truth. He is also already reaching for Palmer Eldritch as a parasite "
        "replicating himself through human hosts.",
        "Burroughs speaks of a virus - a word become a neural - cell virus, infecting "
        "us.", PKD),

    'BWV-EX-1976-03': (
        "The decisive modification, made in the same sitting as the adoption. Having "
        "accepted the diagnosis, Dick reverses the mechanism: the virus does not carry "
        "information into us, it prevents information reaching us, and substitutes "
        "counterfeit signal for the true. He glosses it at once with the erased "
        "instruction tape in A Maze of Death — the recording that would have told the "
        "characters what they were for, wiped. Everything he says about Burroughs for "
        "the next five years follows from this sentence.",
        "The virus (of Burroughs) is an information (or word) virus, but in this sense: "
        "it blocks to reception of information. So it is an anti-information virus.",
        PKD),

    'BWV-EX-1976-04': (
        "Working through how the jamming would actually operate, with K. W. Jeter (\"Kw\") "
        "supplying observations. The visual channel is blocked at the level of "
        "set/ground discrimination; the auditory channel by subvocal chatter, for which "
        "Burroughs supplies the evidence that inner silence cannot be held for ten "
        "seconds. Dick converts that from a fact about attention into a deliberate "
        "override, and casts Hagia Sophia as a transmitter trying to reach us from "
        "behind enemy lines.",
        "There is an inner raving, howling, clamaring bug, which deliberately creates "
        "derogatory noise on the line at all times.", PKD),

    'BWV-EX-1976-05': (
        "A theological aside in which Burroughs's cosmology is folded into the problem "
        "of why God permits evil. Dick is working with the idea of a world that tests "
        "its inhabitants — the \"teaching machine\" model — and notes that Burroughs's "
        "concealed hostile entities fit the same structure as the gospel parable of "
        "Christ unrecognised in the poor.",
        "all this fits in with the theory (Burroughs' included) that this world contains "
        "evil entities wearing ordinary human semblance", PKD),

    'BWV-EX-1976-06': (
        "The passage that turns Burroughs into autobiography. Dick names the book, "
        "summarises its thesis — the criminal virus related to words, submessages, the "
        "nova police — and then reads 3-74 as a temporary cure rather than a revelation. "
        "The paragraph ends with the darker half: the remission did not hold. Note the "
        "medical vocabulary that surrounds it, the Asklepios dream and the \"aspirin of "
        "mercury\", and that he suspects the healing was done to him rather than by him.",
        "what happened to me in 3-74 is that I temporarily got well - was somehow able "
        "to throw off the word virus which had entered me + infected me", PKD),

    'BWV-EX-1976-07': (
        "Dick assigns the two sides of the Burroughs cosmology to the two sides of his "
        "own. The enemy he says he knows little about; the power that intervened he "
        "identifies with the cosmic Christ — and then, flatly, with Burroughs's police "
        "force. The same paragraph brings in Robert Anton Wilson on Sirius and the "
        "surgical implanting of Firebright, and states the planetary scale of the "
        "infection.",
        "the sentient power which took complete control of me is connected with the "
        "cosmic Christ, a healer + wise entity. Equal to Burroughs' nova police.", PKD),

    'BWV-EX-1976-08': (
        "A model of how a partial world gets completed by its inhabitants: we receive a "
        "bare-bones transmission and fill in the rest ourselves, as Ragle Gumm does in "
        "Time Out of Joint, so that the counterfeit world is substantially our own "
        "projection. Dick offers this as the explanation for why Burroughs's cut-up "
        "experiments turn up messages at all — they are latent because we are the ones "
        "supplying the surface.",
        "This would explain Burroughs' results in obtaining living, latent messages "
        "normally passing us by.", PKD),

    'BWV-EX-1976-09': (
        "One of the strangest turns in the 1976 material: Dick casts himself as the "
        "quarry rather than the patient. Stanislaw Lem, with whom he was then in "
        "conflict, becomes one of the \"brittle moralistic\" police; Dick's defence is "
        "that his writing is already dispersed beyond recall. The passage moves through "
        "Zagreus and Dithyrambus, and treats the 1971 \"Taco Stand\" vision as evidence "
        "of a world-generating faculty he has since lost.",
        "Burroughs is right about the Nova police + their tracking down their quarry.",
        PKD),

    'BWV-EX-1976-10': (
        "The Nova police material recombined into a figure Dick uses repeatedly — the "
        "agent who must not know he is an agent. Amnesia is not a misfortune here but "
        "an operational requirement: the cop can only reach the interior of the prison "
        "because he cannot give himself away. It is the plot of A Scanner Darkly stated "
        "as cosmology, and Dick applies it to himself as \"2 people\", PKD and Thomas.",
        "he's a cop tracking down some evil (enslaving BIP) criminals - shades of "
        "Burroughs' nova Mob + the Nova police whom come after them! A cop with amnesia.",
        PKD),

    'BWV-EX-1976-11': (
        "Dick is trying to explain why the Rome he saw superimposed on 1974 California "
        "is invisible to everyone else, and settles on concealment as a survival trait — "
        "which makes the thing that conceals itself an organism with a life cycle. He "
        "takes Burroughs's replicating virus as the nearest available model while "
        "insisting on his own refinement: it works as Gestalt, as shaping, not as "
        "substance.",
        "This fits the \"replicating virus\" theory of Burroughs - I would say as "
        "Gestalt, as shaping (+ certainly as functioning). It has a life cycle of sorts. "
        "It is an organism.", PKD),

    'BWV-EX-1976-12': (
        "The most structurally explicit of the 1976 entries. Dick has arrived at two "
        "transtemporal organisms in permanent combat, each able to infiltrate objects, "
        "processes and people, and recognises the shape as Burroughs's. He then extends "
        "it: the messages are not addressed to us at all but are one distributed mind "
        "keeping its own parts informed, with human beings as nerve fibres — which is "
        "how he explains what Flow My Tears was doing.",
        "This is very much like Burroughs' formulation (the Nova Mob vs the pursuing "
        "Nova police - + he has the latent message theory, too).", PKD),

    'BWV-EX-1976-13': (
        "Where the borrowed virus becomes Dick's own vocabulary. Starting from the word "
        "KING FELIX seen charged with red and gold plasmic energy, he argues that an "
        "organism could reproduce as information, notes Burroughs's version — and "
        "records Jeter's dissent in parenthesis. The term \"living information\", and its "
        "identification with the Logos, arrives here.",
        "If that plasmic energy is alive, + it is (or it carries) information, then we "
        "have living information. Logos?", PKD),

    # ---- Exegesis, 10 October 1978 --------------------------------------
    'BWV-EX-1978-01': (
        "Two years on, Dick is reading 3-74 as a detoxification — something poisonous "
        "flushed from his nervous system — and connects it to the mercury he believes he "
        "ingested lifelong. The endorsement of Burroughs is put in the strongest terms "
        "he ever uses, and it settles a specific question: whether human faculties are "
        "impaired or merely undeveloped. He chooses impaired, and calls the condition a "
        "curse.",
        "Then it is evident that our proper full functioning is impaired, rather than "
        "just not (yet) achieved. Then we are \"cursed.\" William Burroughs is correct.",
        PKD),

    'BWV-EX-1978-02': (
        "The passage that most complicates the standard account. Working from The Three "
        "Stigmata of Palmer Eldritch and transubstantiation, Dick keeps the phrase "
        "\"information virus\" but reverses its sign entirely: the virus is Zebra, and it "
        "is the cure. He then maps the benign version onto four of his own novels — it "
        "abolishes the counterfeit world (Flow My Tears, A Maze of Death), lifts the "
        "inner occlusion (A Scanner Darkly), breaks astral determinism (The Electric "
        "Ant) and restores memory (Impostor). This is three years before the entry "
        "usually read as his reversal.",
        "But this is not an occluding, toxifying \"virus\" - it is an antitoxic, "
        "de-occlusive.", PKD),

    'BWV-EX-1978-03': (
        "Dick is trying to account for how the Acts material and the Bacchae "
        "superimposed themselves in Flow My Tears without his intending it, and reaches "
        "for randomness as a mechanism — the monkeys-with-typewriters image alongside "
        "Burroughs's cut-ups. What interests him is the timing: the superimposition was "
        "published in the same month as a parallel event in a real life, which he takes "
        "as pointing to a common source rather than to cause and effect.",
        "Imagine a random sentence generator (as in \"Fifty million monkeys\" or william "
        "Burroughs' latent message stuff)", PKD),

    'BWV-EX-1978-04': (
        "The most quoted of Dick's assessments, and the most balanced. He is arguing "
        "that the Acts material in Flow My Tears was self-generating, and that the KING "
        "FELIX cipher is the same kind of tracing — information that is alive or "
        "semi-alive. Burroughs is credited with the insight and denied the whole of it "
        "in the same clause. The passage ends by calling 3-74 a double miracle: an "
        "acausal event, and then acausal information explaining it.",
        "this information is alive or semi-alive like a virus; Burroughs is right but he "
        "has only a bit of the whole picture", PKD),

    'BWV-EX-1978-05': (
        "Dick auditing the provenance of one of his own convictions — rare, and worth "
        "the attention. He has held for years that the plasmate's messages were a "
        "contamination; here he abandons the view and names its two sources, one of them "
        "Burroughs's theory and the other his own fear. He replaces it with an inner "
        "occluding agent, the DNA, and with the reading of Flow My Tears as a message "
        "telling us we are imprisoned.",
        "I doubt very much if the plasmate is an occluding agent (like Burrough's "
        "information virus).", PKD),

    'BWV-EX-1978-06': (
        "The pessimistic pole, written in the same section as the passage that calls the "
        "virus a cure. Dick is asking what the \"stolen secret\" of his visionary material "
        "actually was, and the answer he gives — with visible reluctance — is Burroughs's. "
        "He then wonders whether the occluding life form might be the plasmate itself, "
        "the entity he elsewhere treats as the remedy, and turns to Paul's hostility to "
        "the Torah for corroboration.",
        "there is an occluding life form here; it not only occludes us, but it enslaves "
        "us and Kills us.", PKD),

    'BWV-EX-1978-07': (
        "Dick's account of how a sacred narrative could replicate itself in newly "
        "generated information without anyone intending it — Acts appearing in microform "
        "inside texts written by people who do not know they are Christians. He credits "
        "Burroughs with the discovery and takes the interpretation away from him in the "
        "same breath: the same phenomenon, read as the ground of being rather than as an "
        "infection.",
        "This is what William Burroughs discovered (but interprets differently).", PKD),

    'BWV-EX-1978-08': (
        "A passage about method rather than doctrine, and one of the few places Dick "
        "names a Burroughs title other than The Ticket That Exploded. He has been "
        "arguing that the Kingdom is disclosed rather than found — the stone rejected by "
        "the builder, the fly grooming itself — and concludes that systematic philosophy "
        "is the wrong instrument for it. Junky is the right one because it is testimony, "
        "not argument.",
        "Ponderous books of philosophy won't help me; Burroughs' \"Junky\" will.", PKD),

    'BWV-EX-1978-09': (
        "A third position, again in the same section, and it discards the frame "
        "altogether. Dick is on the Parousia — the announcement has been made and nobody "
        "has noticed — and insists that his repeated cry of \"I am no longer blind\" was "
        "literal rather than figurative. If the problem is blindness there is nothing to "
        "throw off, and the diagnosis becomes enchantment: the work of a magician, the "
        "private worlds of Eye in the Sky.",
        "We're under a spell. This is no information virus; this is blindness.", PKD),

    'BWV-EX-1978-10': (
        "The most literal-minded version Dick ever gives. Asking what Ubik actually is, "
        "he answers: an occult information-processing entity riding the media — and then "
        "puts it in the Cold War, as Soviet psychotronic research escaped from its "
        "makers. The question mark is his. In the same breath he identifies Ubik, Valis, "
        "the macrometasomakosmos and the \"second signal\" as one thing.",
        "Some kind of living information (Burrough's information virus) got away from "
        "the Soviets + is replicating as a life form?", PKD),

    'BWV-EX-1978-11': (
        "A compressed note listing four aspects of information processing — linking, "
        "rest-motion, set-ground discrimination, and message collages assembled by "
        "whatever happens to be juxtaposed — and connecting all four to Burroughs. The "
        "entry ends on the word Dick is reaching for: syntax. Valis can extract meaning "
        "because it can perceive syntax where we cannot.",
        "This is related to william Burroughs latent messages + info virus.", PKD),

    # ---- Exegesis, 16 April 1981 ----------------------------------------
    'BWV-EX-1981-01': (
        "Written on Good Friday. Dick has the Black Iron Prison and the Palm Tree Garden "
        "set against each other as Satan and Christ, and reaches for Calvin — not "
        "Burroughs — as the authority on occlusion, with Burroughs added as a secondary "
        "witness. The self-assessment matters: he takes the occlusion in A Scanner "
        "Darkly as having been correct, and lists what is occluded as perception, "
        "cognition and memory.",
        "Then there is an occlusion, as Calvin says. And only Christ can lift the "
        "occlusion. Burroughs, too, in his own way is right. I was right when I wrote "
        "SCANNER.", PKD),

    'BWV-EX-1981-02': (
        "The reversal, stated as plainly as Dick ever states anything. The angelic powers "
        "keep humanity ignorant by occluding its faculties; living information is the "
        "countermeasure sent to break the news, and its message is KING FELIX. He then "
        "diagnoses Burroughs's error precisely — not the observations but the arrow "
        "between them — and identifies the mistake as a genre habit, the secret-invasion "
        "plot. The paragraph still ends by conceding that Burroughs is onto the truth.",
        "Man is not occluded by an \"information virus,\" i.e. living information; on the "
        "contrary: man is occluded and the living information is sent to tell him the "
        "true situation", PKD),

    'BWV-EX-1981-03': (
        "Written in the same sitting as the reversal, and it keeps the occluding virus — "
        "transferred from Burroughs's information to the Torah. Reading the ending of "
        "The Divine Invasion, Dick has Torah take the role of Fate, the book of the "
        "spinners, and collapses Torah, living information, programming, fate and world "
        "into one thing. Christ overcomes it by overcoming causation itself.",
        "Thus Torah assumes the role of Fate: \"the book of the spinners\". It programs + "
        "controls us. So it is like an occluding information virus; it keeps us enslaved "
        "at the level of machines.", PKD),

    'BWV-EX-1981-04': (
        "Dick's attempt to hold both readings at once, and the nearest thing to a "
        "resolution in the 1981 material. The occluding virus is not denied; it is "
        "invaded in turn by a second, living information he associates with Christ's "
        "blood. The result is a combat between frozen and living information conducted "
        "below the level of the physical universe, since on his account information is "
        "ontologically prior to matter.",
        "as the \"information virus\" controls + occludes + enslaves us, it itself has "
        "been penetrated by a living hyper-information (which I associate with Christ's "
        "sacrificial blood).", PKD),

    'BWV-EX-1981-05': (
        "Dick anticipating his own readers. He expects the Burroughs parallel to be "
        "noticed in VALIS, concedes the resemblance — an information life form standing "
        "between us and reality — and then marks the distance in five words. The lineage "
        "he claims is gnostic, not Beat; Valentinus, not Burroughs.",
        "Someone in reading \"Valis\" will see the correlation to Burroughs.", PKD),

    'BWV-EX-1981-06': (
        "An unusually self-referential passage. Dick argues that VALIS was split into "
        "dual messages by the very thing it describes, which he takes as the book "
        "verifying its own thesis. Burroughs, on his account, missed the scale of it: "
        "the virus does not merely infect a world, it manufactures one. The claim is "
        "grounded in something small and concrete — watching the I Ching work the night "
        "before.",
        "Burroughs never guessed this: his info virus creates a whole spurious universe "
        "for us - but in 3-74 I saw it as it is", PKD),

    'BWV-EX-1981-07': (
        "The darkest passage in the dossier, and it is Manichaean rather than gnostic. "
        "Dick has decided that what he saw in 3-74 was beautiful on purpose — beauty as "
        "enchantment, designed to beguile and cause forgetting, which he identifies as a "
        "major theme of The Divine Invasion. Burroughs's virus becomes the instrument by "
        "which Satan tempted Christ and deflected him from waking humanity.",
        "he ensnared him as the info virus of Burroughs, ensnared him with beauty. So: "
        "Manichaenism, Burroughs + the story of Satan (world) tempting Christ.", PKD),

    'BWV-EX-1981-08': (
        "Dick naming the framework that finally displaces Burroughs. Reading Hans Jonas "
        "on Manichaeism gave him a structure he judges more radical ontologically — not "
        "an invasion of the world but a doubt about whether the world is there at all. "
        "The vocabulary that follows is Jonas's: beguiling, entrapment, ensnaring, "
        "engulfing on one side; error, ignorance, sleep, intoxication and forgetfulness "
        "on his own.",
        "This very slightly resembles Burroughs, but is much more radical (ontologically "
        "speaking).", PKD),

    'BWV-EX-1981-09': (
        "Dick's radical acosmism, arrived at after watching the I Ching do what he had "
        "seen the plasmate do in 3-74. Living information is divine, and so is he — and "
        "it still controls us, on Burroughs's authority, while wearing the world as a "
        "disguise. The passage ends with the reversal of appearances that governs the "
        "late work: the enslaver appears beautiful, Christ appears as trash and pain.",
        "This living info is divine but so am I. + it controls us (as Burroughs teaches); "
        "more, it assumes the guise of [being a] world", PKD),

    'BWV-EX-1981-10': (
        "The cut-up method given a theological cause. Dick is working out how Hagia "
        "Sophia and the Torah function together in creation: if she reads the book "
        "aloud, that reading is the world. It follows that any fragment of text is "
        "already inside the narration — which is why, he reasons, Burroughs's "
        "randomised texts produce narrative rather than noise. He connects it to a dream "
        "of galley pages bearing a message about a writer in Marin County.",
        "This is why -as William Burroughs found- when any written text is cut up + "
        "rejoined at random, a narrative results.", PKD),

    # ---- Letters ---------------------------------------------------------
    'BWV-LET-1976-01': (
        "The earliest Burroughs reference in the archive, and it is about business, not "
        "ideas — eight months before Dick reads him. Doubleday planned to Xerox the "
        "manuscript of A Scanner Darkly and send it to literary figures with standing "
        "among college readers, and left Dick to make the approaches. His difficulty, "
        "stated plainly to a friend, is that he knows no one outside science fiction, "
        "and that Doubleday does not want the novel read by anyone inside it.",
        "They want people like William Burroughs, Kurt Vonnegut—all the counterculture "
        "cult heroes to read it.", PKD),

    'BWV-LET-1976-02': (
        "The same problem, put to his agent on the same day. Lacking access to the "
        "writers Doubleday wants, Dick falls back on review quotations, and copies out "
        "one from Oui that pairs him with Burroughs. The comparison is the magazine's, "
        "not his — worth noting, since it is the earliest instance of the pairing in the "
        "archive and it circulated for years, reappearing in the fanzine PKD Otaku.",
        "In many ways, Phil Dick is to psychedelics and science fiction what William "
        "Burroughs is to hard drugs and mainstream literature.", 'Oui, quoted by PKD'),

    'BWV-LET-1979-01': (
        "Dick thanking the editor of Rolling Stone College Papers for the first issue, "
        "which carried his story \"Strange Memories of Death\" alongside an article on "
        "Burroughs and an interview with him. The remark is the only place in the "
        "archive where Dick claims the Beat affiliation for himself, and he does it in "
        "passing, as a reason the two pieces sit well together.",
        "his interview leads right into my story inasmuch as he discusses the rebellion "
        "during the Fifties and the Beats, of which I was one.", PKD),

    'BWV-LET-1981-01': (
        "Advice to a beginning writer, and a rare direct statement of whom Dick thought "
        "worth reading. The list is short and entirely outside science fiction. The "
        "surrounding counsel is practical to the point of bluntness — write what you "
        "know, keep a journal, ignore negative criticism — which is the register in "
        "which Burroughs appears here: as a working model of prose, not as a theorist.",
        "read the great prose writers: Faulkner, Hemingway, Hunter S. Thompson, "
        "William Burroughs, Saul Bellow, Herbert Gold.", PKD),

    'BWV-LET-1981-02': (
        "Written to the fanzine editor Richard E. Geis while Dick was defending VALIS "
        "against the charge of being simply autobiography. He works through the problem "
        "of the first person by way of Henry Miller, then states what he was actually "
        "attempting: an old form, the picaresque, carrying modern voices. Burroughs is "
        "named as a source of the prose, alongside Hunter S. Thompson and his own A "
        "Scanner Darkly — the only forward-running debt Dick ever claims.",
        "a new kind of blending of the ancient picaresque form with certain modern "
        "elements associated with Hunter S. Thompson and William S. Burroughs", PKD),

    'BWV-LET-1981-03': (
        "Three days later, the same account to the scholar Patricia Warrick, with the "
        "politics attached. Dick has been in conflict with Ursula K. Le Guin and with "
        "Lem, and frames his own work as protest art set against official culture — which "
        "is what the vernacular in VALIS is for. The Burroughs debt is stylistic and "
        "specific, and it sits inside a description of VALIS as a novel about madness and "
        "God told by a madman with whom Dick identifies.",
        "It is a picaresque novel blended with new elements derived from William "
        "Burroughs, Hunter S. Thompson", PKD),

    'BWV-LET-1981-04': (
        "The opening of the most important document in the dossier: Dick's reply to a "
        "correspondent named Brig Elliot, written on 15 April 1981, one day before the "
        "Exegesis entry that states the reversal. He confirms what he has read and what "
        "he understands by it — and then dates his own observation of the phenomenon to "
        "1971, before he knew of Burroughs, which is the single strongest piece of "
        "evidence against reading A Scanner Darkly as Burroughs-influenced.",
        "Back in 1971 before I knew of Burroughs I noted a thinking dysfunction or "
        "occlusion in people involved with drugs; I deal with this in A SCANNER DARKLY.",
        PKD),

    'BWV-LET-1981-05': (
        "The fairest sentence Dick ever wrote about anyone he disagreed with. He has "
        "just described a dysfunction in which the self-monitoring circuit is itself "
        "compromised — so the impairment cannot notice itself — and turns to Burroughs's "
        "explanation. He declines it and refuses to dismiss it in the same breath, then "
        "separates the two things that can be judged separately: the description of the "
        "problem, and the account of its cause.",
        "he states the problem correctly, although perhaps his analysis of the cause is "
        "faulty; still, merely to be aware of the problem is to achieve a great deal",
        PKD),

    'BWV-LET-1981-06': (
        "Later in the same letter, and this is where the disagreement is named. Dick has "
        "found accounts of occlusion in ancient sources — the Cave of Treasures, Adam "
        "deprived of his bright nature, Calvin as quoted in the VALIS tractate — and "
        "argues that if the condition exists it is very old, which removes the need for "
        "an invasion. The difference is then reduced to a single question of valence, "
        "with a third possibility left open: that the information life form has no "
        "interest in us either way and merely rides our traffic.",
        "it is benign; it does not occlude us; on the contrary: it informs us", PKD),

    'BWV-LET-1981-07': (
        "Four months later, to Patricia Warrick, and the formulation has hardened into "
        "metaphysics. Dick corrects his own line in VALIS that the universe consists of "
        "information: what he should have said is that rolling the universe back to its "
        "ontological source yields the Word or Torah. The disagreement with Burroughs is "
        "no longer about whether the information life form is friendly but about where it "
        "stands — not an invader from outside but the level above.",
        "This life form has not invaded our universe (as William Burroughs supposes) but "
        "is the source of our universe, one level higher", PKD),

    'BWV-LET-1981-08': (
        "The last dated Burroughs reference in the archive, at the close of the same "
        "letter. Dick describes the meta-abstraction by which he says he rolled the "
        "physical universe back to the Uttered Word, arriving at \"word\" as the right "
        "translation of Logos — and then measures the distance from Burroughs in a "
        "single sentence, with an exclamation mark. Language is the origin of the world, "
        "not the parasite on it.",
        "This view is a far cry from Burroughs’ notion that we have been invaded by an "
        "information virus that is making us stupid!", PKD),

    # ---- Interview and essay ---------------------------------------------
    'BWV-INT-1981-01': (
        "The only interview in the archive where Dick discusses the word virus, and the "
        "tone is entirely different from the notebooks: relaxed, and slightly amused. "
        "Talking to Gregg Rickman about Chesterton's The Man Who Was Thursday, he "
        "distinguishes his own taste in conspiracy from the ordinary kind, and files "
        "Burroughs firmly under the ordinary kind. He and Robert Anton Wilson, he says, "
        "prefer benign conspiracies — and then notes that this is much harder to explain "
        "psychologically than paranoia.",
        "the parasitic information virus which has afflicted our minds and made us all "
        "stupid. They’ve taken over the planet. That’s cool.", PKD),

    'BWV-ESS-1978-01': (
        "From the 1978 essay, published in Dick's lifetime, in which he defines reality "
        "as that which does not go away when you stop believing in it. The surrounding "
        "argument is about manufactured pseudo-worlds delivered by media into the heads "
        "of viewers, and about how much of television is received subliminally. It is "
        "his clearest statement that language is the instrument of control — and the "
        "authority he cites is Orwell, not Burroughs. Lapoujade reads this passage as "
        "Dick's proximity to Burroughs; Dick's own attribution says otherwise, and both "
        "belong on the record.",
        "The basic tool for the manipulation of reality is the manipulation of words. If "
        "you can control the meaning of words, you can control the people who must use "
        "the words.", PKD),

    # ---- Biography and scholarship ---------------------------------------
    'BWV-SCH-SUTIN-01': (
        "The single most useful paragraph of biography in the dossier. Sutin describes "
        "K. W. Jeter's role after the two men resumed their friendship in late 1976: "
        "unpersuaded by Dick's religious theories but willing to complicate them. It is "
        "Jeter who supplies the Burroughs parallel — which identifies the \"KW\" credited "
        "throughout the September 1976 Exegesis entries — and Jeter with whom Dick "
        "actually performed a cut-up experiment, on Moby Dick, Roderick Thorp's The "
        "Detective, and the Book of Acts. That last text is the one Dick elsewhere "
        "insists generated itself in Flow My Tears.",
        "He called attention to the similarities between Phil’s novels and those of "
        "William Burroughs-such as an invading alien virus occluding human faculties "
        "(for Burroughs, the virus is language).", 'Lawrence Sutin'),

    'BWV-SCH-SUTIN-02': (
        "Sutin placing Burroughs among Dick's reading, in a list that runs from physics "
        "papers to the Bhagavad Gita by way of Binswanger. The passage is evidence for "
        "breadth, not for chronology: no date is attached, and it sits beside Sutin's "
        "note that Dick would name Stendhal, Flaubert and Maupassant before any science "
        "fiction writer when asked about influence. It should be read against Dick's own "
        "statement that he did not know Burroughs in 1971.",
        "Throughout his life the range of his reading was virtually limitless, from "
        "technical papers on physics to Binswanger’s daseinanalyse to Jung, Kant, "
        "William Burroughs, the Bible, the Dead Sea Scrolls, the Bhagavad Gita.",
        'Lawrence Sutin'),

    'BWV-SCH-SUTIN-03': (
        "Sutin using Burroughs to frame Ubik — the biographer's comparison, not Dick's. "
        "The context is Runciter's graffito and the impossibility of knowing which side "
        "of the half-life boundary anyone is on, including Runciter himself. Sutin's "
        "point is that the novel declines to answer, and that Ubik itself, hard to come "
        "by and requiring something like faith, is what is offered instead of an answer.",
        "A student once asked William Burroughs if he believed in life after death. "
        "Burroughs asked back: How do you know you’re not dead already?",
        'Lawrence Sutin'),

    'BWV-SCH-SUTIN-04': (
        "A judgement on style, and it goes against Burroughs. Discussing the antidrug "
        "theme of A Scanner Darkly — and Dick's 1973 offer of assistance to the "
        "Department of Justice — Sutin argues that Dick captured sixties drug dialogue "
        "more accurately than Burroughs did in The Soft Machine and The Wild Boys, and "
        "illustrates it with Ernie Luckman's scheme for smuggling hashish carved into "
        "the shape of a man.",
        "William Burroughs employs a junkie patois that is part forties Times Square, "
        "part private eye, part laconic Beat Burroughs. Vivid and sharp, but not the way "
        "it sounded at the time.", 'Lawrence Sutin'),

    'BWV-SCH-SUTIN-05': (
        "Sutin on the cost of genre classification, with Burroughs as the control case. "
        "The argument is that the same books would have been received as literature "
        "under different names, and it is followed by a Borges example running the other "
        "way — \"Tlön, Uqbar, Orbis Tertius\" would have been shelved as science fiction "
        "had Dick written it.",
        "They were marketed as SF, but if, say, William Burroughs and Thomas Pynchon, "
        "respectively, had written them, they would have been mainstream.",
        'Lawrence Sutin'),

    'BWV-SCH-LAPO-01': (
        "The core of the only sustained scholarly treatment in the archive. Lapoujade "
        "has been arguing that for Dick the left hemisphere is dedicated to the "
        "programming of the psyche, the brain becoming a servo-mechanism shaped by "
        "linguistic and numeric algorithms. He quotes Dick's \"How to Build a Universe\" "
        "passage and sets Burroughs beside it, with the line from Nova Express — word "
        "begets image, and image is virus.",
        "On this point, Dick is rather close to William S. Burroughs, for whom the words "
        "of a language are tools used for taking control of brains and taking over their "
        "ability to construct realities.", 'David Lapoujade'),

    'BWV-SCH-LAPO-02': (
        "Lapoujade's causal claim, and the most contestable thing on this page. Having "
        "established the resemblance, he explains it as convergence rather than "
        "influence: both men read Korzybski, whose general semantics describes how "
        "language imposes bivalent Aristotelian logic on analogical experience. The "
        "archive holds no direct evidence of Dick reading Korzybski, and the passage "
        "Lapoujade quotes credits Orwell — so this belongs in the register of scholarly "
        "argument, not established fact.",
        "This proximity between Dick and Burroughs stems in part from their readings of "
        "Alfred Korzybski", 'David Lapoujade'),

    'BWV-SCH-LAPO-03': (
        "Lapoujade on proliferating artifacts — simulacra, androids, the synthetic "
        "animals of Do Androids Dream of Electric Sheep?, Molinari's spare bodies in Now "
        "Wait for Last Year — and the moment where copies stop being copies and become "
        "the world. The Burroughs comparison is doing specific work: it supplies the "
        "mechanism by which junk spreads, and the sickness it carries with it.",
        "As in Burroughs, the “trash” has the propagative power of a virus",
        'David Lapoujade'),

    'BWV-SCH-LAPO-04': (
        "Lapoujade on drugs as an instrument of control rather than of escape, following "
        "from his argument that whoever controls the transmission of information controls "
        "what gets called reality. He reads The Three Stigmata of Palmer Eldritch as the "
        "clearest case: two drugs sold by two dealers described as rival divinities, one "
        "of them offering a communion that delivers its users into a standardised world.",
        "There are no soft drugs in Dick. There are only hard drugs that attack the "
        "brain directly and take control of it, as in Burroughs.", 'David Lapoujade'),

    'BWV-SCH-LAPO-05': (
        "A structural parallel drawn from Naked Lunch rather than from the Nova trilogy. "
        "Lapoujade distinguishes the analogical, which circulates between worlds, from "
        "the digital, which is sealed inside its own codes, and finds Dick arriving "
        "independently at Burroughs's opposition between cooperatives, which create, and "
        "bureaucracies, which can only graft themselves onto what already exists, in the "
        "manner of a tapeworm.",
        "Dick rediscovers the distinction between cooperatives and bureaucracies that "
        "Burroughs established in _Naked Lunch_", 'David Lapoujade'),

    'BWV-SCH-BUTLER-01': (
        "Butler reading the Author's Note of A Scanner Darkly, in which Dick describes "
        "drug users as children punished for playing, and includes himself among them. "
        "The comparison is to the prefatory testimony Burroughs attached to Naked Lunch "
        "— the addict's account of his own sickness, offered as a warning. Butler's point "
        "is that Dick's novel is neither an anti-drug tract nor an advertisement, and the "
        "Burroughs parallel is what lets him say so.",
        "Compare this to William S Burroughs’ testimony about his own sickness and the "
        "word to the wise which forms a health warning to _Naked Lunch._",
        'Andrew M. Butler'),

    'BWV-REC-DAVIS-01': (
        "Reception rather than argument, and included because it shows what the pairing "
        "came to mean after Dick's death. Erik Davis's line, written for Details, was "
        "picked up as a jacket endorsement and reprinted for years — here on an edition "
        "of Do Androids Dream of Electric Sheep?, and again in the fanzine Simulacrum "
        "Meltdown. Burroughs functions in it as the writer against whom Dick's stature "
        "is measured: a succession, not an influence.",
        "If the ’70s and ’80s…belonged to William Burroughs, the millennium belongs to "
        "Philip K. Dick.", 'Erik Davis'),

    # ---- Published Exegesis: folios absent from our transcriptions -------
    'BWV-EXP-15-100': (
        "Folio 15:100, and the passage that ties the cut-up method to everything else "
        "in the late work. Dick is asking whether the latent story inside Flow My Tears "
        "is a kind of living DNA guiding an entelechy through its growth, and reaches "
        "for Bateson's immanent mind — the mind that narrates information to each "
        "living thing. The novel becomes an incised form bearing the bench marks of "
        "whatever fashioned him, read the way one reads tea leaves or entrails, with "
        "Burroughs's method cited as the precedent for extracting latent meaning. It "
        "ends in the eucharist: the text as wafer, the reader as host.",
        "(Cf. Burroughs' cut-up message pieces latent meaning-extraction method.) This "
        "being replicates itself through—as—information.", PKD),

    'BWV-EXP-19-35': (
        "Folio 19:35, and the most exact account Dick ever gives of why the impairment "
        "cannot notice itself. Derange the brain in precisely the right circuits and it "
        "will not only be deranged but unaware of it, and so will never seek repair — "
        "which is what he says fascinated him in 1971 and 1972 and produced A Scanner "
        "Darkly, here called \"the Key Book in the sequence\". The Burroughs invocation "
        "arrives as an immunological figure: a pathogen the immune system failed to "
        "detect, after which the host becomes its instrument.",
        "It is as if the immune system has failed to detect an invader, a pathenogen "
        "(shades of William Burroughs: a criminal virus!)", PKD),

    'BWV-EXP-90-16A': (
        "Folio 90:16A, from Dick's notes on The Transmigration of Timothy Archer. He is "
        "diagnosing Angel Archer as intelligence without faith — a mind that plods and "
        "cannot leap the gap into what he calls divine foolishness — and locates her "
        "failure precisely at the boundary of language: she cannot pass from words to "
        "the non-verbal. The self-description in passing is the reason this card is "
        "here, and it is the only place Dick uses addiction and disease as figures for "
        "language itself. Burroughs is not named; the debt cannot be shown.",
        "It cannot pass over from words (\"I am a word junky, a word disease\") to the "
        "supra or non verbal", PKD),

    'BWV-EXP-90-6A': (
        "Not Dick but his editors. The glossary appended to the 2011 Jackson and Lethem "
        "edition supplies the only dating in the whole archive for the cut-up experiment "
        "Sutin describes: 1978. It also states the debt more confidently than Dick ever "
        "does — that Burroughs's reality-as-control-system and language-as-virus "
        "\"clearly resonated\" with him. Worth reading against Dick's own careful "
        "\"Where Burroughs and I sharply disagree\". The same sentence misplaces Brion "
        "Gysin's nationality.",
        "Burroughs's notions of reality as a control system and language as an "
        "extraterrestrial virus clearly resonated with Dick, who, in 1978, experimented "
        "with the cut-up method", 'Pamela Jackson and Jonathan Lethem, eds.'),

    'BWV-LET-1981-06B': (
        "The close of the Brig Elliot letter, and the hardest problem in the dossier. "
        "Having set out where he and Burroughs agree and disagree, Dick turns the "
        "hypothesis on the person holding it: if an occluding information virus exists, "
        "then the mind assessing the claim is itself occluded, and so is its perception "
        "that the thing exists at all. He does not resolve it. He names the novel where "
        "he tried to.",
        "if you grant an occluding information virus, are you not then yourself occluded "
        "in your very analysis of it, as well as your perception of its existence? There "
        "is a paradox involved. I’m sure you can see that. And I try to deal with it in "
        "VALIS.", PKD),
}
