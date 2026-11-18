# 17 November 2026 — world news in one image

![make.fun bounty](https://img.shields.io/badge/make.fun-bounty%20entry-111827)
![image](https://img.shields.io/badge/image-1024%C3%971024%20PNG-15803d)

Entry for **make.fun / Sum up 17 November's world news in one image**:
<https://make.fun/c/news-image-20261117>.

The poster names the day (**TUESDAY, 17 NOVEMBER 2026**) and gives ten
story cards in two columns, plus a ticker of further events. It is a single
1024×1024 PNG under 1 MiB.

## What the image covers

1. **Ukraine · War** — the Kerch Bridge was hit for a second day; two people died and a road span collapsed.
2. **Middle East · War** — US strikes on Qeshm Island; Bahrain intercepted IRGC drones aimed at Sheikh Isa Air Base.
3. **Gaza & West Bank · Humanitarian** — Israeli strikes killed five Palestinians, including a child; settlers killed a 72-year-old woman near Jericho.
4. **Europe · Disasters** — a Russian An-12 crashed near Kemerovo, killing 19; two trains collided in Prague, injuring 46.
5. **Americas · Health** — PAHO revoked the measles elimination status of the US, Mexico and Bolivia; US cases passed 5,700.
6. **Bangladesh · Economy** — garment workers protested for a minimum wage rise; 37 factories closed.
7. **Asia-Pacific · Economy** — Canada and China agreed further tariff cuts before APEC in Shenzhen.
8. **Politics · North America & Asia** — Mary Peltola won Alaska's Senate seat; Mongolia's president resigned over embezzlement allegations.
9. **Europe-Asia · Diplomacy** — France and Malaysia signed a strategic partnership covering defence, energy and technology.
10. **Africa & Caribbean · Justice** — Guinea jailed 200+ illegal gold miners; Haitians marched for Salvadoran anti-gang troops.

The footer ticker adds the Apple service outage, the storming of a Bangladesh
police station, and North Macedonia's arrests in an alleged Iran-linked plot
in Greece.

## Files

- `entry.png` — the submitted image (1024×1024, PNG, < 1 MiB).
- `main.py` — Python 3.13 entrypoint; copies `entry.png` to `/output/entry.png`.
- `render.py` — Pillow renderer used to draw the poster; not run by the grader.
- `LICENSE` — MIT.
- `.makefun/owner.json` — wallet claim file for the make.fun entry.

## Run locally

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The grader runs `main.py` twice; both runs copy the same PNG bytes.
