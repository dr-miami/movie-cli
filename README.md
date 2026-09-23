# 67movies.net CLI

A simple command‑line tool to search for movies and TV shows on 67movies.net and open the video player in your browser.

## Features

- Search for movies and TV shows via The Movie Database (TMDB) API.
- Browse seasons and episodes for TV shows.
- Opens the embed player directly in your default browser.
- Lightweight and fast – no video player required (uses browser for playback with subtitles and quality options).

## Requirements

- Python 3.7+
- A free [TMDB API key](https://www.themoviedb.org/signup)
*(api key is required for the program to find movies)*

## Installation

1. Clone or download this repository.
2. Create a virtual environment (optional but recommended):
 - python -m venv venv
 - source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies:
   - pip install -r requirements.txt
4. Create a `.env` file in the project root with your TMDB API key:
   - TMDB_API_KEY=your_api_key_here

## Usage

Run the CLI:
### python
> python cli.py
### uv
> uv run cli.py

Follow the interactive prompts:

1. Choose **Movies** or **TV Shows**.
2. Enter a title (e.g., `Inception` or `Breaking Bad`).
3. Select the correct result from the list.
4. For TV shows, choose a season and then an episode.
5. The embed URL will open automatically in your default web browser.

> **Note:** The video player is opened in your browser, where you can use the built‑in controls to enable subtitles, adjust quality, and more.

## File Structure

```
.
├── cli.py          # Command‑line interface
├── scraper.py      # Search and embed extraction logic
├── requirements.txt
├── .env            # TMDB_API_KEY (not included in repo)
└── README.md
```

## Dependencies

- `requests` – HTTP requests.
- `beautifulsoup4` – HTML parsing.
- `lxml` – Fast XML/HTML parser.
- `python-dotenv` – Load environment variables.
- `colorama` – Coloured terminal output.
- `InquirerPy` – Interactive CLI menus.

## Disclaimer

This tool is for educational purposes only. Please respect the content providers' terms of service. Use at your own risk.

## License

MIT