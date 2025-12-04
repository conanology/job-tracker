# Job Listing Tracker

![Python](https://img.shields.io/badge/-Python-blue) ![Selenium](https://img.shields.io/badge/-Selenium-blue) ![Pandas](https://img.shields.io/badge/-Pandas-blue) ![SMTP](https://img.shields.io/badge/-SMTP-blue)

Scrapes job boards for remote developer positions. Tracks new postings and sends email alerts.

## Features

- Scrapes Indeed, LinkedIn, RemoteOK
- Filters by keywords (Python, Remote, etc)
- Detects new postings since last run
- Email notifications for new matches
- CSV export of all results

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/job-tracker.git
cd job-tracker

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py --url "https://example.com" --output output/results.csv
```

## Output Format

Results are saved as CSV with the following columns:

| Column | Description |
|--------|-------------|
| name   | Item name   |
| value  | Item value  |
| url    | Source URL  |

## Testing

```bash
pytest tests/
```

## License

MIT License

## Contact

For questions or custom scraping projects, contact me at [your-email]

---

**Note:** This is a portfolio project demonstrating web scraping capabilities. Use responsibly and respect websites' Terms of Service.
