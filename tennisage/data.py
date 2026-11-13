"""Download and clean Tennis Abstract career match data."""

import json
import re
from datetime import date, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

import pandas as pd

_BASE = "https://www.tennisabstract.com"
_COLUMNS = [
    "date",
    "tournament",
    "surface",
    "result",
    "opponent",
    "player_age",
    "opponent_age",
    "age_difference",
]


def _player_slug(name):
    words = re.findall(r"[A-Za-z0-9]+", name.strip())
    if not words:
        raise ValueError("Enter a player name, such as 'Serena Williams'.")
    if len(words) == 1:
        return words[0][0].upper() + words[0][1:]
    return "".join(word[0].upper() + word[1:] for word in words)


def _read_url(url):
    request = Request(url, headers={"User-Agent": "tennisage/0.1"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def _fetch_career_js(slug):
    url = f"{_BASE}/jsmatches/{quote(slug)}Career.js"
    try:
        return _read_url(url)
    except (HTTPError, URLError, TimeoutError) as error:
        message = f"No Tennis Abstract career file was found for '{slug}'."
        raise ValueError(message + " Check the player name.") from error


def _fetch_birth_date(slug):
    url = f"{_BASE}/cgi-bin/player.cgi?p={quote(slug)}"
    try:
        page = _read_url(url)
    except (HTTPError, URLError, TimeoutError):
        return None
    pattern = r"Born\s*:?\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})"
    match = re.search(pattern, page, re.I)
    if match:
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(match.group(1), fmt).date()
            except ValueError:
                pass
    match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", page)
    return date.fromisoformat(match.group(1)) if match else None


def _parse_career_js(source):
    pattern = r"var\s+morematchmx\s*=\s*(\[\s*\[.*?\]\s*\])\s*;"
    match = re.search(pattern, source, re.S)
    if not match:
        raise ValueError("The career file has no readable morematchmx array.")
    return json.loads(match.group(1))


def _age_on(match_date, birth_date):
    return (match_date - birth_date).days / 365.2425


def _opponent_age(raw_age, match_date):
    value = str(raw_age).strip()
    if re.fullmatch(r"\d{8}", value):
        birth_date = datetime.strptime(value, "%Y%m%d").date()
        return _age_on(match_date, birth_date)
    try:
        return float(value)
    except ValueError:
        return None


def _clean_row(row, player_birth_date):
    match_date = datetime.strptime(str(row[0]), "%Y%m%d").date()
    result = str(row[4]).upper()
    opponent_age = _opponent_age(row[16], match_date)
    if result not in {"W", "L"} or opponent_age is None:
        return None
    player_age = _age_on(match_date, player_birth_date)
    age_gap = player_age - opponent_age
    return [
        match_date, row[1], row[2], result, row[11],
        player_age, opponent_age, age_gap,
    ]


def _process_career_js(source, player_birth_date):
    rows = _parse_career_js(source)
    cleaned = [_clean_row(row, player_birth_date) for row in rows]
    cleaned = [row for row in cleaned if row is not None]
    if not cleaned:
        raise ValueError("No completed matches with usable age data were found.")
    return pd.DataFrame(cleaned, columns=_COLUMNS)


def get_career_data(player_name):
    """Return cleaned match data for a Tennis Abstract player name."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Enter a player name, such as 'Serena Williams'.")
    slug = _player_slug(player_name)
    source = _fetch_career_js(slug)
    birth_date = _fetch_birth_date(slug)
    if birth_date is None:
        message = f"Could not find a birth date for '{player_name}'."
        raise ValueError(message)
    return _process_career_js(source, birth_date)
