#!/usr/bin/env python3
"""reel.py: build an ApartmentIQ reel from clips + spec.json. This is the method used for
the first reel ("March vs December", 2026-11-27), turned into a script.

USE
  python3 -I ig-kit/reel.py instagram/<date>-<slug>/spec.json instagram/<date>-<slug>
Needs ffmpeg. Reads the clips named in the spec (paths relative to the spec's folder).
Writes reel.mp4 (1080x1920, 24 fps, H.264 + AAC), contact.jpg (one frame per caption at
phone width) and build.json. LOOK AT contact.jpg before pushing.

HOW IT IS BUILT, AND WHY
- Clips from Google Flow are 24 fps, so the reel is 24 fps. Converting to 30 makes slow
  camera moves judder.
- One encoded file per scene with identical settings, joined with ffmpeg's concat
  demuxer and "-c copy". A caption change then re-renders one scene, not the film.
- Captions are drawn by this script, never by the video model: AI footage cannot spell.
  Each scene gets a soft navy band behind its caption only, so the picture stays clean
  and Flow's own watermark (bottom right) is never covered. Never crop or cover it.
- Scene lengths must be multiples of 12 frames (0.5 s) so every cut lands on the music's
  beat (120 bpm).
- Caption on screen from frame 1 of scene 1 (the hook). Later captions fade in 0.12 s
  after the cut and slide up 26 px.
- Sound = an original music bed made in code (no licence needed) + each clip's own room
  sound underneath, normalised to about -15 LUFS.

SPEC (reel)
  {"format": "reel", "ai_footage": true, "publish_date": "...", "slug": "...",
   "scenes": [
     {"clip": "clips/s1.mp4", "in": 0.5, "frames": 72, "position": "top"|"low",
      "chip": "SITE VISIT · MARCH · 11 AM", "lines": ["You saw the flat", "in **March.**"],
      "sub": null, "size": 96, "mark": false, "mood": "bright"|"dark"|"build"|"warm",
      "ambience_db": 10, "then": {"at": 3.3, "chip": ..., "lines": [...], "sub": ...}}],
   "end": {"title": ["See the sun your flat", "**actually gets.**"],
           "cta": "Free report during pre-launch", "cities": "NOIDA · GURUGRAM",
           "url": "apartmentiq.in",
           "footnote": ["Scenes are illustrative.", "Report numbers come from our 3D sun model."]},
   "end_seconds": 5, "sources": [...]}
"position": "top" when the subject or the light you want seen is in the lower half.
"then" swaps to a second caption inside the same scene (used for a two-part sentence).
"say": up to 2 speech bubbles in a scene. Each pops in at "at" seconds and stays to the cut:
  [{"who": "Dhoop", "text": "Where is my sun?", "at": 0.9, "tip": [330, 1290], "box": [340, 1185]}]
  tip = the speaker's head, box = the bubble's centre, in pixels of the 1080x1920 frame. Find them by
  pulling a frame at that moment and looking: the animals move. 6 words at most. Keep bubbles below
  y 590 when the caption is at the top, and out of the bottom right corner (Flow's mark).
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import F, MONO, diamond, spans, text_w, draw_line, bubble, NAVY, EMER, ACCENT, WHITE, ONNAVY, ONNAVY_M  # noqa: E402

W, H, FPS = 1080, 1920, 24
TOP, LOW = 400, 1350
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an"]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd[:12]) + " ...\n" + r.stderr[-1500:])


# ---------- caption layers ----------
def scrim(cy, half, strength):
    g = Image.new("L", (1, H), 0); px = g.load()
    for y in range(H):
        t = abs(y - cy) / half
        if t < 1:
            px[0, y] = int(strength * (0.5 + 0.5 * math.cos(math.pi * t)) ** 0.9)
    im = Image.new("RGBA", (W, H), NAVY + (0,)); im.putalpha(g.resize((W, H)))
    return im


def chip(im, text, cy, mark):
    d = ImageDraw.Draw(im); f = MONO("SemiBold", 35); tr = 3.4
    tw = sum(d.textlength(c, font=f) + tr for c in text) - tr
    lead = 48 if mark else 32
    w = tw + 34 + lead + 12; x0 = (W - w) / 2; h = 70
    d.rounded_rectangle([x0, cy - h / 2, x0 + w, cy + h / 2], radius=h / 2, fill=NAVY + (235,), outline=(255, 255, 255, 46), width=2)
    if mark:
        im.alpha_composite(diamond(40, ONNAVY), (int(x0 + 18), int(cy - 20)))
    else:
        d.ellipse([x0 + 24, cy - 8, x0 + 40, cy + 8], fill=EMER)
    x = x0 + 18 + lead
    for ch in text:
        d.text((x, cy - 24), ch, font=f, fill=ONNAVY); x += d.textlength(ch, font=f) + tr


def caption(c, cy):
    size = c.get("size", 88); f = F("ExtraBold", size); lh = int(size * 1.12)
    lines = [spans(l, WHITE, EMER) for l in c["lines"]]
    total = len(lines) * lh + (70 if c.get("sub") else 0); y0 = cy - total // 2
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shd = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); ds = ImageDraw.Draw(shd)
    for i, sp in enumerate(lines):
        w = text_w(d, sp, f)
        assert w <= 960, f"caption line too wide ({int(w)} px > 960) at size {size}: {c['lines'][i]!r}"
        draw_line(ds, (W - w) / 2, y0 + i * lh + 4, [(t, (4, 12, 22, 190)) for t, _ in sp], f)
    im = Image.alpha_composite(shd.filter(ImageFilter.GaussianBlur(10)), im); d = ImageDraw.Draw(im)
    for i, sp in enumerate(lines):
        draw_line(d, (W - text_w(d, sp, f)) / 2, y0 + i * lh, sp, f)
    if c.get("sub"):
        fs = F("SemiBold", 40); w = d.textlength(c["sub"], font=fs)
        assert w <= 960, f"sub line too wide: {c['sub']!r}"
        d.text(((W - w) / 2, y0 + len(lines) * lh + 22), c["sub"], font=fs, fill=ONNAVY)
    if c.get("chip"):
        chip(im, c["chip"], y0 - 70, c.get("mark", False))
    return im


def end_card(e):
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([140, 300, 940, 1100], fill=ACCENT + (70,))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(190)))
    im.alpha_composite(diamond(190, ONNAVY), ((W - 190) // 2, 430)); d = ImageDraw.Draw(im)

    def centre(y, sp, font, tr=0.0):
        w = sum(d.textlength(ch, font=font) + tr for t, _ in sp for ch in t) - tr
        x = (W - w) / 2
        for t, col in sp:
            for ch in t:
                d.text((x, y), ch, font=font, fill=col); x += d.textlength(ch, font=font) + tr
    centre(660, [("APARTMENT", WHITE), ("IQ", EMER)], F("Bold", 96), -1.9)
    centre(782, [("APARTMENT INTELLIGENCE", ONNAVY_M)], MONO("Medium", 30), 4.8)
    for i, l in enumerate(e["title"]):
        centre(930 + i * 86, spans(l, WHITE, EMER), F("ExtraBold", 74))
    fp = F("Bold", 42); t = e.get("cta", "Free report during pre-launch"); w = d.textlength(t, font=fp)
    d.rounded_rectangle([(W - w) / 2 - 44, 1180, (W + w) / 2 + 44, 1272], radius=46, fill=ACCENT)
    d.text(((W - w) / 2, 1200), t, font=fp, fill=WHITE)
    centre(1318, [(e.get("cities", "NOIDA · GURUGRAM"), ONNAVY)], MONO("SemiBold", 34), 5)
    centre(1412, [(e.get("url", "apartmentiq.in"), WHITE)], F("ExtraBold", 84))
    for i, t in enumerate(e.get("footnote", [])):
        centre(1560 + i * 42, [(t, ONNAVY_M)], F("Medium", 30))
    return im.convert("RGB")


# ---------- picture ----------
def still(idx, dur):
    return f"[{idx}:v]format=rgba,loop=loop=-1:size=1:start=0,setpts=N/({FPS}*TB),trim=duration={dur}"


def build_scene(k, sc, src_dir, work, first, last):
    frames = sc["frames"]; dur = frames / FPS
    assert frames % 12 == 0, f"scene {k + 1}: frames must be a multiple of 12 (0.5 s) so cuts land on the beat"
    top = sc.get("position", "low") == "top"; cy = TOP if top else LOW
    (scrim(cy - 20, 400, 150) if top else scrim(cy, 360, 176)).save(f"{work}/scrim{k}.png")
    caps = [(sc, None if first else 0.12, None)]
    if sc.get("then"):
        t = sc["then"]["at"]; caps = [(sc, None if first else 0.12, t - 0.3), (sc["then"], t, None)]
    inputs = ["-ss", str(sc.get("in", 0)), "-i", os.path.join(src_dir, sc["clip"]), "-framerate", str(FPS), "-i", f"{work}/scrim{k}.png"]
    g = [f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v0]", still(1, dur) + "[sc]", "[v0][sc]overlay=format=auto[v1]"]
    lastv = "v1"
    for i, (c, t_in, t_out) in enumerate(caps):
        caption(c, cy).save(f"{work}/cap{k}_{i}.png")
        inputs += ["-framerate", str(FPS), "-i", f"{work}/cap{k}_{i}.png"]
        f = still(2 + i, dur)
        if t_in is not None:
            f += f",fade=t=in:st={t_in}:d=0.28:alpha=1"
        if t_out is not None:
            f += f",fade=t=out:st={t_out}:d=0.22:alpha=1"
        g.append(f + f"[c{i}]")
        y = "0" if t_in is None else f"if(lt(t,{t_in}),26,if(lt(t,{t_in + 0.28}),26*(1-(t-{t_in})/0.28),0))"
        g.append(f"[{lastv}][c{i}]overlay=x=0:y='{y}':format=auto[v{2 + i}]"); lastv = f"v{2 + i}"
    # speech bubbles (2026-11-28): each pops in at its "at" time and stays to the end of the scene
    says = sc.get("say", [])
    assert len(says) <= 2, f"scene {k + 1}: 2 speech bubbles at most"
    for j, b in enumerate(says):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        x0, y0, x1, y1 = bubble(layer, b["who"], b["text"], tuple(b["tip"]), tuple(b["box"]), 52, keep_out=(840, 1640, W, H))
        if top:
            assert y0 > 590, f"scene {k + 1}: speech bubble {b['text']!r} sits in the caption band at the top: move its box down"
        assert 0.2 <= b["at"] <= dur - 1.2, f"scene {k + 1}: speech bubble {b['text']!r} needs at least 1.2 s on screen"
        layer.save(f"{work}/say{k}_{j}.png")
        idx = 2 + len(caps) + j
        inputs += ["-framerate", str(FPS), "-i", f"{work}/say{k}_{j}.png"]
        t = b["at"]
        g.append(still(idx, dur) + f",fade=t=in:st={t}:d=0.16:alpha=1[b{j}]")
        y = f"if(lt(t,{t}),18,if(lt(t,{t + 0.16}),18*(1-(t-{t})/0.16),0))"
        g.append(f"[{lastv}][b{j}]overlay=x=0:y='{y}':format=auto[w{j}]"); lastv = f"w{j}"
    tail = f"[{lastv}]format=yuv420p"
    if last:
        tail += f",fade=t=out:st={dur - 0.35}:d=0.35:color=0x0b1f33"
    g.append(tail + "[out]")
    out = f"{work}/s{k}.mp4"
    sh(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(g), "-map", "[out]", "-frames:v", str(frames)] + ENC + [out])
    return out


# ---------- music: an original bed, 120 bpm, cuts on the half-second grid ----------
SR = 48000
CHORDS = {"bright": [48, 55, 64, 67, 71, 74], "dark": [33, 45, 52, 57, 60], "build": [45, 52, 55, 60, 64],
          "warm": [36, 48, 55, 60, 64, 67], "end": [36, 48, 55, 64, 67, 71, 74]}
ARPS = {"bright": [72, 76, 79, 83, 84, 88, 91, 88], "dark": [57, None, None, None, 60, None, None, None],
        "build": [69, 72, 76, 79, 76, 72, 69, 72], "warm": [76, 79, 84, 83, 79, 81, 84, 88], "end": [84, 79, 86, None, 88, 91, 96, None]}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pluck(m, dur=1.6):
    t = np.arange(int(dur * SR)) / SR; f = hz(m); s = np.zeros_like(t)
    for k in range(1, 9):
        if f * k > 9000:
            break
        s += 1 / k ** 1.6 * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.2 + 1.3 * k))
    return s * np.minimum(1, t / 0.004)


def pad(notes, dur, rng):
    n = int((dur + 0.9) * SR); t = np.arange(n) / SR; l = np.zeros(n); r = np.zeros(n)
    for m in notes:
        for det, side in ((-0.0035, -1), (0.0035, 1), (0.0, 0)):
            ph = rng.uniform(0, 6.28); s = sum(0.55 ** (k - 1) / k * np.sin(2 * np.pi * hz(m) * (1 + det) * k * t + ph * k) for k in range(1, 6) if hz(m) * k < 5000)
            if side <= 0: l += s
            if side >= 0: r += s
    env = np.minimum(1, t / 0.3) * np.minimum(1, np.maximum(0, (dur + 0.9 - t) / 0.9)) / len(notes)
    return l * env, r * env


def thump(deep):
    t = np.arange(int((2.0 if deep else 0.35) * SR)) / SR
    f = (38 + 48 * np.exp(-t * 9)) if deep else (46 + 70 * np.exp(-t * 28))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (2.2 if deep else 11))


def music(scenes, end_s, path):
    rng = np.random.default_rng(7); total = sum(s["frames"] for s in scenes) / FPS + end_s
    n = int(total * SR); L = np.zeros(n); R = np.zeros(n)

    def add(sig, t0, gain, pan=0.0):
        i = int(t0 * SR)
        if i < n:
            m = min(len(sig), n - i)
            L[i:i + m] += gain * math.sqrt(0.5 * (1 - pan)) * sig[:m]; R[i:i + m] += gain * math.sqrt(0.5 * (1 + pan)) * sig[:m]
    t0 = 0.0
    parts = [(s.get("mood", "build"), s["frames"] / FPS) for s in scenes] + [("end", end_s)]
    for idx, (mood, dur) in enumerate(parts):
        pl, pr = pad(CHORDS[mood], dur, rng); i = int(t0 * SR); m = min(len(pl), n - i)
        L[i:i + m] += 0.22 * pl[:m]; R[i:i + m] += 0.22 * pr[:m]
        if idx:
            add(thump(mood in ("dark", "warm")), t0, 0.5 if mood == "dark" else 0.32)
        add(pluck(CHORDS[mood][0], 2.5), t0, 0.3)
        for j in range(int(round(dur / 0.25))):
            note = ARPS[mood][j % 8]
            if note:
                add(pluck(note, 1.2), t0 + j * 0.25, 0.17 if mood != "dark" else 0.2, 0.45 * math.sin(j * 1.7))
        if mood in ("build", "warm"):
            for j in range(int(dur / 0.5)):
                add(thump(False), t0 + j * 0.5, 0.3)
        t0 += dur
    tt = np.arange(int(1.8 * SR)) / SR; ir = rng.standard_normal((2, len(tt))) * np.exp(-tt * 3.4)
    ir = sosfilt(butter(2, 5200, "low", fs=SR, output="sos"), ir, axis=1); ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    L = L + 0.3 * fftconvolve(L, ir[0])[:n]; R = R + 0.3 * fftconvolve(R, ir[1])[:n]
    hp = butter(2, 28, "high", fs=SR, output="sos"); L, R = sosfilt(hp, L), sosfilt(hp, R)
    t = np.arange(n) / SR; fade = np.minimum(1, np.maximum(0, (total - t) / 1.6)) ** 1.5 * np.minimum(1, t / 0.01)
    st = np.tanh(np.stack([L * fade, R * fade], axis=1) * 1.6) / 1.6; st = st / np.abs(st).max() * 0.89
    wavfile.write(path, SR, (st * 32767).astype(np.int16))
    return total


# ---------- main ----------
def main(spec_path, out_dir):
    spec = json.load(open(spec_path, encoding="utf-8")); src = os.path.dirname(os.path.abspath(spec_path))
    scenes = spec["scenes"]; end_s = spec.get("end_seconds", 5)
    work = os.path.join(out_dir, "_work"); os.makedirs(work, exist_ok=True)
    files = [build_scene(k, sc, src, work, k == 0, k == len(scenes) - 1) for k, sc in enumerate(scenes)]
    end_card(spec["end"]).save(f"{work}/end.png")
    sh(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{work}/end.png", "-filter_complex",
        f"[0:v]format=yuv420p,loop=loop=-1:size=1:start=0,setpts=N/({FPS}*TB),trim=duration={end_s},fade=t=in:st=0:d=0.35:color=0x0b1f33[out]",
        "-map", "[out]", "-frames:v", str(int(end_s * FPS))] + ENC + [f"{work}/end.mp4"])
    open(f"{work}/list.txt", "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files + [f"{work}/end.mp4"]))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt", "-c", "copy", f"{work}/picture.mp4"])
    total = music(scenes, end_s, f"{work}/music.wav")
    amb = []
    for k, sc in enumerate(scenes):
        d = sc["frames"] / FPS; o = f"{work}/amb{k}.wav"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", str(sc.get("in", 0)), "-t", str(d), "-i", os.path.join(src, sc["clip"]), "-vn", "-af",
            f"aresample=48000,volume={sc.get('ambience_db', 0)}dB,afade=t=in:d=0.04,afade=t=out:st={d - 0.06}:d=0.06,apad=whole_dur={d},atrim=duration={d}",
            "-ac", "2", "-c:a", "pcm_s16le", o]); amb.append(o)
    sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-t", str(end_s), "-i", "anullsrc=r=48000:cl=stereo", "-c:a", "pcm_s16le", f"{work}/ambend.wav"])
    open(f"{work}/amb.txt", "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in amb + [f"{work}/ambend.wav"]))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/amb.txt", "-c", "copy", f"{work}/amb.wav"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/music.wav", "-i", f"{work}/amb.wav", "-filter_complex",
        "[0:a]volume=-5dB[m];[1:a]volume=-6dB[a];[m][a]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000[o]",
        "-map", "[o]", "-t", str(total), "-c:a", "pcm_s16le", f"{work}/mix.wav"])
    rev = spec.get("revision", 1); name = "reel.mp4" if rev == 1 else f"reel-r{rev}.mp4"
    tmp = os.path.join(out_dir, "reel.tmp.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/picture.mp4", "-i", f"{work}/mix.wav", "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", tmp])
    os.replace(tmp, os.path.join(out_dir, name))
    # contact sheet: one frame from the middle of each caption, plus the end card
    times, t0 = [], 0.0
    for sc in scenes:
        d = sc["frames"] / FPS
        times += [t0 + min(1.0, d / 2)] + ([t0 + (sc["then"]["at"] + d) / 2] if sc.get("then") else [])
        t0 += d
    times.append(t0 + end_s / 2); thumbs = []
    for i, t in enumerate(times):
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", os.path.join(out_dir, name), "-frames:v", "1", "-vf", "scale=390:-2", f"{work}/f{i}.jpg"])
        thumbs.append(Image.open(f"{work}/f{i}.jpg"))
    sheet = Image.new("RGB", (390 * len(thumbs), thumbs[0].size[1]))
    for i, th in enumerate(thumbs):
        sheet.paste(th, (i * 390, 0))
    sheet.save(os.path.join(out_dir, "contact.jpg"), quality=88)
    json.dump({"file": name, "seconds": round(total, 2), "scenes": len(scenes), "frame_times": times}, open(os.path.join(out_dir, "build.json"), "w"))
    print(json.dumps({"reel": name, "seconds": round(total, 2), "contact": "contact.jpg"}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
