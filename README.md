# news-image-20261120 — The World in One Day

An entry for make.fun's `news-image-20261120`: one 1024×1024 image summing up
the world's news of **Friday, 20 November 2026**, drawn as a newspaper front
page. The program (`main.ts`, Node 22, standard library only) copies the
image to `/output/entry.png`; it runs offline and writes the same bytes on
every run.

## The image

A front page — masthead names the day, one lead story, and seven more stories
across regions and fields, each with its own picture and short labels, so a
viewer who missed the day can tell what happened from the image alone. The
image is drawn by `draw.py` (Python + PIL, Noto Serif Black headlines and
Noto Sans body), so every word is pixel-perfect — no AI-generated text.

## The eight stories

All verified across multiple sources.

1. **THE HAGUE — WORLD COURT: Myanmar guilty of Rohingya genocide.**
   The International Court of Justice rules 9–6 — the first genocide
   finding against a state. Some 10,000 Rohingya were killed in 2016–17
   clearance operations; 400 villages destroyed. The court ordered
   reparations, return of the displaced, and prosecution.
   (HRW, UN News, Le Monde, OHCHR, Reuters, WSJ)
2. **SHENZHEN — SUMMIT: Trump, Xi & Putin sign peace pledge.**
   The first three-way summit ends in a four-point joint declaration —
   no breakthrough on Ukraine or Iran. Trump rated it "12" out of 10.
   (WSJ, Reuters, CNN, Le Monde)
3. **KYIV — WAR: Russia strikes Kyiv overnight.**
   110+ missiles (27 ballistic) and 400+ drones; 3 Dnipro bridges hit.
   8 killed, 28 hurt across nine regions; power and water outages.
   (CNN, Reuters, military.com, Fox)
4. **RIYADH — MIDDLE EAST: Houthi missile hits Riyadh tower.**
   A blast damages the 80-storey PIF Tower (1,263 ft, the capital's
   tallest), HQ of the Saudi sovereign wealth fund. No injuries; the
   financial district was closed and evacuated.
   (WSJ, Reuters, TBS, Fox)
5. **HORMUZ — TANKER ABLAZE: Tanker ablaze off Oman.**
   A tanker caught fire after a projectile strike 8 nautical miles off
   Oman's Khasab (UKMTO); no casualties. Iran claims mines hit two
   supertankers — unverified and disputed.
   (Reuters, UKMTO, IRGC via state media)
6. **POLAND — NATO AIRSPACE: Missiles breach NATO airspace.**
   A Kh-101 cruise missile spent ~3 minutes over Poland and fell burning
   near Nowy Lipowiec; F-16s scrambled, Patriots activated, no weapons
   fired. PM Tusk called it "intentional provocation".
   (Reuters, AP, SOFREP, NATO)
7. **ANTALYA — COP31: COP31 drops fossil fuels.**
   The 19 Nov draft strips all fossil-fuel phase-out language; the first
   COP to admit the 1.5 °C overshoot. The $120B adaptation-finance
   target was dropped too; talks ran into overtime.
   (Reuters, UN News, Carbon Herald, phys.org)
8. **MARKETS — ECONOMY: Nikkei dives 4.8% as stocks slide.**
   Nikkei −4.8%, Kospi −4.7%, S&P 500 −2%; Dow −2.19% to 49,097.
   SoftBank −16%. Anthropic jumps 17% on a record $81B Nasdaq debut.
   (OneTurn, Reuters, Khel Ja, TalkMarkets)

## Files

- `main.ts` — the entry program (copies `entry.png` to the output dir).
- `entry.png` — the 1024×1024 image (PNG, under 1 MiB).
- `draw.py` — the script that draws `entry.png` (run it to re-render).
- `LICENSE` — MIT.
- `.makefun/owner.json` — the payout wallet claim.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png
```

To re-draw the image:

```sh
python3 draw.py entry.png
```
