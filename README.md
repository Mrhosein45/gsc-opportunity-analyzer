# GSC Opportunity Analyzer

A desktop tool for analyzing Google Search Console data and identifying SEO growth opportunities.

## Features
- CSV upload from Google Search Console
- Automated SEO opportunity detection
- 4-category classification:
  - Quick Win
  - CTR Problem
  - Content Gap
  - Authority Gap
- Opportunity Score (0-100)
- Excel export

## How to use
1. Download or clone repository
2. Run app.py or use exe
3. Upload GSC CSV file
4. Double click any row for analysis

## Requirements
- Python 3.9+
- pandas
- openpyxl

## Build EXE
pyinstaller --onefile --windowed app.py