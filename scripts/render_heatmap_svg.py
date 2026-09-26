import json
import os
from datetime import date, timedelta
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PALETTE = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353', '#69f0a0']

def main():
    data = json.loads((ROOT / 'data/contributions.json').read_text())
    days = data['days']
    first = date.fromisoformat(days[0]['date'])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    columns = ((date.fromisoformat(days[-1]['date']) - start).days // 7) + 1
    pitch = min(14.4, 764 / columns)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="240" viewBox="0 0 860 240" role="img" aria-labelledby="title desc">',
           '<title id="title">Mukund’s GitHub contributions</title>',
           f'<desc id="desc">{data["stats"]["total"]} contributions in the displayed calendar. Updated {data["as_of"]}.</desc>',
           '<rect width="860" height="240" rx="14" fill="#0d1117"/>',
           '<style>text{font-family:monospace;fill:#8b949e;font-size:11px}.day{animation:reveal .5s both}@keyframes reveal{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){.day{animation:none}}</style>',
           '<text x="26" y="28" fill="#39d353">mukundBMW / contribution activity</text>']
    for row, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        svg.append(f'<text x="20" y="{62 + row*15}">{label}</text>')
    seen = set()
    peak = max(d['count'] for d in days)
    for d in days:
        day = date.fromisoformat(d['date']); offset = (day-start).days
        col, row = offset//7, offset%7
        x,y = 62+col*pitch, 52+row*15
        month = day.strftime('%Y-%m')
        if month not in seen and day.day <= 7:
            svg.append(f'<text x="{x:.1f}" y="44">{day:%b}</text>'); seen.add(month)
        level = 5 if peak > 0 and d['count'] == peak else min(d['level'],4)
        animation = '' if os.getenv('STATIC') == '1' else f' class="day" style="animation-delay:{(col+row)*.025:.3f}s"'
        svg.append(f'<rect{animation} x="{x:.1f}" y="{y}" width="11" height="11" rx="2" fill="{PALETTE[level]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>')
    svg.append('<text x="665" y="177">Less</text>')
    for i,color in enumerate(PALETTE):
        svg.append(f'<rect x="{701+i*15}" y="167" width="11" height="11" rx="2" fill="{color}"/>')
    svg.append('<text x="797" y="177">More</text>')
    stats = data['stats']
    svg += [f'<text x="26" y="204">{stats["total"]:,} contributions in the displayed year · current streak {stats["current_streak"]}d · longest {stats["longest_streak"]}d</text>',
            f'<text x="26" y="224">Public GitHub calendar · updated {data["as_of"]}</text>', '</svg>']
    (ROOT/'contrib-heatmap.svg').write_text('\n'.join(svg), encoding='utf-8')
if __name__ == '__main__': main()
