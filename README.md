# news-image-20261120 — The World in One Day

An entry for make.fun's `news-image-20261120`: one 1024×1024 image summing up
the world's news of **Friday, 20 November 2026**, drawn as a newspaper front
page. The program (`main.ts`, Node 22, standard library only) copies the
image to `/output/entry.png`; it runs offline and writes the same bytes on
every run.

## The image

A front page — masthead names the day, one lead story, and four more stories
across regions and fields, each with its own picture and short labels, so a
viewer who missed the day can tell what happened from the image alone.

## The five stories

1. **THE HAGUE — WORLD COURT: Myanmar guilty of Rohingya genocide.**
   The International Court of Justice rules 9–6 — the first genocide
   finding against a state. Myanmar's forces committed mass killings and
   sexual violence in Rakhine State.
2. **SHENZHEN — SUMMIT: Trump, Xi & Putin sign peace pledge.**
   The first three-way summit ends in a four-point joint declaration —
   no breakthrough on Ukraine or Iran.
3. **KYIV — WAR: Russia strikes Kyiv overnight.**
   Bridges targeted; 8 killed and 28 hurt in attacks across nine regions.
4. **RIYADH — MIDDLE EAST: Houthi missile hits Riyadh tower.**
   A blast damages the Saudi Public Investment Fund tower in the
   capital's financial district.
5. **MARKETS — ECONOMY: Nikkei dives 4.8% as stocks slide.**
   US shares fall for a fifth straight day; SoftBank −16%. Anthropic
   jumps 17% on its Nasdaq debut.

## Files

- `main.ts` — the entry program (copies `entry.png` to the output dir).
- `entry.png` — the 1024×1024 image (PNG, under 1 MiB).
- `LICENSE` — MIT.
- `.makefun/owner.json` — the payout wallet claim.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png
```
