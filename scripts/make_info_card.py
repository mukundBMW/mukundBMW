import os
from html import escape
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ROWS = [
 ('Role', 'Game & Systems Designer'),
 ('Focus', 'Gameplay loops · Progression · UX/UI'),
 ('Now', 'MSc Game Design'),
 ('', 'Staffordshire University'),
 ('Prev', 'B.Tech Computer Science · KL University'),
 ('Stack', 'Unreal Engine 5 · Blueprints · Unity'),
 ('Building', 'Paws & Parcels'),
 ('', 'A stylized animal delivery game'),
 ('Highlights', 'Mayavi Club game-design masterclasses'),
 ('Interests', 'Game systems · UI · Web'),
]

def main():
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="490" height="370" viewBox="0 0 490 370" role="img" aria-labelledby="title">',
           '<title id="title">Mukund Wuppalapati — Game and Systems Designer</title>',
           '<rect width="490" height="370" rx="12" fill="#0d1117"/>',
           '<path d="M0 40H490" stroke="#30363d"/>',
           '<style>text{font-family:monospace;font-size:12px;fill:#c9d1d9}.line{animation:print .45s both}@keyframes print{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:translateX(0)}}@media(prefers-reduced-motion:reduce){.line{animation:none}}</style>',
           '<circle cx="18" cy="20" r="4" fill="#ff5f57"/><circle cx="32" cy="20" r="4" fill="#febc2e"/><circle cx="46" cy="20" r="4" fill="#28c840"/>',
           '<text x="67" y="24">mukund@github ~ $ neofetch</text>',
           '<text x="20" y="70" style="font-size:19px;fill:#f0f6fc">Mukund Wuppalapati</text>',
           '<text x="20" y="91" style="fill:#39d353">Designing systems that feel good to play.</text>']
    for i,(key,value) in enumerate(ROWS):
        anim = '' if os.getenv('STATIC') == '1' else f' class="line" style="animation-delay:{.2+i*.12:.2f}s"'
        svg.append(f'<g{anim}><text x="20" y="{124+i*23}" style="fill:#39d353">{escape(key)}</text><text x="110" y="{124+i*23}">{escape(value)}</text></g>')
    svg.append('</svg>')
    (ROOT/'info-card.svg').write_text('\n'.join(svg),encoding='utf-8')
if __name__ == '__main__': main()
