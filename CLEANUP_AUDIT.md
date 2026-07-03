# Saigon Companion v4 Base Clean Pack — Cleanup Audit

Source: `saigon-companion-v3.9.7-trip-final-freeze.zip`
Output: `saigon-companion-v4-base-clean-pack.zip`

## Summary

- Original files: 58
- Clean pack files: 57
- Deleted files: 1
- UI/functionality changes: none
- CSS cleanup: replaced missing legacy `logo-latest.jpeg` references with existing `logo-watermark-monogram.png` to preserve intended watermark behaviour.
- Structural path changes: none, to avoid breaking existing root-relative static deployment.

## KEEP

All files below are retained because they are referenced by HTML, CSS, JS, manifest, service worker, or are part of the reachable static site/PWA shell.

- `bakes.html`
- `bep-me-in.html`
- `book-street.html`
- `cafe-apartments.html`
- `com-tam-moc.html`
- `cong.html`
- `cooking.html`
- `dauple.html`
- `day1.html`
- `day2.html`
- `day3.html`
- `day4.html`
- `day5.html`
- `expenses.html`
- `fine-arts.html`
- `fusion.html`
- `garmentory.html`
- `guide.html`
- `ha-spa.html`
- `icon-192.png`
- `icon-512.png`
- `index.html`
- `itinerary.html`
- `libe.html`
- `little-bear.html`
- `logo-monogram-transparent.png`
- `logo-watermark-monogram.png`
- `lune.html`
- `manifest.json`
- `marou.html`
- `memory.html`
- `moc-huong.html`
- `moc-kim.html`
- `moments.html`
- `new-playground.html`
- `nha-suga.html`
- `nosbyn.html`
- `notre-dame.html`
- `offline.html`
- `ohquao.html`
- `omakase-tiger.html`
- `pho-sol.html`
- `pho-vietnam.html`
- `pink-church.html`
- `pizza4ps.html`
- `post-office.html`
- `push-push.html`
- `quan-thuy.html`
- `quince.html`
- `running-bean.html`
- `saigon-concept.html`
- `script.js`
- `styles.css`
- `sw.js`
- `temple-leaf.html`
- `trip.html`
- `war-museum.html`

## DELETE

| File | Reason |
|---|---|
| `logo-extracted.png` | Confirmed not referenced by any HTML, CSS, JS, `manifest.json`, or `sw.js`. Duplicate/legacy logo asset. |

## MERGE

No merge performed. The current project is a flat static site. Merging guide/detail HTML pages or shared markup would be a Version 4 refactor, not cleanup.

## RENAME

No rename performed. Renaming root files or asset names would require changing references and increases deployment risk.

## Folder Structure Review

Current flat structure is deploy-safe for GitHub + Vercel static hosting. Recommended for later Version 4 refactor only:

```text
/assets/images/
/assets/icons/
/css/styles.css
/js/script.js
```

Not applied in this clean pack because it would require changing many paths and could create avoidable regressions.

## PWA Audit

- `manifest.json`: kept. Uses `index.html` as `start_url`, includes `icon-192.png` and `icon-512.png`.
- `sw.js`: kept and cleaned.
- `styles.css`: kept. Missing legacy `logo-latest.jpeg` references replaced with existing watermark asset.
- Cache name updated from `saigon-companion-v3.9.7` to `saigon-companion-v4-base-clean`.
- Duplicate `offline.html` entry removed from precache list.
- `logo-monogram-transparent.png` and `logo-watermark-monogram.png` added to precache because `styles.css` references them.
- `offline.html`: kept.
- Icons: kept.

## Project Tree

```text
bakes.html
bep-me-in.html
book-street.html
cafe-apartments.html
com-tam-moc.html
cong.html
cooking.html
dauple.html
day1.html
day2.html
day3.html
day4.html
day5.html
expenses.html
fine-arts.html
fusion.html
garmentory.html
guide.html
ha-spa.html
icon-192.png
icon-512.png
index.html
itinerary.html
libe.html
little-bear.html
logo-monogram-transparent.png
logo-watermark-monogram.png
lune.html
manifest.json
marou.html
memory.html
moc-huong.html
moc-kim.html
moments.html
new-playground.html
nha-suga.html
nosbyn.html
notre-dame.html
offline.html
ohquao.html
omakase-tiger.html
pho-sol.html
pho-vietnam.html
pink-church.html
pizza4ps.html
post-office.html
push-push.html
quan-thuy.html
quince.html
running-bean.html
saigon-concept.html
script.js
styles.css
sw.js
temple-leaf.html
trip.html
war-museum.html
```
