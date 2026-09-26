"""Fetch public calendar counts. Fail on unknown HTML instead of inventing zeros."""
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
USERNAME = 'mukundBMW'

def parse_calendar(html, today):
    soup = BeautifulSoup(html, 'html.parser')
    tips = {t.get('for'): t.get_text(' ', strip=True) for t in soup.find_all('tool-tip')}
    days = {}
    for cell in soup.select('[data-date][data-level]'):
        day = date.fromisoformat(cell['data-date'])
        if day > today:
            continue
        label = tips.get(cell.get('id'), '')
        match = re.search(r'\b([\d,]+) contributions?\b', label, re.I)
        if match:
            count = int(match.group(1).replace(',', ''))
        elif re.search(r'\bNo contributions?\b', label, re.I):
            count = 0
        else:
            raise ValueError(f'Missing contribution count for {day}: {label!r}')
        days[day.isoformat()] = {'date': day.isoformat(), 'count': count, 'level': int(cell['data-level'])}
    result = sorted(days.values(), key=lambda d: d['date'])
    if len(result) < 350:
        raise ValueError(f'Incomplete calendar: {len(result)} days; keeping previous data')
    for a, b in zip(result, result[1:]):
        if date.fromisoformat(b['date']) - date.fromisoformat(a['date']) != timedelta(days=1):
            raise ValueError('Calendar has missing dates')
    return result

def derive_stats(days):
    longest = run = 0
    monthly = {}
    for day in days:
        run = run + 1 if day['count'] else 0
        longest = max(longest, run)
        month = day['date'][:7]
        monthly[month] = monthly.get(month, 0) + day['count']
    # Today's unfinished day does not break yesterday's active streak.
    tail = days[:-1] if days and days[-1]['count'] == 0 else days
    current = 0
    for day in reversed(tail):
        if not day['count']:
            break
        current += 1
    return {'total': sum(d['count'] for d in days), 'current_streak': current,
            'longest_streak': longest, 'best_day': max(days, key=lambda d: d['count']),
            'monthly_totals': monthly}

def main():
    response = requests.get(f'https://github.com/users/{USERNAME}/contributions',
                            headers={'User-Agent': 'mukundBMW-profile-calendar'}, timeout=30)
    response.raise_for_status()
    today = datetime.now(timezone.utc).date()
    days = parse_calendar(response.text, today)
    data = {'username': USERNAME, 'as_of': today.isoformat(), 'days': days, 'stats': derive_stats(days)}
    out = ROOT / 'data/contributions.json'
    out.parent.mkdir(exist_ok=True)
    temporary = out.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    temporary.replace(out)
    print(f"Saved {len(days)} days, {data['stats']['total']} contributions")

if __name__ == '__main__':
    main()
