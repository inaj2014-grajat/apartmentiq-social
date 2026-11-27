#!/usr/bin/env python3
"""test_kit.py: proves the gate works. Run after ANY change to the kit, before pushing.

  python3 -I ig-kit/test_kit.py

It takes a known-good post, checks that it passes, then plants one fault at a time and
checks that lint_aiq.py REFUSES each one. A gate that has only ever been seen passing
has not been tested (ApartmentIQ rule: simulate before implementing, with a failure path).
"""
import copy, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GOOD_SPEC = {
    "format": "carousel", "pillar": "sun-fact", "publish_date": "2026-12-01", "ai_footage": False,
    "slides": [
        {"type": "hook", "kicker": "SUN FACTS · NOIDA", "title": ["Noon sun in December:", "**38.0°**"], "sub": "Low."},
        {"type": "fact", "kicker": "NOON", "value": "38.0°", "label": "above the horizon", "sub": "21 DEC"},
        {"type": "end", "title": ["See the sun your flat", "**actually gets.**"], "sources": ["NOAA solar equations"]},
    ],
    "sources": [
        {"display": "38.0°", "script": "sun_facts.py", "args": "--place noida --date 2026-12-21",
         "field": "noon_altitude_deg", "format": "{:.1f}°"},
        {"display": "21 DEC", "given": "date label for the fact"},
    ],
}
GOOD_CAP = "The December sun over Noida climbs only 38.0° at noon.\n\nFree sun report: apartmentiq.in\n\n#ApartmentIQ #Noida"


def run(spec, cap):
    with tempfile.TemporaryDirectory() as d:
        json.dump(spec, open(f"{d}/spec.json", "w", encoding="utf-8"), ensure_ascii=False)
        open(f"{d}/caption.txt", "w", encoding="utf-8").write(cap)
        r = subprocess.run([sys.executable, "-I", f"{HERE}/lint_aiq.py", "--spec", f"{d}/spec.json",
                            "--caption", f"{d}/caption.txt"], capture_output=True, text=True)
        return r.returncode, r.stdout


def mutate(fn):
    s = copy.deepcopy(GOOD_SPEC)
    fn(s)
    return s


def typed(s):       s["slides"][1]["value"] = "41.5°"; s["sources"][0]["display"] = "41.5°"
def unsourced(s):   s["slides"][1]["sub"] = "That is 47 degrees lower than June. 47°"
def builder(s):     s["slides"][0]["sub"] = "Ask anyone at DLF."
def app_screen(s):  s["assets"] = [{"type": "app_screen", "url": "x"}]
def not_live(s):    s["slides"][0]["sub"] = "Check the Vastu too."


CASES = [  # name, spec, caption, expected exit code, text that must appear in the output
    ("good post passes", GOOD_SPEC, GOOD_CAP, 0, "RESULT PASS"),
    ("a typed number is refused", mutate(typed), GOOD_CAP.replace("38.0°", "41.5°"), 1, "TYPED NUMBER"),
    ("a number with no source is refused", mutate(unsourced), GOOD_CAP, 1, "has no entry in spec.sources"),
    ("a builder name is refused", mutate(builder), GOOD_CAP, 1, "names a builder"),
    ("an app screen is refused", mutate(app_screen), GOOD_CAP, 1, "never show the app"),
    ("a pillar that is not live is refused", mutate(not_live), GOOD_CAP, 1, "not live"),
    ("a guarantee in the caption is refused", GOOD_SPEC, GOOD_CAP.replace("Free sun report", "Guaranteed sun. Free report"), 1, "banned phrase"),
    ("a caption without the site address is refused", GOOD_SPEC, GOOD_CAP.replace("apartmentiq.in", "our site"), 1, "site address"),
    ("more than 10 hashtags are refused", GOOD_SPEC, GOOD_CAP + " " + " ".join(f"#tag{i}" for i in range(10)), 1, "hashtags"),
    ("a caption read back from Notion as markup is refused", GOOD_SPEC,
     GOOD_CAP.replace("apartmentiq.in", "[apartmentiq.in](http://apartmentiq.in)").replace("\n\n", "<br /><br />", 1), 1, "Notion markup"),
    ("AI footage without the illustrative line is refused",
     {"format": "reel", "publish_date": "2026-12-03", "ai_footage": True, "sources": [],
      "scenes": [{"clip": "a.mp4", "frames": 96, "lines": ["One"]}, {"clip": "b.mp4", "frames": 96, "lines": ["Two"]}]},
     "A reel.\n\napartmentiq.in\n\n#ApartmentIQ", 1, "Scenes are illustrative"),
]

bad = 0
for name, spec, cap, want, needle in CASES:
    code, out = run(spec, cap)
    ok = code == want and needle in out
    bad += not ok
    print(("ok   " if ok else "WRONG"), name, "" if ok else f"\n      exit {code}, wanted {want}; output:\n{out}")
print(f"{len(CASES) - bad}/{len(CASES)} cases behave as expected")
sys.exit(1 if bad else 0)
