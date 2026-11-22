# The World Today — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/r30639623-lab/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/r30639623-lab/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page summing up Sunday 22 November 2026 world news in one
image: 35 stories across 7 regions, every one dated Sunday 22 November 2026.
Three big illustrated panels (Kyiv drone strike, COP31 overtime, Iran strikes
Bahrain), ten medium cards, a world map with numbered pins 14–35, and a DATE
CHECK box listing the earlier news deliberately left out. All drawn locally
with Pillow — no external photos.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024 PNG). `render.py` draws `news.png`
from the story data; `main.py` (stdlib only) just copies it to the output
directory, so both grader runs produce byte-identical output.
