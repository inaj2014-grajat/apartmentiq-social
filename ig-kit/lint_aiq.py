#!/usr/bin/env python3
"""lint_aiq.py: the gate every ApartmentIQ Instagram post passes before it is drafted,
and again in the same run before it is published.

USE
  python3 -I ig-kit/lint_aiq.py --spec <dir>/spec.json --caption <dir>/caption.txt
Exit 0 = pass (warnings may still print). Exit 1 = at least one FAIL: do not publish.

WHAT IT ENFORCES, AND WHY
 1. DERIVED NUMBERS. Every number on a slide or in the caption must have an entry in
    spec["sources"]. An entry with "script" is RE-COMPUTED here by running sun_facts.py
    and must print exactly the text on the slide. An entry with "given" is an input or a
    label (an example tower height, a date) and needs a reason. Product rule: figures are
    derived from data, never typed.
 2. NO NAMED BUILDER OR PROJECT. Rajat, 2026-11-27: "Not yet".
 3. NO APP OR WEBSITE SCREENS. Rajat, 2026-11-27: "Never".
 4. ONLY CLAIMS THE LIVE SITE MAKES. No guarantees, rankings, testimonials, or pillars
    that are not live (heat, wind, noise, Vastu...). Coverage is Noida and Gurugram.
 5. CAPTION SHAPE. First line 125 characters or fewer, 2,200 at most, the site address,
    at most 10 hashtags and only in the last paragraph, "Scenes are illustrative." when
    the post uses AI footage.
It cannot judge taste, whether a comparison is fair, or whether footage is physically
right. Those are in the "Look at it" list in README.md and are checked by eye.
"""
import argparse, json, os, re, subprocess, sys, shlex

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS, WARNS = [], []

BUILDERS = """dlf godrej jaypee supertech gaur gaurs mahagun sobha m3m emaar eldeco experion
kalpataru amrapali gulshan bhutani lodha vatika unitech parsvnath ansal omaxe shapoorji
whiteland smartworld conscient ireo raheja bptp adani ajnara antriksh logix panchsheel nirala
samridhi civitech migsun sunworld krisumi tarc aipl""".split()
# names that are also ordinary words are matched only as phrases, so "cold wave" or "signature" pass
BUILDER_PHRASES = ["max estate", "max estates", "ace group", "ace parkway", "ace arte", "central park",
                   "hero homes", "lotus greens", "lotus boulevard", "wish town", "garden isles", "kasa blanca",
                   "prestige city", "prestige group", "pious orchards", "kingston heath", "signature global",
                   "wave city", "county group", "tata housing", "tata realty", "mahindra lifespaces",
                   "birla estates", "paras buildtech", "puri constructions", "elan group", "ats greens",
                   "ats bouquet", "ats group", "sikka group", "saya homes", "apex group", "fusion homes",
                   "pioneer urban", "tulip infratech", "ambience group", "suncity projects", "ss group"]
BANNED = {  # phrase -> why
    "guarantee": "no guarantees", "guaranteed": "no guarantees", "100% accurate": "no accuracy claims",
    "accurate to": "no accuracy claims", "best flat": "no rankings", "#1": "no rankings",
    "no. 1": "no rankings", "trusted by": "no testimonials", "customers say": "no testimonials",
    "our users say": "no testimonials", "rera approved": "not a claim the site makes",
    "rera certified": "not a claim the site makes", "government approved": "not a claim the site makes",
    "price will": "no price predictions", "appreciation": "no investment claims",
    "investment advice": "no investment claims", "you will": "no predictions about the reader's flat",
}
NOT_LIVE = ["vastu", "wind score", "noise score", "privacy score", "heat score", "walkability", "valuation",
            "ar walkthrough", "livability score"]
OTHER_CITIES = ["mumbai", "pune", "bengaluru", "bangalore", "hyderabad", "chennai", "kolkata", "ahmedabad",
                "faridabad", "ghaziabad", "greater noida", "lucknow", "jaipur", "chandigarh"]
NUM = re.compile(r"\d[\d,.:]*(?:\s?(?:°N|°|m\b|km\b|min\b|h\b|%|AM\b|PM\b|am\b|pm\b))?")


def fail(msg):
    FAILS.append(msg)


def warn(msg):
    WARNS.append(msg)


def strings(obj):
    """Every text string inside the slides (or scenes), flattened."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("type", "tone", "size", "clip", "position"):
                continue
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def norm(t):
    return re.sub(r"\s+", " ", t.replace("**", "")).strip()


def check_sources(spec):
    """Re-compute every scripted number. Returns the list of display strings that are backed."""
    backed = []
    for src in spec.get("sources", []):
        disp = src.get("display")
        if not disp:
            fail(f"source entry without 'display': {src}")
            continue
        if "script" in src:
            if src["script"] != "sun_facts.py":
                fail(f"source {disp!r}: unknown script {src['script']!r} (only sun_facts.py is allowed)")
                continue
            cmd = [sys.executable, "-I", os.path.join(HERE, "sun_facts.py")] + shlex.split(src.get("args", ""))
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                fail(f"source {disp!r}: sun_facts.py failed: {r.stderr.strip()[:200]}")
                continue
            val = json.loads(r.stdout).get(src.get("field"))
            if val is None:
                fail(f"source {disp!r}: sun_facts.py printed no field {src.get('field')!r}")
                continue
            got = src["format"].format(val) if "format" in src else str(val)
            if got != disp:
                fail(f"TYPED NUMBER: slide says {disp!r} but sun_facts.py {src.get('args')} gives {got!r}")
                continue
            backed.append(disp)
        elif "given" in src:
            if len(src["given"].strip()) < 8:
                fail(f"source {disp!r}: 'given' needs a real reason")
                continue
            warn(f"given value {disp!r}: {src['given']}")
            backed.append(disp)
        else:
            fail(f"source {disp!r} has neither 'script' nor 'given'")
    return backed


def check_numbers(texts, backed, where):
    for t in texts:
        t2 = re.sub(r"https?://\S+|apartmentiq\.in|#\w+", " ", norm(t))
        for m in NUM.finditer(t2):
            tok = norm(m.group(0))
            if not any(b == tok or b.startswith(tok + " ") or b.startswith(tok) and not b[len(tok):len(tok) + 1].isdigit()
                       and b[len(tok):len(tok) + 1] not in ".,:" for b in backed):
                fail(f"{where}: number {tok!r} in {t[:60]!r} has no entry in spec.sources")


def check_words(texts, where):
    for t in texts:
        low = " " + re.sub(r"[^a-z0-9#%.& ]+", " ", norm(t).lower()) + " "   # keeps "." for "no. 1"
        words = " " + re.sub(r"[^a-z0-9 ]+", " ", norm(t).lower()) + " "      # words only, for names
        words = re.sub(r"\s+", " ", words)
        for b in BUILDERS:
            if f" {b} " in words:
                fail(f"{where}: names a builder or project ({b!r}) in {t[:60]!r}")
        for b in BUILDER_PHRASES:
            if f" {b} " in words:
                fail(f"{where}: names a builder or project ({b!r}) in {t[:60]!r}")
        for b, why in BANNED.items():
            if b in low:
                fail(f"{where}: banned phrase {b!r} ({why}) in {t[:60]!r}")
        for b in NOT_LIVE:
            if b in low:
                fail(f"{where}: {b!r} is not live in the product; do not claim it")
        for c in OTHER_CITIES:
            if f" {c} " in words:
                warn(f"{where}: mentions {c!r}; the site covers Noida and Gurugram only")
        if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", t):
            warn(f"{where}: contains an emoji; the brand style uses none")


def check_spec(spec):
    fmt = spec.get("format")
    if fmt not in ("carousel", "reel"):
        fail("spec.format must be 'carousel' or 'reel'")
    if not isinstance(spec.get("ai_footage"), bool):
        fail("spec.ai_footage must be true or false")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(spec.get("publish_date", ""))):
        fail("spec.publish_date must be YYYY-MM-DD")
    blob = json.dumps(spec).lower()
    for bad in ("app_screen", "screenshot", "apartmentiq-web", "vercel.app", "screen recording"):
        if bad in blob:
            fail(f"spec mentions {bad!r}: posts never show the app or the website (Rajat, 2026-11-27)")
    if fmt == "carousel":
        sl = spec.get("slides", [])
        if not (3 <= len(sl) <= 8):
            fail("a carousel takes 3 to 8 slides")
        elif sl[0].get("type") != "hook" or sl[-1].get("type") != "end":
            fail("first slide must be type hook, last must be type end")
        # 2026-11-28: a slide may carry a cast picture ("image": "<name>" from ig-kit/cast/cast.json).
        # Those pictures are AI-made, so the post must say so: ai_footage true, and the caption line below.
        pics = [(k + 1, s_.get("type"), s_.get("image")) for k, s_ in enumerate(sl) if s_.get("image")]
        if pics:
            try:
                lib = [c["name"] for c in json.load(open(os.path.join(HERE, "cast", "cast.json"), encoding="utf-8"))["pictures"]]
            except Exception as e:
                lib = []; fail(f"cannot read ig-kit/cast/cast.json: {e}")
            for k, typ, name in pics:
                if name not in lib:
                    fail(f"slide {k}: picture {name!r} is not in the cast library (ig-kit/cast/cast.json)")
                if typ not in ("hook", "scene"):
                    fail(f"slide {k}: only hook and scene slides take a picture, not {typ!r}")
            if not spec.get("ai_footage"):
                fail("carousel uses a cast picture: set ai_footage true (the caption then needs 'Scenes are illustrative.')")
        elif spec.get("ai_footage"):
            fail("carousel has no cast picture: ai_footage must be false")
    if fmt == "reel":
        sc = spec.get("scenes", [])
        if len(sc) < 2:
            fail("a reel needs at least 2 scenes")
        total = sum(s.get("frames", 0) for s in sc) / 24 + spec.get("end_seconds", 5)
        if not (8 <= total <= 45):
            fail(f"reel length {total:.1f} s is outside 8 to 45 s")
        if any("clip" in s for s in sc) and not spec.get("ai_footage"):
            fail("reel uses clips: set ai_footage true")
        first = sc[0] if sc else {}
        if not first.get("lines"):
            fail("the first scene must carry the hook text from frame 1")


CAST = ["Meera", "Kabir", "Dhoop", "Chhaya", "Gutar"]


def check_say(spec):
    """Speech bubbles (2026-11-28). The words are checked like any other text on the post; this checks the shape."""
    for k, part in enumerate(spec.get("slides", []) + spec.get("scenes", []), 1):
        says = part.get("say", [])
        if len(says) > 2:
            fail(f"part {k}: 2 speech bubbles at most")
        for b in says:
            if b.get("who") not in CAST:
                fail(f"part {k}: speaker {b.get('who')!r} is not in the cast ({', '.join(CAST)})")
            if len(str(b.get("text", "")).split()) > 6:
                fail(f"part {k}: a line of speech takes 6 words at most: {b.get('text')!r}")
            if not b.get("text"):
                fail(f"part {k}: a speech bubble has no text")


def check_caption(cap, spec):
    if len(cap) > 2200:
        fail(f"caption is {len(cap)} characters; Instagram's limit is 2,200")
    first = cap.strip().split("\n")[0]
    if len(first) > 125:
        fail(f"first caption line is {len(first)} characters; 125 or fewer shows before 'more'")
    if "apartmentiq.in" not in cap:
        fail("caption must carry the site address apartmentiq.in")
    # 2026-11-27: Notion's rows mode and page fetch return a text field as markup
    # ([apartmentiq.in](http://apartmentiq.in), <br />, \_). That markup must never reach
    # Instagram. Read the Caption with a SQL-mode query, which returns plain text.
    for mark, what in (("](", "a markdown link"), ("<br", "an HTML line break"), ("\\", "a backslash"),
                       ("http://", "a link"), ("https://", "a link")):
        if mark in cap:
            fail(f"caption contains {what} ({mark!r}): Notion markup, not plain text. "
                 "Read the Caption with a SQL-mode query and lint again")
    tags = re.findall(r"#\w+", cap)
    if len(tags) > 10:
        fail(f"{len(tags)} hashtags; at most 10")
    paras = [p for p in cap.strip().split("\n\n") if p.strip()]
    if tags and any("#" in p for p in paras[:-1]):
        fail("hashtags belong only in the last paragraph")
    if "#ApartmentIQ" not in tags and tags:
        warn("no #ApartmentIQ hashtag")
    if spec.get("ai_footage") and "Scenes are illustrative." not in cap:
        fail("post uses AI footage: caption must contain 'Scenes are illustrative.'")
    if "link in bio" in cap.lower():
        warn("'link in bio' only works once the profile link is set in the phone app")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--caption", required=True)
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    cap = open(a.caption, encoding="utf-8").read()
    check_spec(spec)
    check_say(spec)
    backed = check_sources(spec)
    body = list(strings(spec.get("slides", []))) + list(strings(spec.get("scenes", []))) + list(strings(spec.get("end", {})))
    check_numbers(body, backed, "slides")
    check_numbers([cap], backed, "caption")
    check_words(body, "slides")
    check_words([cap], "caption")
    check_caption(cap, spec)
    for w in WARNS:
        print("WARN", w)
    for f in FAILS:
        print("FAIL", f)
    print(f"RESULT {'FAIL' if FAILS else 'PASS'}: {len(FAILS)} fail, {len(WARNS)} warn")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
