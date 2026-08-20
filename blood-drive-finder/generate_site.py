"""Generate the static Blood Drive Finder site."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

from blooddrivedata import OUTPUT_DIR, SITE_DIR


def generate():
    data = json.loads(
        (Path(OUTPUT_DIR) / "blood-drives.json").read_text(encoding="utf-8")
    )
    drives = data["drives"]

    all_aos = sorted(
        {ao for drive in drives for ao in drive.get("aos", [])},
        key=str.casefold,
    )

    rows = []
    for index, drive in enumerate(drives):
        rows.append(
            f"""
            <tr data-index="{index}"
                data-date="{escape(drive.get("date") or "9999-12-31")}"
                data-aos="{escape("|".join(drive.get("aos", [])), quote=True)}">
              <td>{escape(drive["date_time"])}</td>
              <td>{escape(drive["drive_name"])}</td>
              <td>{escape(", ".join(drive.get("aos", [])))}</td>
              <td>{escape(", ".join(drive.get("zip_codes", [])))}</td>
              <td>
                <a href="{escape(drive["url"], quote=True)}"
                   target="_blank" rel="noopener">Details</a>
              </td>
            </tr>
            """
        )

    ao_options = ['<option value="">All AOs</option>']
    ao_options += [
        f'<option value="{escape(ao, quote=True)}">{escape(ao)}</option>'
        for ao in all_aos
    ]

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blood Drives</title>
<style>
  :root {{
    color-scheme: light;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: 0;
    background: #f6f7f9;
    color: #202124;
  }}
  header {{
    background: #fff;
    border-bottom: 1px solid #ddd;
    padding: 24px 20px;
  }}
  main {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 20px;
  }}
  h1 {{ margin: 0 0 6px; }}
  h2 {{ margin-top: 32px; }}
  .meta {{ color: #666; font-size: .95rem; }}
  .card {{
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 16px;
    margin: 16px 0;
  }}
  .controls {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    align-items: end;
  }}
  .control {{
    display: flex;
    flex-direction: column;
    gap: 5px;
  }}
  label {{
    font-size: .82rem;
    color: #666;
    font-weight: 600;
  }}
  select, button {{
    font: inherit;
    padding: 9px 11px;
    border: 1px solid #bbb;
    border-radius: 7px;
    background: #fff;
  }}
  button {{ cursor: pointer; }}
  .count {{ margin-left: auto; color: #666; align-self: center; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{
    text-align: left;
    padding: 10px 8px;
    border-bottom: 1px solid #eee;
    vertical-align: top;
  }}
  th {{
    font-size: .85rem;
    color: #666;
    white-space: nowrap;
  }}
  a {{
    color: #b00020;
    font-weight: 600;
    text-decoration: none;
  }}
  a:hover {{ text-decoration: underline; }}
  .empty {{ display: none; color: #666; padding: 18px 0 4px; }}
  @media (max-width: 700px) {{
    main {{ padding: 12px; }}
    header {{ padding: 18px 12px; }}
    .count {{ width: 100%; margin-left: 0; }}
  }}
</style>
</head>
<body>
<header>
  <main>
    <h1>Blood Drives</h1>
    <div class="meta">
      Bloodworks Northwest • Updated {escape(data["generated_at"])}
    </div>
  </main>
</header>

<main>
  <section class="card">
    <div class="controls">
      <div class="control">
        <label for="aoFilter">AO</label>
        <select id="aoFilter">
          {''.join(ao_options)}
        </select>
      </div>

      <div class="control">
        <label for="dateSort">Sort by date</label>
        <select id="dateSort">
          <option value="asc">Soonest first</option>
          <option value="desc">Latest first</option>
        </select>
      </div>

      <button id="resetButton" type="button">Reset</button>
      <div class="count" id="resultCount"></div>
    </div>
  </section>

  <section class="card">
    <h2>Upcoming Blood Drives</h2>
    <div class="table-wrap">
      <table id="drivesTable">
        <thead>
          <tr>
            <th>Date / Time</th>
            <th>Drive</th>
            <th>AO(s)</th>
            <th>ZIP</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
      <div class="empty" id="emptyMessage">
        No drives match the selected AO.
      </div>
    </div>
  </section>
</main>

<script>
(function () {{
  const table = document.getElementById("drivesTable");
  const tbody = table.querySelector("tbody");
  const aoFilter = document.getElementById("aoFilter");
  const dateSort = document.getElementById("dateSort");
  const resetButton = document.getElementById("resetButton");
  const resultCount = document.getElementById("resultCount");
  const emptyMessage = document.getElementById("emptyMessage");

  function rows() {{
    return Array.from(tbody.querySelectorAll("tr"));
  }}

  function update() {{
    const selectedAO = aoFilter.value;
    const direction = dateSort.value === "desc" ? -1 : 1;

    const filtered = rows().filter(row => {{
      const aos = row.dataset.aos
        ? row.dataset.aos.split("|")
        : [];
      return !selectedAO || aos.includes(selectedAO);
    }});

    filtered.sort((a, b) => {{
      const dateA = a.dataset.date || "9999-12-31";
      const dateB = b.dataset.date || "9999-12-31";
      const dateCompare = dateA.localeCompare(dateB);
      if (dateCompare !== 0) return dateCompare * direction;

      const textA = a.cells[0].textContent;
      const textB = b.cells[0].textContent;
      return textA.localeCompare(textB) * direction;
    }});

    // Re-append all rows in sorted order. Nonmatching rows are hidden.
    rows().forEach(row => {{
      row.style.display = "none";
    }});

    filtered.forEach(row => {{
      row.style.display = "";
      tbody.appendChild(row);
    }});

    resultCount.textContent =
      filtered.length + " drive" + (filtered.length === 1 ? "" : "s");

    emptyMessage.style.display = filtered.length ? "none" : "block";
  }}

  aoFilter.addEventListener("change", update);
  dateSort.addEventListener("change", update);

  resetButton.addEventListener("click", function () {{
    aoFilter.value = "";
    dateSort.value = "asc";
    update();
  }});

  update();
}})();
</script>
</body>
</html>
"""

    site_path = Path(SITE_DIR)
    site_path.mkdir(parents=True, exist_ok=True)
    (site_path / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {site_path / 'index.html'}")


if __name__ == "__main__":
    generate()
