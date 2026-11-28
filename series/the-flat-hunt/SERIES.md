# The Flat Hunt · series guide

An animated microseries for @apartmentiq.in. Rajat, 28 Nov 2026: "i want to create a animated microseries on this theme".

**Look: stylised 3D animation.** Rajat picked it on 28 Nov 2026 from three style stills (A stylised 3D, B flat 2D, C claymation) with "a", and asked for episode 1 after the moving look test (`look_test_02_stylised_3d.mp4`).

History: the first look, a miniature diorama, was withdrawn by Rajat after he saw episode 1 in it: "i am looking for a different animation style.. colorful, trendy.. and a storyline with charectords, including animals". Do not use it. Its files are kept under `r1-diorama` names for the record only.

Read `CONTENT_RULES.md` first. Every rule there applies to the series.

## The idea in one line

A couple and their pets hunt for a flat in Noida. The cat only sleeps in the sun. In each episode the visit hides something, and the cat finds it out.

## The cast

Names are invented. They are for scripts, captions and the small sub-line only. Never put a surname, a builder or a society on them.

| Name | Who | Always |
|---|---|---|
| **Meera** | Woman, wavy shoulder-length dark hair | Yellow kurta. She notices things first. |
| **Kabir** | Man, short dark hair | Teal henley shirt, jeans. He looks at the plan and the price, then follows her gaze. |
| **Dhoop** | Ginger tabby cat | Only sleeps in a patch of sun. Dhoop is how the viewer sees where the sun is, and where it is not. |
| **Chhaya** | Black labrador | Only sleeps in the shade. Happy wherever Dhoop is not. |
| **Gutar** | Plump grey pigeon | Sits on the balcony railing and watches. A bit part. |

Dhoop is Hindi for sunshine, Chhaya for shade. Do not explain this on screen.

## The world

Bright, clean flats high up in apartment towers in an Indian city. Pale tiled floors, a wide balcony door on the left, the front door on the right, other towers outside. Vibrant colours, soft rounded shapes. The light is the story: a hard bright patch of sun on the floor, or none.

## How every clip is made (this order, every time)

1. **Make the first frame as a still. It costs 0 credits.** In Flow, attach the reference image and ask for "one still image, vertical 9:16, with Nano Banana". The reference for a new room is the look still `series/the-flat-hunt/look/look_A_reference.jpg` (in Flow it is the image titled "Couple watching sleeping pets"). The reference for the same room in a new state is the previous still of that room.
2. **Look at the still before spending.** Check all five points in "What to check" below. Remake it if any fail.
3. **Animate the still: 24 credits.** Attach the still and write "Generate one 8 second video. Use the attached image as the first frame and keep exactly the same characters, room and stylised 3D animated film look." Then one small action per character, the light rule, the camera move, the sound, and "No speech, no text, no captions, no logos, no music."
4. Download as 1080p (Upscaled). See `ig-kit/README.md` for the click-by-click notes.

Still prompt block (copy, then fill the scene):

> Generate one still image, vertical 9:16, with Nano Banana. Use the attached image [only as a reference for the same four characters and the same stylised 3D animated film look with vibrant colours and soft rounded shapes. It is a new scene in a different flat. / as a reference for the same four characters, the same stylised 3D animated film look, the same room and the same camera angle.] Scene: [the room, its furniture, what is outside the balcony]. [The light: where the patch of sun is, or "No direct sunlight enters the room and there is no patch of sun on the floor."] The same woman with wavy shoulder-length dark hair in the yellow kurta and the same man with short dark hair in the teal henley shirt [what they do]. The same ginger tabby cat [what it does]. The same black labrador dog [what it does]. Wide shot, camera at chest height. Keep the top third of the picture as plain ceiling and wall. No text, no signs, no logos.

Flow settings for video: Omni 1.2 Flash, 9:16, 1 output, 8 seconds, 24 credits a clip. Approve a quote only if it says 1 video and 24 credits.

## The shape of every episode (about 25 seconds)

| Part | Length | Job |
|---|---|---|
| Scene 1 | 4.5 s | The hook, on screen from the first frame. Chip: `THE FLAT HUNT · EP n`. Dhoop does something that shows the hook. |
| Scene 2 | 5 s | The turn: what the visit did not show. A new room or a new state of the room. |
| Scene 3 | 5 s | Living with it in winter. The sub-line may name Dhoop ("Dhoop the cat naps under a lamp now"). |
| Scene 4 | 5.5 s | **The same in every episode:** `clips/s4_home_in_the_sun.mp4` (the look test: Dhoop rolling in the sun at home, Chhaya under the sofa, Gutar on the railing, Meera and Kabir at the door). First 2.5 s: chip `THE RIGHT FLAT`, "Dhoop knows / where the sun is. / **Now you can too.**" Then chip `APARTMENTIQ` with the mark: "We trace the **real sun** / on your exact flat" · "hour by hour · season by season". |
| End card | 5 s | The standard end card. |

Three new clips an episode (72 credits). Scene 4 is already paid for: copy it from episode 1's `clips` folder.

All captions go at the **top** (`"position": "top"`). Flow's sparkle mark sits at the bottom right and must stay uncovered, and the animals are in the lower half.

Caption starts "The Flat Hunt · Episode n · <title>" (a middle dot, not a colon: the lint reads "1:" as a number), introduces Dhoop in one line, and follows the caption shape in `CONTENT_RULES.md` section 5, with "Scenes are illustrative."

## Episodes

| Ep | Title | Hook | Slot | State |
|---|---|---|---|---|
| 1 | The sample flat | The sample flat is sunny. Will yours be? | Thu 10 Dec | Built 28 Nov as `reel-r5.mp4` (with speech), waiting for Rajat. The first hook ("You toured the sample flat. You're buying another.") was dropped: Rajat found it "very confusing" |
| 2 | Low floor, high floor | Low floor. High floor. Same tower. Different winter. | Thu 17 Dec | Not started |
| 3 | North-facing in December | North-facing. No direct sun all December. | Mon 21 Dec (needs a one-off publish run) | Not started |
| 4 | East-facing | East-facing. But what stands in the east? | Thu 24 Dec | Not started |
| 5 | Where the neighbours dry their clothes | Look where the neighbours dry their clothes. | Thu 31 Dec | Not started |

Do not build episodes 2 to 5 until Rajat has approved episode 1 in this look. Scene notes for them are in `REEL_CONCEPTS_2026-11-28.md` on Rajat's PC (`marketing\instagram\`), written for live action: re-stage each with the cast, and let Dhoop show the point.

Episode 1, for reference: (1) the sample flat, a big sun patch, Dhoop flops into it; (2) chip `YOUR FLAT`: the flat they get, same layout, other side of the tower, empty, no sun patch, Dhoop looks for it and Chhaya is delighted; (3) the same flat in winter, a lamp on in the daytime, Meera in a shawl, Dhoop asleep in the lamp's light; (4) the shared closing.

## What to check in every still and every clip

1. Yellow kurta and teal shirt are both there, on the right people, with the same faces and hair.
2. The cat is ginger and the dog is black. Neither changes size or breed between shots.
3. The light does what the caption says. If the caption says there is no sun, there is no hard patch of sun on the floor at any time in the clip.
4. No writing anywhere: no signs, no labels on boxes, no brand on anything.
5. Flow's watermark is visible and not covered.
6. Hands, paws and faces: nothing broken, nothing exaggerated.

## Voices (the cast talks)

Rajat, 28 Nov 2026: "i want charectors to interact (dog and cat to talk in as well)". Speech is a speech bubble drawn by the kit (`"say"` in the spec). It is text on screen, not sound.

| Who | How they talk | Example |
|---|---|---|
| **Dhoop** (cat) | Dry and entitled. Talks only about the sun, as if it were his. | "Sun! Mine." · "Where is my sun?" · "Not in here." |
| **Chhaya** (dog) | Cheerful and easy to please. Loves shade. Often answers Dhoop with the opposite. | "Shade! Mine." · "Shade for me." |
| **Meera** | Talks to Kabir and to the animals. Says what she sees. | "I love it!" · "It's daytime, Dhoop." |
| **Kabir** | Slower to notice. Reacts to what Meera or the animals point out. | (none yet) |
| **Gutar** (pigeon) | Says nothing. | |

Rules:
- Six words at most a line. Two bubbles at most in a scene or on a picture slide. Let them answer each other.
- Each line must be something that character would say to someone in the picture. A line that only explains the picture to the viewer belongs in the caption (`CONTENT_RULES.md` lesson 10).
- The first bubble of a scene comes about 0.8 s after the cut, the second about 1.5 s later. A scene with two bubbles runs at least 4.5 s.
- The animals never say a number, a product claim or the name ApartmentIQ. The captions carry the facts; the cast carries the feeling.
- Nobody mocks a broker or a builder. No surnames. English.
- A bubble never covers a face, the caption band at the top, or Flow's mark at the bottom right. The kit refuses the last two; faces are checked by eye.
- To place a bubble in a reel, pull a frame at the moment it appears and read the speaker's head position off it: the animals move.

## Cast pictures (for carousels and single posts)

Rajat, 28 Nov 2026: "i want these charectors to be used in carousals and posts as well". The rule is `CONTENT_RULES.md` section 7. The pictures live in `ig-kit/cast/` with `cast.json`.

To add one (live chat with Flow open; 0 credits):

1. In Flow attach the look still ("Couple watching sleeping pets"). If the picker already previews it, press "Add to prompt"; clicking the name again closes the picker.
2. Ask: "Generate one still image, landscape 4:3, with Nano Banana. Use the attached image only as a reference for the same characters and the same stylised 3D animated film look with vibrant colours and soft rounded shapes. It is a new scene. Scene: [...]. Keep the people and animals in the middle of the picture, away from the edges. No text, no signs, no logos."
3. Download the PNG, look at it against "What to check" above, and check the walls: no religious pictures, no writing.
4. Save it as `ig-kit/cast/<name>.jpg` (4:3, quality 92; crop only to remove something on a wall, never the bottom right corner) and add its entry to `cast.json`: `name`, `file`, `shows`, `light`, `use_for`.
5. Run `python3 -I ig-kit/test_kit.py`.

Six pictures made on 28 Nov 2026: `visit_sunny`, `no_sun_patch`, `winter_lamp`, `balcony_tall_tower`, `dhoop_in_the_sun`, `ask_on_visit`.

## Known flaws (accepted on episode 1; say so when reporting)

- A still made in Flow carries its own small sparkle mark in the picture. When that still is animated with a camera push-in, the old mark drifts while Flow's video mark stays put, so two sparkles can show for a second or two. Do not paint over either.
- The sound in each clip (purr, meow, room tone) was asked for in the prompt but nobody has listened to it. Rajat plays each reel with sound before he approves.
