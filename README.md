# UYB AI

**Zero Token Architecture™** — Thinks deeply. Helps never.

A CLI that mimics the look and feel of AI coding assistants — thinking animations,
usage panels, effort levels — and then tells you to figure it out yourself.

```
╭─ UYB AI  v0.1.0 ───────────────────────────────────────────────────╮
│  ~/your/project                                                     │
│  uyb-cortex-1.0  ·  effort: maximum  ·  Autonomous Reasoning Platform™ │
╰─────────────────────────────────────────────────────────────────────╯
```

## Install

```bash
pipx install uybai
```

Or with pip:

```bash
pip install uybai
```

## Usage

```bash
uyb                    # 60-second deliberation mode
uyb --fast             # 10-second mode
uyb --think-time 30    # custom duration
```

### Commands

| Command   | Description |
|-----------|-------------|
| `/fast`   | Switch to 10-second think mode |
| `/slow`   | Switch to 60-second think mode |
| `/usage`  | Show token usage and cost (all zero) |
| `/effort` | Show effort level and thinking budget |
| `/clear`  | Clear the screen |
| `/help`   | Show all commands |
| `/exit`   | Exit |

Type `/` to see command suggestions with autocomplete.

## License

MIT
