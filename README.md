```
`7MM"""Yp, `7MM"""Mq.   .g8""8q. `7MMF' `YMM' `7MMF'`7MM"""YMM 
  MM    Yb   MM   `MM..dP'    `YM. MM   .M'     MM    MM    `7 
  MM    dP   MM   ,M9 dM'      `MM MM .d"       MM    MM   d   
  MM"""bg.   MMmmdM9  MM        MM MMMMM.       MM    MMmmMM   
  MM    `Y   MM  YM.  MM.      ,MP MM  VMA      MM    MM   Y  ,
  MM    ,9   MM   `Mb.`Mb.    ,dP' MM   `MM.    MM    MM     ,M
.JMMmmmd9  .JMML. .JMM. `"bmmd"' .JMML.   MMb..JMML..JMMmmmmMMM
```

A terminal coding agent designed to minimize token costs by any means necessary.

![Status](https://img.shields.io/badge/status-in%20development-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-red?style=for-the-badge)
![Language](https://img.shields.io/badge/language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
---

## Installation

### macOS / Linux:

brokie is managed by [uv](https://docs.astral.sh/uv/). Install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

then install brokie with:
```bash
uv tool install git+https://github.com/theranser/brokie
```

### Windows:

COMING SOON

## Configuration

| OS | Path |
|---|---|
| macOS / Linux | `~/.config/brokie/config.json` |
| Windows | `%APPDATA%\brokie\config.json` |

More info on configuration coming soon.

## Roadmap (subject to change)

```diff
General features:
+ Basic agent functionality
- Response streaming
- Anthropic API support
- AGENTS.md support
- Token/cost tracking

Cost-saving features:
- Subagent support
- Automatic context compaction
- Headroom integration (https://github.com/headroomlabs-ai/headroom)
- context-mode integration (https://github.com/mksglu/context-mode)
- Graphify integration (https://github.com/Graphify-Labs/graphify)
```

## Development

Linting is [ruff](https://docs.astral.sh/ruff/) with `select = ["ALL"]`, type checking is [basedpyright](https://docs.basedpyright.com/) in `standard` mode.

To run the linting and formatting:
```bash
uvx ruff format --check .
uvx basedpyright
```