---
name: baidu-search
description: Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# Baidu Search

Search the web via Baidu AI Search API.

## Usage

```bash
python3 skills/baidu-search/scripts/search.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | Search query |
| count | int | no | 10 | Number of results to return, range 1-50 |
| freshness | str | no | Null | Time range: pd(24h), pw(7d), pm(31d), py(365d) or YYYY-MM-DDtoYYYY-MM-DD |

## Examples

```bash
# Basic search
python3 scripts/search.py '{"query":"人工智能"}'

# Recent news (past 24h)
python3 scripts/search.py '{"query":"最新新闻","freshness":"pd"}'

# Set count to 20
python3 scripts/search.py '{"query":"旅游景点","count":20}'
```

## Configuration

Set environment variable:
```bash
export BAIDU_API_KEY="your_baidu_qianfan_api_key"
```

## Current Status

Fully functional.
