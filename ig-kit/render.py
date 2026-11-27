#!/usr/bin/env python3
"""render.py: draw an ApartmentIQ Instagram carousel from spec.json.

USE
  python3 -I ig-kit/render.py instagram/<date>-<slug>/spec.json instagram/<date>-<slug>
Writes 01-<type>.jpg, 02-..., and contact.jpg (all slides side by side at phone size).
ALWAYS open contact.jpg and look at it before pushing. The checks to make by eye are
listed in ig-kit/README.md, section "Look at it".

SPEC (see ig-kit/README.md for a full example)
  {"format": "carousel", "slides": [ {...}, ... ], "sources": [ {...}, ... ]}
Slide types and their fields:
  hook     kicker, title (list of lines), sub
  compare  kicker, title, left {label, value, tone}, right {label, value, tone}, note
  shadow   kicker, title, height_m, items [{label, value, shadow_m, tone}], note
  fact     kicker, value, label, sub
  list     kicker, title, items (3 to 5 short strings)
  end      title (list of lines), cta, url, sources (list of short strings)
Text rules: wrap a word in **double stars** to colour it emerald. Lines in `title`
are drawn as written, one per line: you choose the line breaks. `tone` is "winter"
(blue, 21 Dec) or "summer" (amber, 21 Jun): the product's data colours, never swapped.

The renderer never invents a number. It draws what the spec says. lint_aiq.py is the
step that proves each number came from sun_facts.py.
"""
import json, os, sys, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
M = 84  # outer margin
HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = (11, 31, 51); INK = (11, 31, 51); INK2 = (51, 65, 85); MUTED = (71, 85, 105)
EMER = (52, 211, 153); PRIMARY = (4, 120, 87); ACCENT = (15, 157, 110)
WHITE = (255, 255, 255); SURF = (248, 250, 252); LINE = (226, 232, 240)
ONNAVY = (231, 238, 243); ONNAVY_M = (169, 190, 201)
TONE = {"winter": (3, 105, 161), "summer": (180, 83, 9)}


def F(weight, size):
    return ImageFont.truetype(f"{HERE}/fonts/Inter-{weight}.otf", size)


def MONO(weight, size):
    return ImageFont.truetype(f"{HERE}/fonts/IBMPlexMono-{weight}.ttf", size)


def diamond(size, ring):
    s = size * 4; k = s / 64
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([13 * k, 13 * k, 51 * k, 51 * k], radius=5 * k, fill=ACCENT)
    sh = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([32 * k, 13 * k, 51 * k, 51 * k], radius=5 * k, fill=(8, 19, 30, 56))
    im = Image.alpha_composite(im, sh)
    ImageDraw.Draw(im).rounded_rectangle([13 * k, 13 * k, 51 * k, 51 * k], radius=5 * k, outline=ring, width=int(2.4 * k))
    return im.rotate(45, resample=Image.BICUBIC).resize((size, size), Image.LANCZOS)


def spans(text, base, accent):
    """'a **b** c' -> [('a ', base), ('b', accent), (' c', base)]"""
    out = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            out.append((part, accent if i % 2 else base))
    return out


def text_w(d, sp, font):
    return sum(d.textlength(t, font=font) for t, _ in sp)


def draw_line(d, x, y, sp, font):
    for t, col in sp:
        d.text((x, y), t, font=font, fill=col)
        x += d.textlength(t, font=font)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t.replace("**", ""), font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(d, x, y, text, font, fill, tr):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
    return x


def frame(dark, kicker, idx, total):
    """Background, brand lockup, kicker, page counter. Returns image and draw."""
    im = Image.new("RGBA", (W, H), (NAVY if dark else SURF) + (255,))
    if dark:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([W - 620, -260, W + 260, 620], fill=ACCENT + (64,))
        im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(200)))
    d = ImageDraw.Draw(im)
    fg = WHITE if dark else INK
    im.alpha_composite(diamond(44, ONNAVY if dark else NAVY), (M - 6, M - 8))
    d = ImageDraw.Draw(im)
    f = F("Bold", 30)
    x = M + 46
    d.text((x, M - 2), "APARTMENT", font=f, fill=fg)
    d.text((x + d.textlength("APARTMENT", font=f), M - 2), "IQ", font=f, fill=EMER if dark else ACCENT)
    if kicker:
        fm = MONO("SemiBold", 26)
        tw = sum(d.textlength(c, font=fm) + 2.6 for c in kicker)
        tracked(d, W - M - tw, M + 2, kicker, fm, ONNAVY_M if dark else MUTED, 2.6)
    fm = MONO("Medium", 26)
    d.text((M, H - M - 22), f"{idx:02d} / {total:02d}", font=fm, fill=ONNAVY_M if dark else MUTED)
    if idx < total:
        t = "SWIPE"
        tw = sum(d.textlength(c, font=fm) + 3 for c in t)
        x2 = tracked(d, W - M - tw - 46, H - M - 22, t, fm, ONNAVY_M if dark else MUTED, 3)
        ay = H - M - 6
        col = EMER if dark else ACCENT
        d.line([x2 + 8, ay, x2 + 40, ay], fill=col, width=4)
        d.line([x2 + 28, ay - 11, x2 + 40, ay, x2 + 28, ay + 11], fill=col, width=4, joint="curve")
    return im, d


def title_block(d, lines, y, size, base, accent, lh=1.12, weight="ExtraBold"):
    f = F(weight, size)
    for ln in lines:
        sp = spans(ln, base, accent)
        assert text_w(d, sp, f) <= W - 2 * M, f"title line too wide at {size}px: {ln!r}"
        draw_line(d, M, y, sp, f)
        y += int(size * lh)
    return y


def para(d, text, y, size, fill, accent, width=W - 2 * M, weight="Medium", lh=1.36):
    f = F(weight, size)
    for ln in wrap(d, text, f, width):
        draw_line(d, M, y, spans(ln, fill, accent), f)
        y += int(size * lh)
    return y


def s_hook(s, i, n):
    im, d = frame(True, s.get("kicker"), i, n)
    size = s.get("size", 104)
    total = len(s["title"]) * int(size * 1.12)
    y = (H - total) // 2 - 60
    y = title_block(d, s["title"], y, size, WHITE, EMER)
    if s.get("sub"):
        para(d, s["sub"], y + 36, 46, ONNAVY, EMER)
    return im


STAT_H = 440


def stat(d, x, y, w, label, value, tone):
    col = TONE[tone]
    d.rounded_rectangle([x, y, x + w, y + STAT_H], radius=28, fill=WHITE, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + 14, y + STAT_H], radius=7, fill=col)
    tracked(d, x + 46, y + 56, label, MONO("SemiBold", 36), col, 3.5)
    f = F("ExtraBold", 170)
    while d.textlength(value, font=f) > w - 84:
        f = F("ExtraBold", f.size - 6)
    d.text((x + 40, y + 150), value, font=f, fill=INK)


def s_compare(s, i, n):
    im, d = frame(False, s.get("kicker"), i, n)
    y = title_block(d, s["title"], 250, s.get("size", 78), INK, PRIMARY)
    y += 64
    w = (W - 2 * M - 36) // 2
    stat(d, M, y, w, s["left"]["label"], s["left"]["value"], s["left"]["tone"])
    stat(d, M + w + 36, y, w, s["right"]["label"], s["right"]["value"], s["right"]["tone"])
    if s.get("note"):
        end = para(d, s["note"], y + STAT_H + 64, 46, INK2, PRIMARY)
        assert end < H - M - 50, "compare slide note runs into the page counter: shorten it"
    return im


def s_shadow(s, i, n):
    """Tower and its noon shadows, drawn to scale from the numbers in the spec."""
    im, d = frame(False, s.get("kicker"), i, n)
    y = title_block(d, s["title"], 250, s.get("size", 78), INK, PRIMARY)
    top = y + 50
    box_h = 580
    d.rounded_rectangle([M, top, W - M, top + box_h], radius=28, fill=WHITE, outline=LINE, width=2)
    hm = float(s["height_m"])
    longest = max(float(it["shadow_m"]) for it in s["items"])
    tower_w = 64
    x0 = M + 70
    ground = top + box_h - 210
    scale = min((W - 2 * M - 70 - tower_w - 70) / longest, (box_h - 300) / hm)  # px per metre, same both axes
    th = hm * scale
    d.line([M + 30, ground, W - M - 30, ground], fill=INK2, width=4)
    d.rectangle([x0, ground - th, x0 + tower_w, ground], fill=(203, 213, 225), outline=INK, width=3)
    for k in range(1, 9):  # floor lines, decoration only
        yy = ground - th * k / 9
        d.line([x0 + 8, yy, x0 + tower_w - 8, yy], fill=(148, 163, 184), width=2)
    fm = MONO("SemiBold", 30)
    tracked(d, x0 - 8, ground - th - 50, f"{int(hm)} M", fm, INK2, 2)
    for j, it in enumerate(s["items"]):
        col = TONE[it["tone"]]
        sx = x0 + tower_w + float(it["shadow_m"]) * scale
        yb = ground + 24 + j * 86
        d.line([x0 + tower_w, ground - th, sx, ground], fill=col, width=5)       # sun ray over the roof edge
        d.rounded_rectangle([x0 + tower_w, yb, max(sx, x0 + tower_w + 12), yb + 20], radius=10, fill=col)
        tracked(d, x0 + tower_w, yb + 28, f"{it['label']}  {it['value']}", fm, col, 1.5)
    if s.get("note"):
        end = para(d, s["note"], top + box_h + 40, 42, INK2, PRIMARY)
        assert end < H - M - 50, "shadow slide note runs into the page counter: shorten it"
    return im


def s_fact(s, i, n):
    im, d = frame(False, s.get("kicker"), i, n)
    f = F("ExtraBold", 250)
    while d.textlength(s["value"], font=f) > W - 2 * M:
        f = F("ExtraBold", f.size - 10)
    d.text((M - 6, 330), s["value"], font=f, fill=PRIMARY)
    y = 330 + int(f.size * 1.16)
    y = para(d, s["label"], y, 58, INK, PRIMARY, weight="Bold", lh=1.22)
    if s.get("sub"):
        para(d, s["sub"], y + 34, 42, INK2, PRIMARY)
    return im


def s_list(s, i, n):
    im, d = frame(False, s.get("kicker"), i, n)
    y = title_block(d, s["title"], 250, s.get("size", 78), INK, PRIMARY) + 70
    assert 3 <= len(s["items"]) <= 5, "a list slide takes 3 to 5 items"
    for k, item in enumerate(s["items"], 1):
        d.ellipse([M, y + 2, M + 72, y + 74], fill=NAVY)
        num = str(k); fn = F("Bold", 38)
        d.text((M + 36 - d.textlength(num, font=fn) / 2, y + 14), num, font=fn, fill=WHITE)
        f = F("SemiBold", 52)
        yy = y
        for ln in wrap(d, item, f, W - 2 * M - 108):
            draw_line(d, M + 108, yy + 4, spans(ln, INK, PRIMARY), f)
            yy += 68
        y = max(yy, y + 74) + 56
    assert y < H - M - 40, "list slide overflows: shorten the items"
    return im


def s_end(s, i, n):
    im, d = frame(True, None, i, n)
    y = title_block(d, s["title"], 330, s.get("size", 84), WHITE, EMER)
    f = F("Bold", 44)
    t = s.get("cta", "Free report during pre-launch")
    w = d.textlength(t, font=f)
    y += 50
    d.rounded_rectangle([M, y, M + w + 88, y + 96], radius=48, fill=ACCENT)
    d.text((M + 44, y + 22), t, font=f, fill=WHITE)
    y += 96 + 46
    tracked(d, M, y, "NOIDA · GURUGRAM", MONO("SemiBold", 32), ONNAVY, 4)
    d.text((M, y + 62), s.get("url", "apartmentiq.in"), font=F("ExtraBold", 80), fill=WHITE)
    fs = F("Medium", 28)
    yy = H - M - 70 - 40 * len(s.get("sources", []))
    for src in s.get("sources", []):
        assert d.textlength(src, font=fs) <= W - 2 * M, f"source line too long: {src!r}"
        d.text((M, yy), src, font=fs, fill=ONNAVY_M)
        yy += 40
    return im


DRAW = {"hook": s_hook, "compare": s_compare, "shadow": s_shadow, "fact": s_fact, "list": s_list, "end": s_end}


def main(spec_path, out_dir):
    spec = json.load(open(spec_path, encoding="utf-8"))
    slides = spec["slides"]
    assert 3 <= len(slides) <= 8, "a carousel takes 3 to 8 slides"
    assert slides[0]["type"] == "hook" and slides[-1]["type"] == "end", "first slide is a hook, last is the end card"
    os.makedirs(out_dir, exist_ok=True)
    rev = spec.get("revision", 1)
    suffix = "" if rev == 1 else f"-r{rev}"
    names, thumbs = [], []
    for i, s in enumerate(slides, 1):
        im = DRAW[s["type"]](s, i, len(slides)).convert("RGB")
        name = f"{i:02d}-{s['type']}{suffix}.jpg"
        im.save(os.path.join(out_dir, name), quality=92)
        names.append(name); thumbs.append(im.resize((390, 488), Image.LANCZOS))
    sheet = Image.new("RGB", (390 * len(thumbs) + 12 * (len(thumbs) + 1), 488 + 24), (30, 41, 59))
    for k, t in enumerate(thumbs):
        sheet.paste(t, (12 + k * 402, 12))
    sheet.save(os.path.join(out_dir, "contact.jpg"), quality=88)
    print(json.dumps({"slides": names, "contact": "contact.jpg"}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
