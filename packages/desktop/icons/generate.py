#!/usr/bin/env python3
"""Regenerate every appycode brand icon asset from one 1024px master.

Brand: navy canvas (#0e3a53, --primary) with an amber geometric lowercase
"a" mark (#c8873c, --accent-bright). Outputs mirror the committed set:
  - icons/app-icon.png                      1024 master (source of truth)
  - icons/{dev,beta,prod}/*                 desktop + tauri ladder (identical)
  - app/public/favicon-{v3,v1}.{png,svg,ico}

Pure stdlib: analytic-SDF rasterization, pyramid/area resampling, ICNS and
PNG-based ICO encoders. Big Sur icns members are premultiplied composites
(squircle + soft analytic shadow) per the premultiplication note in
icons/README.md.
"""
import math
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
APP_PUBLIC = os.path.normpath(os.path.join(HERE, "../../app/public"))

BG = (0x0E, 0x3A, 0x53)   # --primary
FG = (0xC8, 0x87, 0x3C)   # --accent-bright (frame)
DOT = (0xF6, 0xEC, 0xE0)  # --accent-tint (badge)
MASTER = 1024
FRAME_EXT = 260.0         # outer half-extent of the rounded frame ring
FRAME_T = 96.0            # ring thickness
FRAME_R = 150.0           # outer corner radius
DOT_CX, DOT_CY, DOT_R = 708.0, 708.0, 90.0
CX = CY = 512.0
SQUIRCLE_CONTENT = 824 / 1024
SQUIRCLE_R = 185.4 / 824  # corner radius as a fraction of the content side
SH_ALPHA, SH_SPREAD, SH_LIFT = 0.22, 0.022, 0.004  # shadow, as target-size fractions


def cov(sd, aa=0.75):
    """Analytic coverage from a signed distance (aa = half the smoothing band)."""
    if sd <= -aa:
        return 1.0
    if sd >= aa:
        return 0.0
    return 0.5 - sd / (2 * aa)


def sil_sd(px, py, half, r):
    """Rounded-square signed distance; half-extent `half`, corner radius `r`."""
    qx = abs(px) - (half - r)
    qy = abs(py) - (half - r)
    return min(max(qx, qy), 0.0) + math.hypot(max(qx, 0.0), max(qy, 0.0)) - r


# ---------------------------------------------------------------- rendering

def letter_draw(size):
    """Opaque master: navy full bleed, rounded frame ring + badge dot."""
    bg3 = bytes(BG)
    buf = bytearray(size * size * 4)
    for i in range(0, len(buf), 4):
        buf[i : i + 3] = bg3
        buf[i + 3] = 255
    scale = size / MASTER
    ext, thick, rad = FRAME_EXT * scale, FRAME_T * scale, FRAME_R * scale
    r_in = max(1.0, rad - thick)
    fcy, fcx = CY * scale, CX * scale
    dcx, dcy, dr = DOT_CX * scale, DOT_CY * scale, DOT_R * scale
    aa = 0.75 * scale
    for y in range(size):
        py = y + 0.5 - fcy
        for x in range(size):
            px = x + 0.5 - fcx
            sd_out = sil_sd(px, py, ext, rad)
            sd_in = sil_sd(px, py, ext - thick, r_in)
            sd_frame = max(sd_out, -sd_in)
            dd = math.hypot(px - (dcx - CX * scale) , py - (dcy - CY * scale))
            sd_dot = dd - dr
            cf = cov(sd_frame, aa)
            if cf <= 0 and sd_dot >= aa:
                continue
            # frame over canvas, then dot over frame (badge stays a full circle)
            r0 = BG[0] + (FG[0] - BG[0]) * cf
            g0 = BG[1] + (FG[1] - BG[1]) * cf
            b0 = BG[2] + (FG[2] - BG[2]) * cf
            cd = cov(sd_dot, aa)
            i = 4 * (y * size + x)
            buf[i] = round(DOT[0] * cd + r0 * (1 - cd))
            buf[i + 1] = round(DOT[1] * cd + g0 * (1 - cd))
            buf[i + 2] = round(DOT[2] * cd + b0 * (1 - cd))
    return bytes(buf)


def resample(rgba, size, target):
    """Downscale by exact halving plus one bounded weighted step (ratio<=2)."""
    if target > size:
        raise ValueError("only downscaling supported")
    cur, cur_size = rgba, size
    while cur_size // target >= 2:
        half = cur_size // 2
        out = bytearray(half * half * 4)
        for y in range(half):
            b0 = (2 * y) * cur_size * 4
            b1 = b0 + cur_size * 4
            o = y * half * 4
            for x in range(half):
                i0 = b0 + 8 * x
                i1 = b1 + 8 * x
                for c in range(4):
                    out[o + 4 * x + c] = (
                        cur[i0 + c] + cur[i0 + 4 + c] + cur[i1 + c] + cur[i1 + 4 + c] + 2
                    ) >> 2
        cur, cur_size = bytes(out), half
    if cur_size == target:
        return cur
    scale = cur_size / target
    out = bytearray(target * target * 4)
    for ty in range(target):
        fy0, fy1 = ty * scale, (ty + 1) * scale
        y0, y1 = int(fy0), min(int(fy1) + 1, cur_size)
        for tx in range(target):
            fx0, fx1 = tx * scale, (tx + 1) * scale
            x0, x1 = int(fx0), min(int(fx1) + 1, cur_size)
            ar = ag = ab = aa_ = ws = 0.0
            for sy in range(y0, y1):
                wy = min(fy1, sy + 1) - max(fy0, sy)
                if wy <= 0:
                    continue
                rowi = sy * cur_size * 4
                for sx in range(x0, x1):
                    wx = min(fx1, sx + 1) - max(fx0, sx)
                    if wx <= 0:
                        continue
                    w = wx * wy
                    i = rowi + 4 * sx
                    ar += w * cur[i]
                    ag += w * cur[i + 1]
                    ab += w * cur[i + 2]
                    aa_ += w * cur[i + 3]
                    ws += w
            t = 4 * (ty * target + tx)
            if ws:
                out[t] = round(ar / ws)
                out[t + 1] = round(ag / ws)
                out[t + 2] = round(ab / ws)
                out[t + 3] = round(aa_ / ws)
    return bytes(out)


def square(size, master, style=None):
    """Straight-alpha square, optional analytic mask ('circle' | 'roundrect12')."""
    body = bytearray(resample(master, MASTER, size))
    if style is None:
        return bytes(body)
    if style == "circle":
        r = size / 2
    elif style == "roundrect12":
        r = size / 2
    else:
        raise ValueError(style)
    for y in range(size):
        py = y + 0.5 - size / 2
        for x in range(size):
            px = x + 0.5 - size / 2
            sd = math.hypot(px, py) - r if style == "circle" else sil_sd(px, py, r, 0.12 * size)
            i = 4 * (y * size + x)
            body[i + 3] = round(cov(sd) * body[i + 3])
    return bytes(body)


def foreground(size, master):
    """Android adaptive foreground: transparent canvas, mark in ~62% safe zone."""
    inner = max(2, round(size * 0.62))
    src = resample(master, MASTER, inner)
    out = bytearray(size * size * 4)
    off = (size - inner) // 2
    for y in range(inner):
        base = 4 * y * inner
        obase = 4 * ((y + off) * size + off)
        for x in range(inner):
            i = base + 4 * x
            if src[i + 3]:
                j = obase + 4 * x
                out[j : j + 4] = src[i : i + 4]
    return bytes(out)


def unpremul(rgba):
    out = bytearray(rgba)
    for i in range(0, len(out), 4):
        a = out[i + 3]
        if 0 < a < 255:
            f = 255.0 / a
            out[i] = min(255, round(out[i] * f))
            out[i + 1] = min(255, round(out[i + 1] * f))
            out[i + 2] = min(255, round(out[i + 2] * f))
    return bytes(out)


def bigsur(size, master):
    """Squircle content at 0.8046 over a subtle analytic shadow; premultiplied."""
    content = max(2, round(size * SQUIRCLE_CONTENT))
    body = resample(master, MASTER, content)
    off = (size - content) / 2
    half = content / 2
    r = SQUIRCLE_R * content
    spread = SH_SPREAD * size + 1.0
    lift = SH_LIFT * size + 0.5
    buf = bytearray(size * size * 4)
    for y in range(size):
        py = y + 0.5 - off - half
        base = y * size * 4
        for x in range(size):
            px = x + 0.5 - off - half
            i = base + 4 * x
            edge = sil_sd(px, py, half, r)
            s = SH_ALPHA * (1.0 - smooth01((edge - lift) / spread))
            m = cov(edge)
            a = m + s * (1 - m)
            if a <= 0:
                continue
            # body content: nearest body pixel (body is opaque, pre-AA'd)
            bx = 0 if content == 1 else min(content - 1, max(0, round(px + half - 0.5)))
            by = 0 if content == 1 else min(content - 1, max(0, round(py + half - 0.5)))
            j = 4 * (by * content + bx)
            buf[i] = round(body[j] * m)
            buf[i + 1] = round(body[j + 1] * m)
            buf[i + 2] = round(body[j + 2] * m)
            buf[i + 3] = round(255 * a)
    return bytes(buf)


def smooth01(t):
    if t <= 0:
        return 0.0
    if t >= 1:
        return 1.0
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- encoders

def _chunk(tag, payload):
    return (
        struct.pack(">I", len(payload))
        + tag
        + payload
        + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
    )


def png_bytes(w, h, rgba):
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(rgba[y * 4 * w : (y + 1) * 4 * w])
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        + _chunk(b"IEND", b"")
    )


def write_png(path, w, h, rgba):
    with open(path, "wb") as f:
        f.write(png_bytes(w, h, rgba))


ICNS_CODES = {16: "icp4", 32: "icp5", 64: "icp6", 128: "ic07", 256: "ic08", 512: "ic09", 1024: "ic10"}


def icns_bytes(members):
    body = b""
    for code, data in members:
        body += code.encode() + struct.pack(">I", len(data) + 8) + data
    return b"icns" + struct.pack(">I", len(body) + 8) + body


def ico_bytes(entries):
    """PNG-compressed ICO; entries: [(w, h, png_bytes)]."""
    out = struct.pack("<HHH", 0, 1, len(entries))
    offset = 6 + 16 * len(entries)
    table = payload = b""
    for w, h, data in entries:
        table += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(data), offset)
        payload += data
        offset += len(data)
    return out + table + payload


# ---------------------------------------------------------------- asset map

def build_channel_files(master):
    outputs = {}

    for name, size in (
        ("icon.png", 512),
        ("128x128.png", 128),
        ("128x128@2x.png", 256),
        ("64x64.png", 64),
        ("32x32.png", 32),
    ):
        outputs[name] = png_bytes(size, size, square(size, master))

    outputs["dock.png"] = png_bytes(256, 256, unpremul(bigsur(256, master)))

    members = [
        (
            ICNS_CODES[size],
            png_bytes(size, size, bigsur(size, master)),
        )
        for size in (16, 32, 64, 128, 256, 512, 1024)
    ]
    outputs["icon.icns"] = icns_bytes(members)

    outputs["icon.ico"] = ico_bytes(
        [(s, s, png_bytes(s, s, square(s, master))) for s in (16, 24, 32, 48, 64, 256)]
    )

    for name, size in (
        ("Square30x30Logo.png", 30),
        ("Square44x44Logo.png", 44),
        ("Square71x71Logo.png", 71),
        ("Square89x89Logo.png", 89),
        ("Square107x107Logo.png", 107),
        ("Square142x142Logo.png", 142),
        ("Square150x150Logo.png", 150),
        ("Square284x284Logo.png", 284),
        ("Square310x310Logo.png", 310),
        ("StoreLogo.png", 50),
    ):
        outputs[name] = png_bytes(size, size, square(size, master))

    android = (
        ("android/mipmap-mdpi/ic_launcher.png", 48, "roundrect12"),
        ("android/mipmap-hdpi/ic_launcher.png", 49, "roundrect12"),
        ("android/mipmap-xhdpi/ic_launcher.png", 96, "roundrect12"),
        ("android/mipmap-xxhdpi/ic_launcher.png", 144, "roundrect12"),
        ("android/mipmap-xxxhdpi/ic_launcher.png", 192, "roundrect12"),
        ("android/mipmap-mdpi/ic_launcher_round.png", 48, "circle"),
        ("android/mipmap-hdpi/ic_launcher_round.png", 49, "circle"),
        ("android/mipmap-xhdpi/ic_launcher_round.png", 96, "circle"),
        ("android/mipmap-xxhdpi/ic_launcher_round.png", 144, "circle"),
        ("android/mipmap-xxxhdpi/ic_launcher_round.png", 192, "circle"),
        ("android/mipmap-mdpi/ic_launcher_foreground.png", 108, False),
        ("android/mipmap-hdpi/ic_launcher_foreground.png", 162, False),
        ("android/mipmap-xhdpi/ic_launcher_foreground.png", 216, False),
        ("android/mipmap-xxhdpi/ic_launcher_foreground.png", 324, False),
        ("android/mipmap-xxxhdpi/ic_launcher_foreground.png", 432, False),
    )
    for name, size, style in android:
        img = foreground(size, master) if style is False else square(size, master, style)
        outputs[name] = png_bytes(size, size, img)

    ios = {
        "ios/AppIcon-20x20@1x.png": 20,
        "ios/AppIcon-20x20@2x.png": 40,
        "ios/AppIcon-20x20@2x-1.png": 40,
        "ios/AppIcon-20x20@3x.png": 60,
        "ios/AppIcon-29x29@1x.png": 29,
        "ios/AppIcon-29x29@2x.png": 58,
        "ios/AppIcon-29x29@2x-1.png": 58,
        "ios/AppIcon-29x29@3x.png": 87,
        "ios/AppIcon-40x40@1x.png": 40,
        "ios/AppIcon-40x40@2x.png": 80,
        "ios/AppIcon-40x40@2x-1.png": 80,
        "ios/AppIcon-40x40@3x.png": 120,
        "ios/AppIcon-512@2x.png": 1024,
        "ios/AppIcon-60x60@2x.png": 120,
        "ios/AppIcon-60x60@3x.png": 180,
        "ios/AppIcon-76x76@1x.png": 76,
        "ios/AppIcon-76x76@2x.png": 152,
        "ios/AppIcon-83.5x83.5@2x.png": 167,
    }
    for name, size in ios.items():
        outputs[name] = png_bytes(size, size, square(size, master))

    outputs["android/mipmap-anydpi-v26/ic_launcher.xml"] = open(
        os.path.join(HERE, "beta/android/mipmap-anydpi-v26/ic_launcher.xml"), "rb"
    ).read()
    outputs["android/values/ic_launcher_background.xml"] = open(
        os.path.join(HERE, "beta/android/values/ic_launcher_background.xml"), "rb"
    ).read().replace(b"fff", b"0E3A53")
    outputs["app-icon.png"] = png_bytes(MASTER, MASTER, master)
    return outputs


SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">\n'
    '  <rect width="1024" height="1024" rx="{rx}" fill="#0e3a53"/>\n'
    '  <rect x="{frame_x}" y="{frame_x}" width="{frame_w}" height="{frame_w}" rx="{frame_r}"'
    ' fill="none" stroke="#c8873c" stroke-width="{frame_t}"/>\n'
    '  <circle cx="708" cy="708" r="90" fill="#f6ece0"/>\n'
    "</svg>\n"
)


def build_favicons(master):
    inner = FRAME_EXT - FRAME_T / 2
    favs = {
        "favicon-96x96-v3.png": png_bytes(96, 96, square(96, master)),
        "favicon-96x96.png": png_bytes(96, 96, square(96, master)),
        "apple-touch-icon-v3.png": png_bytes(180, 180, square(180, master)),
        "apple-touch-icon.png": png_bytes(180, 180, square(180, master)),
        "favicon-v3.svg": SVG.format(
            rx=round(MASTER * SQUIRCLE_R),
            frame_x=round(512 - inner),
            frame_w=round(2 * inner),
            frame_r=round(FRAME_R - FRAME_T / 2),
            frame_t=round(FRAME_T),
        ).encode(),
    }
    favs["favicon.svg"] = favs["favicon-v3.svg"]
    data = ico_bytes([(s, s, png_bytes(s, s, square(s, master))) for s in (16, 24, 32, 48, 64, 96, 256)])
    favs["favicon-v3.ico"] = data
    favs["favicon.ico"] = data
    return favs


CHANNELS = ("dev", "beta", "prod")


def main():
    print("rasterizing master…", flush=True)
    master = letter_draw(MASTER)
    outputs = build_channel_files(master)
    favs = build_favicons(master)
    outputs.pop("app-icon.png")
    write_png(os.path.join(HERE, "app-icon.png"), MASTER, MASTER, master)
    for channel in CHANNELS:
        for rel, value in outputs.items():
            path = os.path.join(HERE, channel, rel)
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "wb") as f:
                f.write(value)
    print(f"wrote {len(outputs)} files x {len(CHANNELS)} channels", flush=True)
    for rel, value in favs.items():
        with open(os.path.join(APP_PUBLIC, rel), "wb") as f:
            f.write(value)
    print(f"wrote {len(favs)} favicons to {APP_PUBLIC}", flush=True)


if __name__ == "__main__":
    main()
