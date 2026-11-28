# ig-kit: how an ApartmentIQ post is made

Four scripts. Run every one with `python3 -I` from the repo root.

| Script | Does | When |
|---|---|---|
| `sun_facts.py` | Prints sun numbers for a place and date | Before writing any number |
| `render.py` | Draws a carousel from `spec.json` | Carousels |
| `reel.py` | Builds a reel from clips + `spec.json` | Reels |
| `lint_aiq.py` | The gate. Exit 1 = do not publish | Every draft, and again before publishing |
| `test_kit.py` | Plants faults and proves the gate refuses them | After any change to the kit |

Needs: Python 3.10+, `pillow`, `numpy`, `scipy`, and `ffmpeg` for reels.
`pip install pillow numpy scipy --break-system-packages -q` if an import fails. Fonts are in `fonts/`.

## The order of work for one post

1. **Pick the one idea.** One post, one idea a buyer or renter can picture.
2. **Get the numbers first.** Run `sun_facts.py` and copy the values into `spec.sources`. Never write a number from memory, and never do the arithmetic in your head.
3. **Write `spec.json` and `caption.txt`** in `instagram/<publish-date>-<slug>/`.
4. **Lint.** Fix until it passes. Do not edit the lint to make a post pass.
5. **Render**, then **look at `contact.jpg`** (the list below).
6. Push. Confirm every raw URL returns 200.

## Carousel spec, complete example

`instagram/2026-12-01-december-noon-sun/spec.json` is the reference. Slide types are listed at the top of `render.py`.
Each `sources` entry is one of:

```json
{"display": "38.0°", "script": "sun_facts.py", "args": "--place noida --date 2026-12-21", "field": "noon_altitude_deg", "format": "{:.1f}°"}
{"display": "100 m", "given": "example tower height chosen for the drawing; an input, not a measurement"}
```

`display` is the exact text on the slide. The lint runs the script and compares. `given` is only for inputs and labels, and each one prints as a warning for the reviewer.

## Reel spec

`instagram/2026-11-27-march-vs-december/spec.json` is the reference (the first reel, rebuilt by `reel.py`). Fields are listed at the top of `reel.py`.

## Look at it (checks no script can make)

Open `contact.jpg` and answer each one. Any "no" goes back to the spec.

1. Can every line be read at phone width? Nothing clipped, no word alone on a line.
2. Does slide or frame 1 make sense with nothing else, and say something specific?
3. If two things are compared, do both halves name the same kind of thing (month against month, floor against floor)?
4. Is each picture a new picture? Never repeat a shot to make the second point.
5. Reels: is the sun where it could really be for the month and hour named? Check with `sun_facts.py --time`. Morning sun is in the east, evening sun in the west, and the winter noon sun is low in the south.
6. Reels: is Flow's sparkle watermark (bottom right) uncovered and uncropped?
7. Reels: no garbled letters, no card or sign with fake text, no broken hands, no exaggerated faces.
8. Is every claim one the live site makes? If you are not sure, leave it out.

## Making reel footage in Google Flow (live sitting, through Chrome)

Settings: model **Omni 1.2 Flash**, 9:16, 1 output, 8 seconds, 720p. Flow quotes 24 credits a clip and asks for approval each time: approve only if it shows 24 or fewer. Budget: at most 3 clips a reel, 4 reels a sitting.

Prompts that worked:
- Plain description, in this order: what kind of shot, the place, the light, who is there and one action, the camera move, the sound, then "No text, no captions, no logos, no music."
- No instructions to the agent mixed into the description, and no colour codes: an early prompt with both was blocked.
- People: "Indian", an age, plain clothes, "natural and understated". One action per clip.
- To keep the **same room and people** in a second mood (sunny, then dark): open the first clip, and use "Describe how to edit this video" with "Keep the same room, the same camera move and the same people. Change ...".
- To keep the **same person in a new scene**: open the clip, move the playhead to a frame with a clear face, press "Save frame", add that image to the prompt with "+", and write "Use the attached image only as a reference for the same woman and the same room. It is not the first frame."
- Flow cannot use a video as a reference, only an image.
- Two prompts that worked first time on 28 Nov 2026 (both start "Photorealistic aerial time-lapse from a drone of a cluster of modern high-rise residential apartment towers in an Indian city, pale cream facades with balconies, green lawns below"): (1) a new tower rising on an empty plot between existing towers: "Between the towers is one empty construction plot of bare earth. Thin pale blue glowing lines of a floor plan appear on the empty plot. Concrete columns rise from the lines, floor slabs stack up storey by storey, and a new apartment tower grows fast in time-lapse until it stands taller than the towers around it. The existing towers stay exactly as they are." (2) a shadow climbing a neighbour: "The sun moves fast across the sky. The long dark shadow of the tall new tower sweeps steadily across the facade of the neighbouring older tower, and its balconies fall into shade floor after floor. Camera almost still with a very slow push-in." Start from these words; a reference image was not needed.
- In Chrome, click Flow's buttons by element reference (find, then click the ref) and focus the prompt box before typing. Clicking by screen position opened the wrong item on 28 Nov.
- A **moving shadow on real buildings** did not work (two tries, 27 Nov 2026): one gave a day-to-dusk fade, one a still aerial. What worked first time: a white **scale model** on a drawing in a dim studio with "a single warm lamp moves slowly in a low arc ... the tall tower's long dark shadow sweeps slowly across the low blocks". Use the model shot when the shadow itself is the point.
- A drawing in shot grows small fake dimension numbers even when the prompt says "no writing". Place the caption band over them and check the first frame.
- A "plan grows into a building" clip works in one 8 second shot: drawing, glowing lines, columns, slabs, finished tower. Split it into two scenes at the 4 second mark.
- **Animated series clips (The Flat Hunt, stylised 3D):** first make each shot's first frame as a still ("Generate one still image, vertical 9:16, with Nano Banana", with a reference image attached; 0 credits and no approval step), check it, then attach that still and ask for "one 8 second video" with it "as the first frame". On 28 Nov 2026 this kept the two people and the two animals the same across four shots in three rooms, first try each. Full prompt blocks: `series/the-flat-hunt/SERIES.md`.
- The Flow agent takes the next request while a video is still rendering: send clip 2 as soon as the prompt box shows the send arrow again, about 80 seconds after approving clip 1. In the editor, the strip of titles along the top switches between clips, so all downloads can be done without going back to the project page.
- Download each clip as **1080p (Upscaled)**. It takes about a minute. Clips land in the Downloads folder. Wait a full 90 seconds before moving the file: a move tried while Chrome is still writing fails and leaves the file locked for the session. If that happens, download it again and move the copy named "(1)". Find the file by a name search; do not list the whole Downloads folder.

## What the kit refuses

See the docstring of `lint_aiq.py`. In short: a typed number, a number with no source, a builder or project name, an app or website screen, a claim the site does not make, AI footage without "Scenes are illustrative.", a caption without `apartmentiq.in`.
