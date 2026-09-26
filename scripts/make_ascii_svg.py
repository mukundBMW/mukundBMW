import os
from html import escape
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
RAMP = ' .`:-=+*cs#%@'

def main():
    photo = Image.open(ROOT/'source-prepped.png').convert('L').resize((100,53),Image.Resampling.LANCZOS)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="370" height="370" viewBox="0 0 700 700" role="img" aria-labelledby="title">',
           '<title id="title">ASCII portrait of Mukund Wuppalapati</title>',
           '<rect width="700" height="700" rx="22" fill="#0d1117"/>',
           '<style>text{font-family:monospace;font-size:10px;fill:#c9d1d9}@media(prefers-reduced-motion:reduce){.row{clip-path:none}.cursor{display:none}}</style>']
    static = os.getenv('STATIC') == '1'
    for row in range(53):
        line = ''.join(RAMP[round((255-photo.getpixel((col,row)))/255*(len(RAMP)-1))] for col in range(100))
        y = 32+row*12; begin = row*.055
        if not static:
            svg.append(f'<defs><clipPath id="r{row}"><rect x="40" y="{y-11}" width="620" height="13"><animate attributeName="width" values="0;0;620" keyTimes="0;{max(.0001,begin/(begin+.35)):.5f};1" begin="0s" dur="{begin+.35}s" fill="freeze"/></rect></clipPath></defs>')
        clip = '' if static else f' class="row" clip-path="url(#r{row})"'
        svg.append(f'<text{clip} x="40" y="{y}" xml:space="preserve" textLength="620" lengthAdjust="spacingAndGlyphs">{escape(line)}</text>')
        if not static:
            svg.append(f'<rect class="cursor" x="40" y="{y-9}" width="5" height="10" fill="#39d353" opacity="0"><set attributeName="opacity" to="1" begin="{begin}s" dur=".35s"/><animate attributeName="x" from="40" to="660" begin="{begin}s" dur=".35s" fill="freeze"/></rect>')
    svg.append('</svg>'); (ROOT/'mukund-ascii.svg').write_text('\n'.join(svg),encoding='utf-8')
if __name__ == '__main__': main()
