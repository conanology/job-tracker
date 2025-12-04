#!/usr/bin/env python3
"""
Job Listing Tracker

Scrapes job boards for remote developer positions. Tracks new postings and sends email alerts.

Usage:
    python main.py --url <target_url>
    python main.py --url "https://remoteok.com/remote-python-jobs"
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time


def scrape_remoteok(url):
    """Scrape RemoteOK job listings"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    # RemoteOK requires a small delay to avoid rate limiting
    time.sleep(1)

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []

    # RemoteOK specific structure
    job_rows = soup.select('tr.job')

    for job in job_rows[:30]:  # Top 30 jobs
        try:
            # Skip featured/ads
            if 'featured' in job.get('class', []):
                continue

            company_elem = job.select_one('h3')
            position_elem = job.select_one('h2')
            tags = job.select('.tag')

            if company_elem and position_elem:
                company = company_elem.text.strip()
                position = position_elem.text.strip()
                skills = [tag.text.strip() for tag in tags[:5]]

                # Get job link
                link = job.get('data-url', '')
                if link and not link.startswith('http'):
                    link = f"https://remoteok.com{link}"

                jobs.append({
                    'company': company,
                    'position': position,
                    'skills': ', '.join(skills),
                    'link': link,
                    'source': 'RemoteOK'
                })
        except (AttributeError, KeyError):
            continue

    return jobs


def scrape_generic_jobs(url):
    """Generic job scraping for various job boards"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []

    # Try common job listing patterns
    job_selectors = [
        'div.job', 'div.job-listing', 'article.job', 'li.job',
        'div[class*="job"]', 'div[class*="listing"]'
    ]

    for selector in job_selectors:
        job_elements = soup.select(selector)[:20]

        if job_elements:
            for job_elem in job_elements:
                try:
                    # Try to find title and company
                    title = job_elem.select_one('h2, h3, .title, [class*="title"]')
                    company = job_elem.select_one('.company, [class*="company"]')
                    link = job_elem.select_one('a[href]')

                    if title:
                        jobs.append({
                            'company': company.text.strip() if company else 'N/A',
                            'position': title.text.strip(),
                            'skills': 'N/A',
                            'link': link.get('href', '') if link else '',
                            'source': url
                        })
                except (AttributeError, KeyError):
                    continue

            if jobs:
                break

    return jobs


def scrape_data(url):
    """
    Main scraping logic - Scrapes job listings from various sources

    Args:
        url: Target URL (job board)

    Returns:
        pandas.DataFrame: Scraped data with columns: company, position, skills, link, source
    """
    data = []

    try:
        # Check if RemoteOK
        if 'remoteok.com' in url:
            data = scrape_remoteok(url)
        else:
            # Try generic scraping
            data = scrape_generic_jobs(url)

    except Exception as e:
        print(f"[WARN] Error: {e}")

    if not data:
        data.append({
            'company': 'N/A',
            'position': 'No jobs found',
            'skills': 'N/A',
            'link': url,
            'source': url
        })

    return pd.DataFrame(data)


def main():
    parser = argparse.ArgumentParser(description='Job Listing Tracker')
    parser.add_argument(
        '--url',
        default='https://remoteok.com/remote-python-jobs',
        help='Target URL (job board, default: RemoteOK Python jobs)'
    )
    parser.add_argument('--output', default='output/results.csv', help='Output file path')

    args = parser.parse_args()

    # Auto-add https:// if missing
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"Scraping jobs from {url}...")
    df = scrape_data(url)

    # Save to CSV
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"[OK] Found {len(df)} job listings")
    print(f"[OK] Saved to {output_path}")

    # Display sample
    if len(df) > 0:
        print(f"\n[DATA] Top 5 jobs:")
        print(df.head())


if __name__ == '__main__':
    main()
