# Submission Info

<!-- Fill this in as your project takes shape, and keep it current.
     This becomes your public profile card on the workshop showcase page,
     pulled live from this file — worth a real sentence per field, not a
     placeholder. -->

- **Student Name:** Chrissy Wang

- **Fork URL:** `https://github.com/XiaohuaWang-Chrissy/2026-ai-news-innovation-workshop`

- **Hypothesis or problem statement:** Local business stories break first in primary sources — SEC filings, layoff notices, building permits, business licenses, property records — but those are scattered across dozens of government sites, most with no search, no alerts, and no RSS. A reporter can't realistically check them all every day, so they end up following other outlets instead of finding stories first. My hypothesis: a monitor that reads those primary sources directly, every day, will surface original leads that never show up in a press release or a competitor's feed.

- **What you're building:** AutoNews, a local business-news monitor. It watches a city's primary sources on a schedule, uses an LLM to summarize each item into a short reporter's pitch with the money or policy angle pulled out, and emails a single digest sorted by beat and neighborhood. The engine is city-agnostic — every place-specific detail lives in a config file, so covering a new city means writing a new config, not new code.

- **Solution:** It runs today for two cities. Houston/Texas watches 46 feeds plus custom readers for SEC EDGAR filings, Texas WARN layoff notices, TDLR contractor licenses, and HCAD commercial property records. New York City/NY State watches 66 feeds plus NY and NJ WARN notices, EDGAR, DOB building permits, DCWP business licenses, and ACRIS property deeds. It checks every 10 minutes via launchd and delivers one HTML digest per city. Honest limits: it runs on my own Mac rather than in the cloud, so it stops when my laptop does; summary quality depends on the model I point it at; and adding a third city still means hand-assembling that city's source list, which is the slow part.
