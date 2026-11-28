# apartmentiq-social

Finished Instagram media for @apartmentiq.in, and the kit that makes it.
No product data, no drawings, no scoring logic lives here. This repo is public because Buffer
reads media from a public URL.

Read in this order before making anything:

1. `CONTENT_RULES.md` what Rajat has approved and rejected, in his words. Read it in full. It wins over everything but his word.
2. `PLAYBOOK.md` how to think and work, with the reasons and worked examples. Copy this approach.
3. `series/the-flat-hunt/SERIES.md` the cast, their voices, the look, how clips and cast pictures are made.
4. `ig-kit/README.md` how the kit works.

What is where:

- `ig-kit/` the kit: `sun_facts.py` (numbers), `render.py` (slides), `reel.py` (reels), `lint_aiq.py` (the gate), `test_kit.py` (proves the gate).
- `ig-kit/cast/` the cast pictures for carousels and posts, with `cast.json` and `cast_sheet.jpg`.
- `series/the-flat-hunt/look/` reference pictures for the look.
- `instagram/<publish-date>-<slug>/` one folder per post: `spec.json`, `caption.txt`, the slides or the reel, `contact.jpg`.

Public URL of any file: `https://raw.githubusercontent.com/inaj2014-grajat/apartmentiq-social/main/<path>`
