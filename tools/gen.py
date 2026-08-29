#!/usr/bin/env python3
"""Generate the zsh-style terminal SVGs for the profile README."""

CH = 12          # monospace advance width at font-size 20
X0 = 40          # left padding
XCMD = X0 + 5 * CH   # commands start at column 5:  "➜  ~ "
XDIR = X0 + 3 * CH   # the cyan ~ sits at column 3

DARK = dict(
    bg="#0d1117", border="#30363d", title="#8b949e",
    green="#3fb950", cyan="#39c5cf", text="#c9d1d9",
    name="#e6edf3", muted="#8b949e", blue="#58a6ff",
)
LIGHT = dict(
    bg="#ffffff", border="#d1d9e0", title="#59636e",
    green="#1a7f37", cyan="#1b7c83", text="#1f2328",
    name="#1f2328", muted="#59636e", blue="#0969da",
)

TYPED = "sudo systemctl restart curiosity"


def keyframes():
    """Discrete widths: type out, hold, erase, pause."""
    n = len(TYPED)
    vals = [i * CH for i in range(n + 1)]      # type
    vals += [n * CH] * 18                       # hold
    vals += list(range(n * CH, -1, -2 * CH))    # erase (2 chars/step)
    vals += [0] * 8                             # pause
    return vals


def prompt(y, cmd, c):
    """A robbyrussell prompt line. Absolute x per tspan so a fallback
    glyph for ➜ can't shift the command."""
    return (
        f'    <text y="{y}">'
        f'<tspan x="{X0}" fill="{c["green"]}" font-weight="700">➜</tspan>'
        f'<tspan x="{XDIR}" fill="{c["cyan"]}">~</tspan>'
        f'<tspan x="{XCMD}" fill="{c["text"]}">{cmd}</tspan></text>'
    )


def cols(y, items, pitch, c):
    """ls-style aligned columns."""
    spans = "".join(
        f'<tspan x="{X0 + i * pitch}">{w}</tspan>' for i, w in enumerate(items)
    )
    return f'    <text y="{y}" fill="{c["blue"]}">{spans}</text>'


def build(c):
    w, h = 1150, 908
    vals = keyframes()
    width_vals = ";".join(str(v) for v in vals)
    cursor_vals = ";".join(str(XCMD + v) for v in vals)
    dur = f"{len(vals) * 0.11:.2f}s"

    L = []
    L.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="A zsh terminal session. '
        'whoami: Nima Naghibi, backend and infrastructure engineer at Hatchup. '
        'cat about.txt: I build the layer underneath - APIs, the servers behind them, '
        'and the automation that puts them there. When I want to understand something, '
        'I write it from scratch. ls langs/: bash, c, go, java, python, typescript. '
        'ls stack/: ansible, docker, docker-swarm, grafana, kafka, linux, portainer, '
        'postgresql, prometheus, redis. cat .focus: distributed systems, networking, '
        'operating systems, system design, security. systemctl status curiosity: '
        'curiosity.service, active (running). uptime: Iran, always curious.">'
    )
    L.append(f'  <defs><clipPath id="typing"><rect x="{XCMD}" y="838" width="0" height="28">')
    L.append(f'    <animate attributeName="width" calcMode="discrete" values="{width_vals}" dur="{dur}" repeatCount="indefinite"/>')
    L.append('  </rect></clipPath></defs>')
    L.append("")
    L.append(f'  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    L.append(f'  <path d="M0 48 H{w}" stroke="{c["border"]}"/>')
    L.append("")
    L.append('  <circle cx="32" cy="24" r="7.5" fill="#ff5f57"/>')
    L.append('  <circle cx="58" cy="24" r="7.5" fill="#febc2e"/>')
    L.append('  <circle cx="84" cy="24" r="7.5" fill="#28c840"/>')
    L.append("")
    L.append('  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="20">')
    L.append(f'    <text x="{w//2}" y="30" font-size="15" fill="{c["title"]}" text-anchor="middle">nima@github: ~ — zsh</text>')
    L.append("")

    L.append(prompt(100, "whoami", c))
    L.append(f'    <text x="{X0}" y="138" font-size="24" font-weight="600" fill="{c["name"]}">Nima Naghibi</text>')
    L.append(f'    <text x="{X0}" y="171" font-size="18" fill="{c["muted"]}">Backend &amp; infrastructure engineer @ Hatchup</text>')
    L.append("")

    L.append(prompt(222, "cat about.txt", c))
    L.append(f'    <text x="{X0}" y="255" fill="{c["muted"]}">I build the layer underneath — APIs, the servers behind them, and the automation</text>')
    L.append(f'    <text x="{X0}" y="288" fill="{c["muted"]}">that puts them there. When I want to understand something, I write it from scratch.</text>')
    L.append("")

    L.append(prompt(339, "ls langs/", c))
    L.append(cols(372, ["bash/", "c/", "go/", "java/", "python/", "typescript/"], 156, c))
    L.append("")

    L.append(prompt(423, "ls stack/", c))
    L.append(cols(456, ["ansible/", "docker/", "docker-swarm/", "grafana/", "kafka/"], 180, c))
    L.append(cols(489, ["linux/", "portainer/", "postgresql/", "prometheus/", "redis/"], 180, c))
    L.append("")

    L.append(prompt(540, "cat .focus", c))
    L.append(f'    <text x="{X0}" y="573" fill="{c["muted"]}">distributed systems · networking · operating systems · system design · security</text>')
    L.append("")

    L.append(prompt(624, "systemctl status curiosity", c))
    L.append(
        f'    <text y="657">'
        f'<tspan x="{X0}" fill="{c["green"]}">●</tspan>'
        f'<tspan x="{X0 + 2*CH}" fill="{c["text"]}">curiosity.service</tspan>'
        f'<tspan x="{X0 + 20*CH}" fill="{c["muted"]}">- always reading one layer below</tspan></text>'
    )
    L.append(f'    <text x="{XCMD}" y="690" fill="{c["muted"]}">Loaded: loaded (/etc/nima/curiosity.service; enabled)</text>')
    L.append(
        f'    <text y="723">'
        f'<tspan x="{XCMD}" fill="{c["muted"]}">Active:</tspan>'
        f'<tspan x="{XCMD + 8*CH}" fill="{c["green"]}" font-weight="600">active (running)</tspan>'
        f'<tspan x="{XCMD + 25*CH}" fill="{c["muted"]}">since boot</tspan></text>'
    )
    L.append("")

    L.append(prompt(774, "uptime", c))
    L.append(f'    <text x="{X0}" y="807" fill="{c["muted"]}">Iran · always curious</text>')
    L.append("")

    # final live prompt: types, holds, erases, repeats
    L.append(
        f'    <text y="858">'
        f'<tspan x="{X0}" fill="{c["green"]}" font-weight="700">➜</tspan>'
        f'<tspan x="{XDIR}" fill="{c["cyan"]}">~</tspan></text>'
    )
    L.append(f'    <text x="{XCMD}" y="858" fill="{c["text"]}" clip-path="url(#typing)">{TYPED}</text>')
    L.append('  </g>')
    L.append("")
    L.append(f'  <rect y="843" width="12" height="21" fill="{c["green"]}" x="{XCMD}">')
    L.append(f'    <animate attributeName="x" calcMode="discrete" values="{cursor_vals}" dur="{dur}" repeatCount="indefinite"/>')
    L.append('    <animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/>')
    L.append('  </rect>')
    L.append('</svg>')
    return "\n".join(L) + "\n"


base = "/Users/hatchup/projects/NimaNaghibi143/assets/"
for name, colors in (("zsh-dark.svg", DARK), ("zsh-light.svg", LIGHT)):
    with open(base + name, "w") as f:
        f.write(build(colors))
    print("wrote", name)
