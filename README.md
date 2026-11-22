# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Mittominato/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Mittominato/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

The World in One Image — 22 November 2026. A deterministic program that
draws one newspaper-style front page (1600×2000) summing up the six
world-news stories that defined Sunday 22 November 2026, each with its
own hand-drawn scene, headline, deck and source line — so an AI judge
with no news feed can still read the day at a glance.

## The six stories (all verified from public reporting)

1. **The Gulf war widens** — Iran hits a U.S. air base in Kuwait and
   sites in Bahrain (Associated Press, 18 Nov 2026).
2. **Ukraine · Poland** — Russia's biggest barrage yet: 400+ drones and
   110+ missiles hit Ukraine; missiles land in Poland (AP, 20 Nov 2026).
3. **APEC · Shenzhen** — Trump, Xi and Putin hold a first-ever
   three-way summit (USA Today / Le Monde, 19 Nov 2026).
4. **Earthquake** — A magnitude 6.9 quake shakes Peru's Andes, felt in
   Lima; no damage or casualties reported (AP / U.S. Geological Survey,
   20–21 Nov 2026).
5. **Climate · COP31** — Talks in Antalya miss their deadline and run
   into overtime, split over fossil fuels (AP / Reuters, 20–21 Nov 2026).
6. **The Baltic** — Drones set the Russian cargo ship Sparta II ablaze
   in the Gulf of Finland; all 16 crew are evacuated (Reuters / CNN,
   21 Nov 2026).

## Run it

```sh
python3 main.py
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`). Pure
Pillow, no network, no clock, no randomness — two runs produce a
byte-identical PNG (verified: identical sha256 across runs).

## Layout

Masthead, a full-width hero panel (the Gulf), two rows of two panels
(Ukraine/Poland, APEC, Peru quake, COP31), a wide bottom panel (the
Baltic ship), and a footer naming every source. Every scene is drawn
from Pillow primitives; fonts fall back to Pillow's built-in font when
no system font is present.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6xedf17w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
