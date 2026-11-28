# ApartmentIQ Instagram: content rules

What Rajat has approved and rejected, in his words where he gave them. Read all of it before
writing a post. Where this file and a skill disagree, this file wins. Where Rajat says something
new, his word wins, and the lesson is added here in the same run.

## 1. Rulings (Rajat, 2026-11-27)

| Question | Ruling |
|---|---|
| Real app or website screens in posts | **Never.** |
| Naming a real society or builder with its numbers | **Not yet.** Raise it again after a month of posts. |
| Who approves | Rajat approves every post himself in Notion. |

From the first film brief (2026-11-25): "photo realistic, state of the art graphics.. dont use images from the apartmentiq website.. consider the audiance as retail custmers looking for buying or renting.. the video should start with enaging hook and should be able to retain the audiance throughout".

- **The cast appears in carousels and single posts too, not only in reels, and they talk.** Rajat, 2026-11-28: "i want these charectors to be used in carousals and posts as well", then "nice.. we will keep it to thi theme.. and i want charectors to interact (dog and cat to talk in as well)". How: section 7.

## 2. What the product may claim (read from the live site, 2026-11-27)

- "See the sun your flat actually gets."
- 3D sunlight analysis for apartments in Noida and Gurugram. Nowhere else.
- Hour by hour, season by season, for your exact flat.
- Free while in pre-launch. Most reports ready within 48 hours.
- Works for new, resale and rented flats.
- The Sun Score is the hours of direct sun a flat gets on 21 December.
- The model leaves out trees, temporary structures and buildings not yet sanctioned.

Not live, so never claimed: heat, wind, noise, privacy, view, Vastu, valuation, any score other than sun.
If the site changes, this section is re-read from the site before the next draft.

## 3. Numbers

Every number comes from `ig-kit/sun_facts.py` and is listed in the post's `sources`. A sun angle or a
shadow length is a fact about the sky over flat ground. It is never presented as a flat's sun hours.

## 4. Lessons from Rajat's reviews

1. **Compare like with like.** First cut said "You saw the flat at 11 AM" then "You'll live in it in December". Rajat: "i dont think that 'you'll live in t in dec' in working here.. as the previous frame didnt talk about the month". Fix: both halves name a month, and both labels carry the same hour.
2. **Never repeat a shot to make the second point.** The second scene re-used the walk-in, darkened. Rajat: "the walking in 2nd frame is repetitive.. ned something else to emphasise the point of low sunlight experience". Fix: a new scene that shows living with low sun (lamp on at 11 AM, shawl, laundry indoors, a tower in the window).
3. **Say what is true, no stronger.** "The tower next door decides your sunlight" became "can take your sunlight". Prefer "can" to "decides", "will" or "always".
4. **One caption edit so far, not yet a rule:** on the first reel Rajat cut "from sanctioned drawings and RERA filings" from the caption. Do not put that phrase in a caption unless he asks for it.
5. **ApartmentIQ does not build towers, so do not say "build" after footage of one going up.** The 3 Dec reel showed a plan growing into a tower, then the line "We build the towers in 3D". Rajat: "It seems to covey that we create the neighbour tower". Fix: say what we do to the sun, not to the tower: "We trace the real sun on your exact flat", "3D sunlight analysis". (The first reel's "We build your tower in 3D" was approved, but it had no construction footage before it.)
6. **Set the story where the viewer lives, then make the point.** The 3 Dec reel first showed a drawing on a table growing into a lone tower over low houses. Rajat: "doesnt make sense.. it needs to show tower being built among already existing tower neighbourhood and then convey the message". Fix: open on existing apartment towers (the viewer's home), show the new tower going up on the plot next door, show its shadow on the neighbouring tower, then the ApartmentIQ line.
7. **Reels are a series: The Flat Hunt, in stylised 3D animation, with a cast.** Rajat, 28 Nov 2026: "i want to create a animated microseries on this theme". The first look (a miniature diorama) was withdrawn after he saw episode 1: "i am looking for a different animation style.. colorful, trendy.. and a storyline with charectords, including animals". He then picked stylised 3D from three style stills ("a") and asked for episode 1. The cast is Meera, Kabir, Dhoop the ginger cat who only sleeps in the sun, Chhaya the black dog who only sleeps in the shade, and Gutar the pigeon. Every Thursday reel is an episode unless Rajat says otherwise. The cast, the world, the prompt blocks, the fixed closing scene and the episode list are in `series/the-flat-hunt/SERIES.md`: read it before any reel work. It replaces the "Blind spot reels" topic list in the `aiq-ig-publisher` skill.
8. **Show the look before spending on it.** A style named in words and one 8 second test did not predict Rajat's reaction to the diorama: 96 credits went on a look he withdrew. Fix: for a new look, show two or three style stills first (stills cost 0 credits in Flow), then one moving test in the look he picks, then the episode. Inside an episode, make each shot's first frame as a still and check it before animating it.

9. **A hook must be clear on first read.** Episode 1 opened with "You toured the sample flat. You're buying another." Rajat, 28 Nov 2026: "very confusing". "Another" left the reader to work out which flat was meant. Fix: "The sample flat is sunny. Will yours be?" Say the two things by name ("the sample flat", "yours", "your flat") and do not make the reader decode a clever turn. Before using a hook, read it alone with no picture: if it needs a second read, rewrite it.

10. **A line of speech must make sense for the one who says it.** Meera, sitting beside her own lamp, was given "Lamp on at noon?". Rajat, 28 Nov 2026: "lamp on at noon baloon? why". She would not ask about a lamp she switched on, and the picture is an afternoon, not noon. Fix: Meera "It's daytime, Dhoop." and Dhoop "Not in here." Before using a line, ask who is speaking, to whom, and whether they would say it. A line written only to explain the picture to the viewer is a caption: put it in the caption.

## 5. Caption shape (approved on the first reel)

1. The hook, 125 characters or fewer.
2. One or two short paragraphs: the problem, in plain words.
3. One paragraph: what ApartmentIQ does about it.
4. "Free sun report during pre-launch." and `apartmentiq.in`.
5. "Scenes are illustrative." when the post uses AI footage. For sun-fact posts, one line saying the numbers are for flat ground and a clear sky.
6. Last paragraph: up to 10 hashtags, `#ApartmentIQ` first.

Plain English. Short sentences. No emoji. No exclamation marks.

## 6. Look

Navy, emerald, white. Inter and IBM Plex Mono. 21 December is always blue, 21 June always amber.
Calm and minimal. The renderer holds these; do not restyle a post by hand.

## 7. The cast in carousels and posts (from 2026-11-28)

The cast is Meera, Kabir, Dhoop the ginger cat, Chhaya the black dog and Gutar the pigeon (`series/the-flat-hunt/SERIES.md`). Every new carousel and single post shows them. Posts Rajat approved before this date stay as approved unless he says to redo them.

1. **Slide 1 carries a cast picture.** Give the hook slide `"image": "<name>"`. The picture sits above the hook. This holds for every pillar, including the first-Saturday "How it works" post: "drawn graphics only" there means no app or website screens, not no cast.
2. **One more picture slide in the middle**, type `scene`, where the post says what the point means for a flat. Two or three pictures in a post at most. Number slides (`compare`, `shadow`, `fact`) and the `list` slide stay as drawn. The end card does not change.
3. **Pictures come only from `ig-kit/cast/`.** `cast.json` says what each one shows and what it is for. Open the .jpg and look before using it. A scheduled run cannot make pictures: it picks from this folder. If none fits, use the nearest one and write `cast: no picture fits <topic>` in Run Log, so a new one gets made in a live chat.
4. **The picture must agree with the words.** A slide about a flat with no sun does not get a picture with a sun patch, and the other way round. `cast.json` has a `light` field for this.
5. **Say the scenes are illustrative.** Set `"ai_footage": true` in the spec and put the line "Scenes are illustrative." in the caption. The lint refuses the post otherwise.
6. **Names.** Dhoop, Chhaya, Meera and Kabir may be named in a `sub` line or the caption ("Dhoop the cat", the first time). No surnames. The hook must still make sense to someone who has never seen them.
7. **Never paint on, crop or cover a picture.** Flow's sparkle mark at its bottom right stays visible. The renderer shows the whole picture.

8. **The cast talks, the dog and the cat too.** Rajat, 2026-11-28: "i want charectors to interact (dog and cat to talk in as well)". Speech goes in speech bubbles drawn by the kit (`"say"` in the spec), in reels and on picture slides. Six words at most a line, two bubbles at most in a scene or on a slide. Who says what, and what they never say, is in `series/the-flat-hunt/SERIES.md`, section "Voices". Speech is on-screen text only: no voices in the sound unless Rajat asks.

9. **Bubble positions come from `cast.json`.** Each picture lists a tested `tip` and `box` for every character who has room to speak in it. Copy them into the slide's `say`. Do not guess positions, and do not give a line to a character the picture has no entry for.
10. **A new post starts at revision 1.** Leave `revision` out of a new spec, even though the reference post's spec carries one.

Worked example: `ig-kit/examples/carousel-with-cast/` (a copy of the 1 Dec carousel spec with two pictures and speech). Spec fields: `ig-kit/README.md`.
