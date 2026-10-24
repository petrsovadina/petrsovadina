"""Generate GitHub profile README SVG components in two design systems.

shadcn  - monochrome zinc, Inter, rounded cards (mirrors petrsovadina.cz)
brutal  - neo-brutalist: hard borders, offset shadows, Space Mono, brand magenta

Each component is written in light + dark variants for <picture> switching.
Fonts are subset per file to the glyphs actually used and embedded as WOFF2.
"""
import base64, io, os, re
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools import subset

FD = os.path.join(os.path.dirname(__file__), "fonts")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

# ---------------------------------------------------------------- fonts
FONTS = {
    "body400": ("Inter-400-o14.ttf", 400, "Inter"),
    "body500": ("Inter-500-o14.ttf", 500, "Inter"),
    "body600": ("Inter-600-o14.ttf", 600, "Inter"),
    "disp600": ("Inter-600-o32.ttf", 600, "Inter"),
    "disp700": ("Inter-700-o32.ttf", 700, "Inter"),
    "mono400": ("SpaceMono-Regular.ttf", 400, "Space Mono"),
    "mono700": ("SpaceMono-Bold.ttf", 700, "Space Mono"),
}
FALLBACK = {
    "Inter": "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
    "Space Mono": "'Space Mono', ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, monospace",
}
_tt = {}


def tt(key):
    if key not in _tt:
        _tt[key] = TTFont(os.path.join(FD, FONTS[key][0]))
    return _tt[key]


def text_width(s, key, size, ls=0.0):
    f = tt(key)
    cmap, hmtx, upem = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    w = 0.0
    for ch in s:
        g = cmap.get(ord(ch))
        w += (hmtx[g][0] / upem * size) if g else size * 1.05  # emoji / missing glyph
    return w + ls * max(len(s) - 1, 0)


def wrap(s, key, size, maxw):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if text_width(t, key, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def font_face(key, chars):
    f = TTFont(os.path.join(FD, FONTS[key][0]))
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(unicodes={ord(c) for c in chars if ord(c) < 0x2600} | {0x20})
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f"@font-face{{font-family:'ps-{key}';font-weight:{FONTS[key][1]};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")


# ---------------------------------------------------------------- themes
THEMES = {
    "shadcn": {
        "light": dict(bg="#ffffff", fg="#09090b", muted="#71717a", border="#e4e4e7",
                      secondary="#f4f4f5", primary="#18181b", primary_fg="#fafafa",
                      live="#16a34a", idle="#a1a1aa"),
        "dark": dict(bg="#0d1117", fg="#fafafa", muted="#a1a1aa", border="#27272a",
                     secondary="#27272a", primary="#fafafa", primary_fg="#18181b",
                     live="#22c55e", idle="#71717a"),
    },
    "brutal": {
        "light": dict(bg="#ffffff", fg="#000000", muted="#3f3f46", border="#000000",
                      shadow="#000000", accent="#D84BA4", accent_fg="#000000",
                      chip="#ffffff", live="#D84BA4", idle="#ffffff"),
        "dark": dict(bg="#0d1117", fg="#fafafa", muted="#a1a1aa", border="#fafafa",
                     shadow="#D84BA4", accent="#D84BA4", accent_fg="#000000",
                     chip="#0d1117", live="#D84BA4", idle="#0d1117"),
    },
}

ICONS = {  # lucide (ISC) + simple-icons (CC0)
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "mail": '<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/><rect x="2" y="4" width="20" height="16" rx="2"/>',
    "arrow": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
}
LINKEDIN = "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"  # simple-icons v10 (CC0)


def linkedin_path():
    return LINKEDIN


# ---------------------------------------------------------------- svg builder
class SVG:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.els, self.used, self.css = [], {}, []

    def add(self, s):
        self.els.append(s)

    def text(self, x, y, s, key, size, fill, anchor="start", ls=0.0, extra=""):
        self.used.setdefault(key, set()).update(s)
        fam = FONTS[key][2]
        style = (f"font-family:'ps-{key}',{FALLBACK[fam]};font-weight:{FONTS[key][1]};"
                 f"font-size:{size}px;letter-spacing:{ls:.2f}px")
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" text-anchor="{anchor}" '
                 f'style="{style}" {extra}>{escape(s)}</text>')

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, r=0, extra=""):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def icon(self, name, x, y, size, color, sw=2):
        sc = size / 24
        if name == "linkedin":
            self.add(f'<g transform="translate({x:.1f},{y:.1f}) scale({sc:.4f})">'
                     f'<path d="{linkedin_path()}" fill="{color}"/></g>')
        else:
            self.add(f'<g transform="translate({x:.1f},{y:.1f}) scale({sc:.4f})" fill="none" '
                     f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
                     f'stroke-linejoin="round">{ICONS[name]}</g>')

    def render(self):
        faces = "".join(font_face(k, v) for k, v in self.used.items())
        css = faces + "".join(self.css)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
                f'<title>{escape(self.title)}</title><style>{css}</style>'
                + "".join(self.els) + "</svg>")


def brutal_box(svg, x, y, w, h, c, off=8, sw=3, fill=None):
    svg.rect(x + off, y + off, w, h, fill=c["shadow"])
    svg.rect(x, y, w, h, fill=fill or c["bg"], stroke=c["border"], sw=sw)


PULSE = ("@keyframes ping{0%{transform:scale(1);opacity:.6}80%,100%{transform:scale(2.6);opacity:0}}"
         ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2s cubic-bezier(0,0,.2,1) infinite}"
         "@media (prefers-reduced-motion:reduce){.ping{animation:none;opacity:0}}")


# ---------------------------------------------------------------- components
def hero(theme, c):
    W = 880
    if theme == "shadcn":
        s = SVG(W, 216, "Hey, I'm Petr. AI engineer building tools for Czech healthcare. Open to freelance and consulting. Brno, Czech Republic.")
        s.css.append(PULSE)
        s.text(0, 84, "Hey, I'm Petr 👋", "disp700", 56, c["fg"], ls=-56 * 0.035)
        s.text(0, 126, "AI engineer building tools for Czech healthcare.", "body400", 20, c["muted"])
        label = "Open to freelance & consulting"
        pw = 36 + text_width(label, "body500", 13) + 16
        s.rect(0.5, 160.5, pw, 32, fill=c["bg"], stroke=c["border"], r=16)
        s.add(f'<circle class="ping" cx="18.5" cy="176.5" r="4" fill="{c["live"]}"/>')
        s.add(f'<circle cx="18.5" cy="176.5" r="4" fill="{c["live"]}"/>')
        s.text(32, 181, label, "body500", 13, c["fg"])
        lx = pw + 18
        s.icon("pin", lx, 168, 16, c["muted"])
        s.text(lx + 22, 181, "Brno, Czech Republic", "body400", 14, c["muted"])
        s.add(f'<circle cx="{W-66}" cy="108" r="64" fill="{c["secondary"]}" stroke="{c["border"]}"/>')
        s.text(W - 66, 120, "PS", "disp600", 34, c["fg"], anchor="middle", ls=-0.5)
    else:
        H = 260
        s = SVG(W, H, "Hey, I'm Petr. AI engineer building tools for Czech healthcare. Open to freelance and consulting. Brno, Czech Republic.")
        brutal_box(s, 0, 0, W - 10, H - 10, c)
        p = 36
        s.text(p, 92, "Hey, I'm Petr", "mono700", 50, c["fg"], ls=-1.5)
        s.text(p, 134, "AI engineer building tools for Czech healthcare.", "body400", 19, c["fg"])
        label = "Open to freelance & consulting"
        tw = text_width(label, "mono700", 13) + 28
        s.rect(p + 4, 168 + 4, tw, 34, fill=c["border"])
        s.rect(p, 168, tw, 34, fill=c["accent"], stroke=c["border"], sw=2.5)
        s.text(p + 14, 190, label, "mono700", 13, c["accent_fg"])
        s.text(p + tw + 22, 190, "Brno, CZ", "mono400", 14, c["fg"])
        a = 140
        ax, ay = W - 10 - 36 - a - 6, (H - 10 - a) / 2 - 3
        s.rect(ax + 6, ay + 6, a, a, fill=c["border"])
        s.rect(ax, ay, a, a, fill=c["accent"], stroke=c["border"], sw=3)
        s.text(ax + a / 2, ay + a / 2 + 17, "PS", "mono700", 52, c["accent_fg"], anchor="middle")
    return s


SKILLS = [("Claude", 1), ("MCP", 1), ("RAG", 1), ("LangGraph", 0), ("LangChain", 0),
          ("OpenAI", 0), ("HL7 FHIR", 1), ("Medplum", 1), ("TypeScript", 0), ("Python", 0),
          ("Next.js", 0), ("Nuxt", 0), ("React", 0), ("FastAPI", 0), ("Docker", 0),
          ("Vercel", 0), ("Railway", 0), ("Azure", 0), ("n8n", 0)]


def skills(theme, c):
    W, gap = 880, 8 if theme == "shadcn" else 12
    key = "body600" if theme == "shadcn" else "mono700"
    size, h, padx = (13, 26, 11) if theme == "shadcn" else (13, 32, 12)
    items, x, y = [], 0, 0
    for name, core in SKILLS:
        w = text_width(name, key, size) + padx * 2
        if x + w > W - 8:
            x, y = 0, y + h + gap
        items.append((x, y, w, name, core))
        x += w + gap
    H = y + h + (6 if theme == "brutal" else 2)
    s = SVG(W, H, "Skills: " + ", ".join(n for n, _ in SKILLS))
    for x, y, w, name, core in items:
        if theme == "shadcn":
            fill, fg = (c["primary"], c["primary_fg"]) if core else (c["secondary"], c["fg"])
            s.rect(x + .5, y + .5, w, h, fill=fill, r=6)
            s.text(x + .5 + w / 2, y + .5 + h / 2 + 4.5, name, key, size, fg, anchor="middle")
        else:
            s.rect(x + 3, y + 3, w, h, fill=c["border"] if core else c["shadow"])
            s.rect(x, y, w, h, fill=c["accent"] if core else c["chip"], stroke=c["border"], sw=2.5)
            s.text(x + w / 2, y + h / 2 + 4.5, name, key, size,
                   c["accent_fg"] if core else c["fg"], anchor="middle")
    return s


NOW = [("D", "Doktůrek.ai", "AI products for Czech general practitioners, built on Medplum (FHIR).", "Co-founder"),
       ("A", "ABUGO Group", "Claude, MCP and agent workflows for teams at Reservio, Smartsupp, Survio and more.", "Contract"),
       ("O", "Open source", "MCP servers that connect AI assistants to Czech health data.", "Maintainer")]


def now(theme, c):
    W = 880
    if theme == "shadcn":
        row = 72
        s = SVG(W, row * len(NOW) - 8, "Now: " + "; ".join(f"{t} ({b}): {d}" for _, t, d, b in NOW))
        for i, (ini, t, d, b) in enumerate(NOW):
            y = i * row
            s.add(f'<circle cx="24" cy="{y+28}" r="24" fill="{c["secondary"]}" stroke="{c["border"]}"/>')
            s.text(24, y + 34, ini, "body600", 16, c["fg"], anchor="middle")
            s.text(64, y + 22, t, "body600", 16, c["fg"])
            s.text(64, y + 46, d, "body400", 14, c["muted"])
            bw = text_width(b, "body600", 12) + 20
            s.rect(W - bw - .5, y + 6.5, bw, 24, fill=c["bg"], stroke=c["border"], r=6)
            s.text(W - bw / 2 - .5, y + 23, b, "body600", 12, c["fg"], anchor="middle")
    else:
        row = 80
        H = row * len(NOW) + 10
        s = SVG(W, H, "Now: " + "; ".join(f"{t} ({b}): {d}" for _, t, d, b in NOW))
        brutal_box(s, 0, 0, W - 10, H - 10, c)
        for i, (ini, t, d, b) in enumerate(NOW):
            y = i * row
            if i:
                s.add(f'<line x1="0" x2="{W-10}" y1="{y}" y2="{y}" stroke="{c["border"]}" stroke-width="3"/>')
            s.rect(20, y + 16, 48, 48, fill=c["accent"], stroke=c["border"], sw=2.5)
            s.text(44, y + 47, ini, "mono700", 22, c["accent_fg"], anchor="middle")
            s.text(88, y + 36, t, "mono700", 17, c["fg"])
            s.text(88, y + 60, d, "body400", 14, c["fg"])
            bw = text_width(b, "mono700", 12) + 22
            s.rect(W - 10 - 20 - bw, y + 22, bw, 28, fill=c["chip"], stroke=c["border"], sw=2)
            s.text(W - 10 - 20 - bw / 2, y + 40, b, "mono700", 12, c["fg"], anchor="middle")
    return s


PROJECTS = [
    ("sukl", "SÚKL MCP Server", "live", "Live",
     "Czech medicinal products database for AI agents: 68,000+ products, 9 tools, typo-tolerant search and monthly data refresh via CI.",
     ["TypeScript", "Next.js 16", "MCP", "Vercel"]),
    ("czechmedmcp", "CzechMedMCP", "live", "Live",
     "60 tools in one MCP server: SÚKL, MKN-10, NRPZS, SZV and VZP, plus PubMed, Europe PMC and bioRxiv.",
     ["Python", "MCP", "uv", "Railway"]),
    ("openclinical", "OpenClinical KB CZ", "idle", "Research",
     "Czech guidelines, SPCs and regulatory bulletins turned into structured JSON for RAG and decision support.",
     ["TypeScript", "JSON", "RAG"]),
    ("mkn11", "MKN11-coder", "idle", "Prototype",
     "Assisted ICD-11 coding: GPT-4 extracts diagnoses from free text, suggests MKN-11 codes and scores confidence.",
     ["TypeScript", "Next.js", "OpenAI"]),
]


def card_height(theme):
    inner = 432 - (40 if theme == "shadcn" else 50) - (0 if theme == "shadcn" else 10)
    n = max(len(wrap(p[4], "body400", 14, inner)) for p in PROJECTS)
    return n


def project(theme, c, p):
    _, title, state, status, desc, tags = p
    W = 432
    n = card_height(theme)
    if theme == "shadcn":
        pad = 20
        lines = wrap(desc, "body400", 14, W - 2 * pad)
        H = pad + 22 + 14 + n * 21 + 18 + 22 + pad
        s = SVG(W, H, f"{title} ({status}): {desc} Stack: {', '.join(tags)}.")
        s.rect(.5, .5, W - 1, H - 1, fill=c["bg"], stroke=c["border"], r=12)
        s.text(pad, pad + 17, title, "body600", 17, c["fg"], ls=-0.2)
        tw = text_width(title, "body600", 17, -0.2)
        s.icon("arrow", pad + tw + 6, pad + 4, 15, c["muted"])
        sw = text_width(status, "body500", 12)
        dot = c["live"] if state == "live" else c["idle"]
        s.add(f'<circle cx="{W-pad-sw-10}" cy="{pad+12}" r="3.5" fill="{dot}"/>')
        s.text(W - pad, pad + 16, status, "body500", 12, c["muted"], anchor="end")
        for i, ln in enumerate(lines):
            s.text(pad, pad + 22 + 14 + 14 + i * 21, ln, "body400", 14, c["muted"])
        x, ty = pad, H - pad - 22
        for t in tags:
            w = text_width(t, "body500", 11.5) + 16
            s.rect(x, ty, w, 22, fill=c["secondary"], r=6)
            s.text(x + w / 2, ty + 15, t, "body500", 11.5, c["fg"], anchor="middle")
            x += w + 6
    else:
        pad = 22
        cw = W - 10
        lines = wrap(desc, "body400", 14, cw - 2 * pad)
        H = pad + 24 + 16 + n * 21 + 20 + 28 + pad + 10
        s = SVG(W, H, f"{title} ({status}): {desc} Stack: {', '.join(tags)}.")
        brutal_box(s, 0, 0, cw, H - 10, c)
        s.text(pad, pad + 20, title, "mono700", 18, c["fg"], ls=-0.4)
        sw = text_width(status, "mono700", 11) + 16
        s.rect(cw - pad - sw, pad + 2, sw, 24, fill=c["live"] if state == "live" else c["idle"],
               stroke=c["border"], sw=2)
        s.text(cw - pad - sw / 2, pad + 18, status, "mono700", 11,
               c["accent_fg"] if state == "live" else c["fg"], anchor="middle")
        for i, ln in enumerate(lines):
            s.text(pad, pad + 24 + 16 + 14 + i * 21, ln, "body400", 14, c["fg"])
        x, ty = pad, H - 10 - pad - 28
        for t in tags:
            w = text_width(t, "mono400", 12) + 18
            s.rect(x, ty, w, 28, fill=c["chip"], stroke=c["border"], sw=2)
            s.text(x + w / 2, ty + 18.5, t, "mono400", 12, c["fg"], anchor="middle")
            x += w + 8
    return s


def section(theme, c, label, title, sub):
    W = 880
    s = SVG(W, 150, f"{label}. {title}. {sub}")
    if theme == "shadcn":
        lw = text_width(label, "body500", 14) + 24
        s.rect(W / 2 - lw / 2, 8, lw, 30, fill=c["primary"], r=8)
        s.text(W / 2, 28, label, "body500", 14, c["primary_fg"], anchor="middle")
        s.text(W / 2, 90, title, "disp700", 40, c["fg"], anchor="middle", ls=-40 * 0.035)
        s.text(W / 2, 128, sub, "body400", 17, c["muted"], anchor="middle")
    else:
        lw = text_width(label, "mono700", 14) + 28
        s.rect(W / 2 - lw / 2 + 4, 12, lw, 32, fill=c["accent"])
        s.rect(W / 2 - lw / 2, 8, lw, 32, fill=c["fg"], stroke=c["border"], sw=2)
        s.text(W / 2, 29, label, "mono700", 14, c["bg"], anchor="middle")
        s.text(W / 2, 92, title, "mono700", 36, c["fg"], anchor="middle", ls=-1)
        s.text(W / 2, 130, sub, "body400", 17, c["fg"], anchor="middle")
    return s


BUTTONS = [("email", "mail", "Email me", True),
           ("linkedin", "linkedin", "LinkedIn", False),
           ("website", "globe", "petrsovadina.cz", False)]


def button(theme, c, b):
    _, ic, label, primary = b
    if theme == "shadcn":
        tw = text_width(label, "body500", 14)
        W, H = 16 + 16 + 8 + tw + 18, 42
        s = SVG(int(W) + 2, H, label)
        fill, fg = (c["primary"], c["primary_fg"]) if primary else (c["bg"], c["fg"])
        s.rect(.5, .5, W, H - 1, fill=fill, stroke="none" if primary else c["border"], r=8)
        s.icon(ic, 16.5, 13, 16, fg)
        s.text(40.5, 26, label, "body500", 14, fg)
    else:
        tw = text_width(label, "mono700", 14)
        W, H = 16 + 16 + 10 + tw + 18, 42
        s = SVG(int(W) + 6, H + 5, label)
        s.rect(5, 5, W, H, fill=c["shadow"] if not primary else c["border"])
        fill, fg = (c["accent"], c["accent_fg"]) if primary else (c["chip"], c["fg"])
        s.rect(1.5, 1.5, W - 1, H - 1, fill=fill, stroke=c["border"], sw=2.5)
        s.icon(ic, 17, 14, 16, fg, sw=2.25)
        s.text(43, 27.5, label, "mono700", 14, fg)
    return s


HEADINGS = {"about": "About", "skills": "Skills", "now": "Now", "try": "Try it"}


def heading(c, label):
    W, H = 880, 44
    s = SVG(W, H, label)
    tw = text_width(label, "mono700", 24, -0.5)
    s.rect(0, 28, tw + 6, 10, fill=c["accent"])
    s.text(0, 32, label, "mono700", 24, c["fg"], ls=-0.5)
    s.add(f'<line x1="{tw + 24:.1f}" x2="{W}" y1="24" y2="24" stroke="{c["border"]}" stroke-width="3"/>')
    return s


def write(theme, mode, name, svg):
    d = os.path.join(OUT, theme)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{name}-{mode}.svg"), "w") as f:
        f.write(svg.render())


def build(only=None):
    for theme, modes in THEMES.items():
        if only and theme != only:
            continue
        for mode, c in modes.items():
            if theme == "brutal":
                for k, label in HEADINGS.items():
                    write(theme, mode, f"h-{k}", heading(c, label))
            write(theme, mode, "hero", hero(theme, c))
            write(theme, mode, "skills", skills(theme, c))
            write(theme, mode, "now", now(theme, c))
            for p in PROJECTS:
                write(theme, mode, f"project-{p[0]}", project(theme, c, p))
            write(theme, mode, "projects", section(theme, c, "Projects", "Things I've built",
                                                   "Open-source tools that work with Czech healthcare data."))
            write(theme, mode, "contact", section(theme, c, "Contact", "Let's build something together",
                                                  "Freelance projects and consulting, especially where AI meets real healthcare data."))
            for b in BUTTONS:
                write(theme, mode, f"btn-{b[0]}", button(theme, c, b))


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else None)
    total = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            total += os.path.getsize(os.path.join(root, fn))
    print("files:", sum(len(f) for _, _, f in os.walk(OUT)), "total KB:", round(total / 1024))
