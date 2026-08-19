"""Generate a simple, mobile-friendly static site from blood-drives.json."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from html import escape

from config import OUTPUT_DIR, SITE_DIR


def generate():
    data = json.loads((Path(OUTPUT_DIR) / "blood-drives.json").read_text())
    drives = data["drives"]

    by_ao = defaultdict(list)
    for drive in drives:
        for ao in drive["aos"]:
            by_ao[ao].append(drive)

    ao_sections = []
    for ao in sorted(by_ao):
        rows = []
        for d in by_ao[ao]:
            zips = ", ".join(str(z) for z in d["zip_codes"])
            rows.append(
                f"""
                <tr>
                  <td>{escape(d["date_time"])}</td>
                  <td>{escape(d["drive_name"])}</td>
                  <td>{escape(zips)}</td>
                  <td><a href="{escape(d["url"], quote=True)}" target="_blank" rel="noopener">Details</a></td>
                </tr>
                """
            )

        ao_sections.append(
            f"""
            <section class="ao">
              <h2>{escape(ao)}</h2>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr><th>Date / Time</th><th>Drive</th><th>ZIP</th><th></th></tr>
                  </thead>
                  <tbody>{''.join(rows)}</tbody>
                </table>
              </div>
            </section>
            """
        )

    all_rows = []
    for d in drives:
        all_rows.append(
            f"""
            <tr>
              <td>{escape(d["date_time"])}</td>
              <td>{escape(d["drive_name"])}</td>
              <td>{escape(", ".join(d["aos"]))}</td>
              <td><a href="{escape(d["url"], quote=True)}" target="_blank" rel="noopener">Details</a></td>
            </tr>
            """
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blood Drives</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          margin: 0; background: #f6f7f9; color: #202124; }}
  header {{ background: #fff; border-bottom: 1px solid #ddd; padding: 24px 20px; }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
  h1 {{ margin: 0 0 6px; }}
  h2 {{ margin-top: 32px; }}
  .meta {{ color: #666; font-size: .95rem; }}
  .card {{ background: #fff; border: 1px solid #ddd; border-radius: 10px;
           padding: 16px; margin: 16px 0; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid #eee; }}
  th {{ font-size: .85rem; color: #666; }}
  a {{ color: #b00020; font-weight: 600; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .summary {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }}
  .pill {{ background: #f0f1f3; border-radius: 999px; padding: 7px 12px; }}
</style>
</head>
<body>
<header>
  <main>
    <h1>Blood Drives</h1>
    <div class="meta">Bloodworks Northwest • Updated {escape(data["generated_at"])}</div>
    <div class="summary">
      <div class="pill">{data["drive_count"]} unique drives</div>
      <div class="pill">Through {escape(data["search_through"])}</div>
    </div>
  </main>
</header>
<main>
  <section class="card">
    <h2>All Drives</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Date / Time</th><th>Drive</th><th>Relevant AOs</th><th></th></tr></thead>
        <tbody>{''.join(all_rows) or '<tr><td colspan="4">No drives found.</td></tr>'}</tbody>
      </table>
    </div>
  </section>

  {''.join(ao_sections) or '<div class="card"><p>No drives found.</p></div>'}
</main>
</body>
</html>
"""

    site_path = Path(SITE_DIR)
    site_path.mkdir(parents=True, exist_ok=True)
    (site_path / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {site_path / 'index.html'}")


if __name__ == "__main__":
    generate()
