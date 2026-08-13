#!/usr/bin/env python3
"""
render_card.py — builds a neofetch-style SVG stats card:
  - ASCII art on the left
  - dot-leader "Key: ..... value" rows on the right, grouped into sections
Matches the structural style of Andrew6rant's profile README card.
"""

# A simple original ASCII art block (terminal/laptop glyph) — swap this out
# for anything you like, e.g. your own initials in ASCII, a different icon,
# or a converted image via the ascii_readme.py script from earlier.
ASCII_ART = r"""
     ___________________
    |  _______________  |
    | |               | |
    | |   > _         | |
    | |               | |
    | |_______________| |
    |___________________|
     \_________________/
"""


def dot_leader(key, value, total_width=38):
    """Pad between key and value with dots, neofetch-style."""
    used = len(key) + 2  # ": "
    dots_len = max(total_width - used - len(value), 3)
    return "." * dots_len


# Each item: (key, value)
# Each section: (heading, [items])
SECTIONS = [
    ("Info", [
        ("OS", "Windows 11"),
        ("Role", "Aspiring SDE-1 / Full-Stack Developer"),
        ("Education", "B.Tech IT, IET Lucknow"),
    ]),
    ("Languages", [
        ("Programming", "Python, JavaScript, Java, C++"),
        ("Web", "HTML, CSS, TypeScript"),
    ]),
    ("Contact", [
        ("GitHub", "shivangi-tiwari"),
        ("LinkedIn", "shivangi-tiwarii07"),
    ]),
    ("GitHub Stats", [
        ("Repos", "{repos}"),
        ("Stars", "{stars}"),
        ("Followers", "{followers}"),
        ("Commits (past yr)", "{commits_last_year}"),
    ]),
]

THEMES = {
    "dark": {
        "bg": "#161b22", "fg": "#c9d1d9", "key": "#ffa657",
        "value": "#a5d6ff", "muted": "#616e7f",
    },
    "light": {
        "bg": "#ffffff", "fg": "#24292f", "key": "#953800",
        "value": "#0550ae", "muted": "#8c959f",
    },
}


def render_svg(username, stats, theme="dark"):
    c = THEMES[theme]
    line_h = 20
    y = 30

    art_lines = ASCII_ART.strip("\n").split("\n")
    art_tspans = []
    ay = y
    for line in art_lines:
        escaped = (line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        art_tspans.append(f'<tspan x="20" y="{ay}">{escaped}</tspan>')
        ay += line_h

    info_x = 340
    iy = y
    info_tspans = [f'<tspan x="{info_x}" y="{iy}">{username}@github</tspan> ' + "-" * 40]
    iy += line_h * 1.5

    for heading, items in SECTIONS:
        info_tspans.append(f'<tspan x="{info_x}" y="{int(iy)}">- {heading}</tspan> ' + "-" * (38 - len(heading)))
        iy += line_h
        for key, value in items:
            value = value.format(**stats)
            dots = dot_leader(key, value)
            info_tspans.append(
                f'<tspan x="{info_x}" y="{int(iy)}" fill="{c["muted"]}">. </tspan>'
                f'<tspan fill="{c["key"]}">{key}</tspan>'
                f'<tspan fill="{c["muted"]}">: {dots} </tspan>'
                f'<tspan fill="{c["value"]}">{value}</tspan>'
            )
            iy += line_h
        iy += line_h * 0.5

    height = max(int(ay) + 20, int(iy) + 20)
    width = 900

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}px" height="{height}px"
     font-family="Consolas, 'Courier New', monospace" font-size="14px">
<rect width="{width}px" height="{height}px" fill="{c['bg']}" rx="15"/>
<text fill="{c['fg']}">
{chr(10).join(art_tspans)}
</text>
<text fill="{c['fg']}">
{chr(10).join(info_tspans)}
</text>
</svg>'''
    return svg
