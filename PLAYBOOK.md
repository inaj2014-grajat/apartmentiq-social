# ApartmentIQ marketing playbook: how to think, and why

Written on 2026-11-28 by the session that built the first posts with Rajat. It is for any agent (Fable, Opus, Sonnet, or a scheduled run) that makes content after it. It does not replace the rules. It explains the thinking behind them, so you can make the same calls on a case the rules do not cover.

Canonical copy: `PLAYBOOK.md` in the GitHub repo `inaj2014-grajat/apartmentiq-social`. If another copy differs, the repo wins.

Read order: `CONTENT_RULES.md` (the rules, Rajat's words), then this file (the thinking), then `series/the-flat-hunt/SERIES.md` (cast, look, voices), then `ig-kit/README.md` (the tools).

## 1. The job, in four lines

- ApartmentIQ's promise to a flat buyer is "measured facts, not marketing claims". A post that bends a fact costs more than a missed post.
- Rajat is the editor. He approves every post himself. Your job is to hand him something he can approve in one look.
- A post must be true, clear on first read, and warm. The cast carries the warmth. The captions carry the facts.
- You are not judged on effort. You are judged on whether the thing works when he opens it.

## 2. How to think through a post, step by step

Do these in order. At each step ask the question, and do not move on until you can answer it.

**Step 1. Who is reading, and where are they standing?**
A person buying or renting a flat in Noida or Gurugram. Pick one real moment: the site visit, the first December in the flat, the lamp on in the afternoon, the brochure page. If you cannot say where the person is standing and what they see, the idea is not ready.

**Step 2. What is the one idea?**
Say it in one sentence a buyer could repeat to a friend. If it needs "and", it is two posts. Example: "The sample flat is one flat; yours can face the other way."

**Step 3. Numbers before words.**
If the post has a number, run `ig-kit/sun_facts.py` first and copy what it prints into the spec's `sources`. Then write around those numbers. Never work a number out in your head, and never round it differently. Why: a number typed from memory is the one thing a builder can use to call the whole account wrong.

**Step 4. Say it no stronger than it is.**
A neighbour's tower "can" shade a flat. It does not "decide" it. A sun angle is for flat ground and a clear sky; it is not any one flat's sun hours. Check every sentence: would it still be true if a builder read it looking for a mistake?

**Step 5. Write three hooks, then read each one cold.**
Three hooks from three different patterns (`aiq-post-craft`, section 3). Then read each with no picture and no context, as a stranger scrolling. If it needs a second read, rewrite it. Name both things in the hook. Do not make the reader decode a clever turn.
- Rejected: "You toured the sample flat. You're buying another." Rajat: "very confusing". "Another" made the reader work out which flat.
- Approved shape: "The sample flat is sunny. Will yours be?"

**Step 6. Tell it in pictures, with the cast.**
Ask: what does each character do that shows the point without words? Dhoop the cat is the sun meter. Where Dhoop sleeps tells the viewer where the sun is. Where Dhoop cannot settle tells them where it is not. Chhaya the dog is the opposite, and is where the humour comes from. A scene shows living with the thing (a lamp on in the afternoon), not a diagram of it. Diagrams belong on the number slides.

**Step 7. Give them lines, and test each line.**
For every speech bubble ask three questions: who is speaking, to whom, and would they say it? A line that only explains the picture to the viewer is a caption, so put it in the caption.
- Rejected: Meera, beside her own lamp, saying "Lamp on at noon?". Rajat: "lamp on at noon baloon? why". She would not ask about a lamp she switched on.
- Fixed: Meera "It's daytime, Dhoop." Dhoop "Not in here." She talks to the cat, the cat answers, and the point lands.
Six words at most. Two bubbles at most. The animals never say a number or a product claim.

**Step 8. Build it with the kit, never by hand.**
`render.py` for slides, `reel.py` for reels. Words are drawn by the kit, never by a picture or video model, because those cannot spell. Pictures come from `ig-kit/cast/`. When the kit stops with an error, fix the post, not the check.

**Step 9. Look at it.**
Open the contact sheet and the full-size slides. Look for: a bubble on a face; words running into each other; a picture that disagrees with its words (a sun patch on a slide about no sun); anything written inside a picture; Flow's small sparkle mark covered. The lint cannot see any of these. Only you can.

**Step 10. File it and prove it.**
Push. Fetch the public URL and compare it with your file. Write the Notion row as `Pending Approval`. Read the row back. Then report. A step you did not read back is "unverified", and you say so.

## 3. How to decide when something is unclear

| The thing in doubt is | Do this |
|---|---|
| A fact (a number, what the site says, what a file holds) | Look it up. Never ask Rajat for a fact. |
| A rule, a taste call, or a trade-off with no right answer | Ask Rajat once, with what you checked and a recommended answer. |
| Cheap, and easy to undo (wording, a bubble position, a free still) | Do it. State the assumption in the report. |
| Costs credits, publishes, deletes, or changes an approved post | Stop and ask first. |

One question at most in a reply. If you made an assumption, say what it was and how to reverse it.

## 4. Spend last

Stills in Flow cost 0 credits. A video clip costs 24. So the order is always: stills first, then one moving test, then the full piece.
- For a new look: two or three style stills, let Rajat pick, then one 8 second test in that look.
- Inside an episode: make each shot's first frame as a still, check the cast matches, and only then animate it.
Why: the first series look (a miniature diorama) was chosen from a description and one short test. 96 credits went on it before Rajat saw a full episode, and he withdrew it. The second look was chosen from three free stills and held.

## 5. When Rajat gives feedback

Five moves, every time.
1. **Answer what he asked, plainly.** If he asks "why", say why. If the line was weak, say it was weak and what made it weak.
2. **Find the general fault, not just the instance.** "Confusing hook" is the instance. "The hook did not name both things" is the fault.
3. **Fix every place it appears.** The lamp line was in the reel and in the carousel. Both were fixed in the same turn.
4. **Record it.** His exact words go in the row's Feedback. The lesson goes in `CONTENT_RULES.md` section 4, in the same session, with his words quoted.
5. **If a tool could have caught it, add the check and a test for it.**

| What was made | What Rajat said | The real fault | The lesson |
|---|---|---|---|
| A miniature diorama series | "i am looking for a different animation style.. colorful, trendy.. and a storyline with charectords, including animals" | A look was chosen in words and built before he saw it | Lesson 8: show stills before spending |
| "You toured the sample flat. You're buying another." | "very confusing" | A clever turn the reader had to decode | Lesson 9: clear on first read, name both things |
| "We build the towers in 3D" over footage of a tower going up | "It seems to covey that we create the neighbour tower" | Words that meant one thing next to a picture that meant another | Lesson 5: read the words against the picture they sit on |
| Meera: "Lamp on at noon?" | "lamp on at noon baloon? why" | A caption dressed up as speech | Lesson 10: a line must fit its speaker |

| Five carousels built as lessons, all from the same six pictures | "But it's the same images", "it should be stories from normal daily life", "We are creating micro series which are funny and relatable" | A reused picture was reported as a caveat instead of being fixed, and the post taught before it entertained | Lessons 12 and 13: new pictures for each post, and a funny daily-life story first, the fact after. He said "Good" to that shape |

A change he asks for is a new revision. The post goes back to `Pending Approval`. "ok" in chat is not approval; only the Notion Status is.

## 6. Changing the kit

1. Write the test first and run it. It must fail.
2. Make the change. Run `test_kit.py`. Every case must behave as expected, including at least one case that must be refused.
3. Re-lint every existing post. Re-render one approved post and confirm its slides are unchanged.
4. Only then use the new feature on a real post.
Why: a check that has only ever been seen passing has not been tested.

## 7. Habits that kept this from going wrong

- **Read Notion with a SQL-mode query.** Page fetch returns markup that must never reach Instagram.
- **A post's spec, caption, media and Notion row move together.** The publish run lints the spec at the row's Spec URL against the row's Caption. If you change one and not the other, an approved post fails on the day.
- **The Notion page body is what Rajat looks at.** A new revision replaces the pictures and the watch link in the page body, not only the Media URLs field. Then fetch the page and check the body shows the new files. On 28 Nov two rows had new Media URLs but still showed the old slides and linked the old reel; Rajat: "i dont see the latest version there with chrectors".
- **Test what Buffer will read.** Create a draft with the real media URLs, read it back, delete the draft.
- **Keep the old version reachable.** When you replace an approved post, keep its files and write in Run Log how to go back.
- **In Flow, click by element reference, not by screen position.** Wait 90 seconds for a 1080p download. Search Downloads by file name; never list the whole folder.
- **Approve a Flow quote only if it says 1 video and 24 credits.**

## 8. Mistakes already made, so you do not repeat them

- Listed Rajat's whole Downloads folder and exposed personal file names.
- Started three video clips for an idea minutes before he changed direction. 72 credits unused.
- Chose a look from a description instead of from stills.
- Wrote a hook that was clever instead of clear.
- Gave a character a line that explained the picture.
- Updated a row's fields for a new revision and left the old pictures in the page body, so Rajat was looking at the old version.
- Reused the same six cast pictures across five posts and told Rajat about it as a caveat. A known flaw is fixed before the work is shown, not listed under it.
- Did the same again an hour later: sent a slide whose picture did not show its words and called it "the loosest picture" in the report. Rajat: "If you know there is a loose picture why do we have it". Remaking it took one free still.
- Built carousels as a lesson with one illustration. He wanted a funny story from daily life, with the fact after it.
- Asked a model to draw a moving shadow on real buildings from a reference image, twice. It cannot. A scale model or a time-lapse prompt works.

## 9. How to report to Rajat

- First line: the verdict, and the one file to open.
- Then: what changed, what was checked, what was not, what it cost, what he must do.
- Short sentences. Exact numbers and paths. Each caveat next to the thing it qualifies.
- Say "unverified" for anything you did not check yourself.
- Last line: "Final check:" and what the re-read added.

## 10. If you are a smaller or faster model

- Do the steps in section 2 in order. Do not merge them.
- Do not skip Step 9. Open the image and look.
- When unsure whether a claim is allowed, leave it out and write why in Run Log.
- When the kit refuses something, change the post. Never change the lint, a `sources` entry, or the rules to get a pass.
- Use the bubble positions in `ig-kit/cast/cast.json` as they are. Do not guess positions.
- You cannot make new pictures in a scheduled run. Pick from `ig-kit/cast/`. If none fits, use the nearest and write `cast: no picture fits <topic>` in Run Log.
