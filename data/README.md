# data/

Everything in this folder except this README is gitignored. It holds about 1.4M
scraped usernames and per-player API responses, which are too large to commit
and shouldn't be redistributed.

```
data/
├── raw/          # exactly as collected, never modified
│   ├── usernames/
│   │   ├── r6_tracker_leaderboards.csv   # R6 Tracker PC ranked leaderboard exports
│   │   └── siegrs_players.csv            # python -m sixsense.data_collection.siegrs
│   └── arenyze/                          # one cached API response per player
├── interim/      # cleaned and merged (e.g. the deduplicated username pool)
└── processed/    # model-ready feature tables
```

## Sources

| File | Columns | How it was collected |
|---|---|---|
| `r6_tracker_leaderboards.csv` | `handle, platform, country, rankPoints, position, matchesPlayed, kd` | Exported from the R6 Tracker ranked leaderboard pages with a browser-console script, then combined into a single file. `rankPoints` is a snapshot from when it was scraped. Use it only to stratify sampling, never as a label. |
| `siegrs_players.csv` | `username, rank, platform` | `python -m sixsense.data_collection.siegrs` |
