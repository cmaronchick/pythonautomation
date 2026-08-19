# Blood Drive Finder

A monthly GitHub Actions job scrapes Bloodworks Northwest for donation drives near
the ZIP codes associated with the configured AOs, deduplicates drives found in
multiple ZIP searches, and publishes a static GitHub Pages site.

## Configuration

Edit `config.py` to change the AO/ZIP mapping.

## Run locally

```bash
pip install -r requirements.txt
python scraper.py
python generate_site.py
```

The generated data is in `data/blood-drives.json` and the website is in `docs/index.html`.

## GitHub setup

1. Create a GitHub repository and upload this project.
2. In **Settings → Pages**, set the source to **Deploy from a branch**.
3. Select the `main` branch and the `/docs` folder.
4. Save.
5. The workflow will update the site monthly.
6. You can also run **Actions → Update Blood Drives → Run workflow** at any time.

## Scheduling note

The included schedule runs at 15:00 UTC on the first day of each month. This is
8:00 AM Pacific while daylight saving time is in effect. GitHub Actions cron is UTC,
so if you want the exact local-time behavior across DST changes, adjust the schedule
or use a different scheduler.
