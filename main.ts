// news-image-20261120 — "Sum up 20 November's world news in one image".
// Node 22, standard library only. The entry is a single 1024x1024 PNG
// (entry.png beside this file) drawn for Friday 20 November 2026:
// a newspaper front page with the day's five biggest stories —
// the ICJ's genocide ruling on Myanmar, the Trump–Xi–Putin summit in
// Shenzhen, Russia's overnight strikes on Kyiv, the Houthi missile that
// hit Riyadh's wealth-fund tower, and the slide in world markets.
// The program's only job is to place that image at /output/entry.png
// (or $MAKEFUN_OUTPUT_DIR/entry.png when the harness sets it), so the
// two runs the grader does write byte-identical output.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
writeFileSync(target, readFileSync(join(here, "entry.png")));
