"""Download H&M Group investor reports (https://hmgroup.com/investors/reports/).

Saves PDFs to data/hm/reports/{full-year,quarterly,annual}/. data/ is gitignored.
Files that already exist are skipped.

    python analysis/download_hm_reports.py
"""

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "hm" / "reports"
BASE = "https://hmgroup.com/wp-content/uploads/"

REPORTS = {
    "full-year/2025.pdf": "2026/01/H-M-Hennes-Mauritz-AB-Full-year-report-2025.pdf",
    "full-year/2024.pdf": "2025/01/H-M-Hennes-Mauritz-AB-Full-year-report-2024.pdf",
    "full-year/2023.pdf": "2024/01/H-M-Hennes-Mauritz-AB-Full-year-report-2023.pdf",
    "full-year/2022.pdf": "2023/01/H-M-Hennes-Mauritz-AB-Full-year-report-2022.pdf",
    "full-year/2021.pdf": "2022/01/The-full-report-PDF.pdf",
    "full-year/2020.pdf": "2021/02/H-M-Hennes-Mauritz-AB-Full-year-report-2020.pdf",
    "full-year/2019.pdf": "2020/09/2629510.pdf",
    "full-year/2018.pdf": "2020/09/2371044.pdf",
    "quarterly/2026-3m.pdf": "2026/03/H-M-Hennes-Mauritz-AB-Three-month-report-2026.pdf",
    "quarterly/2026-6m.pdf": "2026/06/H-M-Hennes-Mauritz-AB-Six-month-report-2026.pdf",
    "quarterly/2026-9m.pdf": "2026/09/H-M-Hennes-Mauritz-AB-Nine-month-report-2026.pdf",
    "quarterly/2025-3m.pdf": "2025/03/H-M-Hennes-Mauritz-AB-Three-month-report-2025.pdf",
    "quarterly/2025-6m.pdf": "2025/06/H-M-Hennes-Mauritz-AB-Six-month-report-2025.pdf",
    "quarterly/2025-9m.pdf": "2025/09/H-M-Hennes-Mauritz-AB-Nine-month-report-2025.pdf",
    "quarterly/2020-3m.pdf": "2020/09/2680113.pdf",
    "quarterly/2020-6m.pdf": "2020/09/2735858.pdf",
    "quarterly/2020-9m.pdf": "2020/11/2792222.pdf",
    "quarterly/2019-3m.pdf": "2021/01/2412194.pdf",
    "quarterly/2019-6m.pdf": "2020/09/Six-month-report-Q2-2019.pdf",
    "quarterly/2019-9m.pdf": "2020/09/2543618.pdf",
    "quarterly/2018-3m.pdf": "2020/09/2145888_en.pdf",
    "quarterly/2018-6m.pdf": "2020/09/2217836.pdf",
    "quarterly/2018-9m.pdf": "2020/09/2281603.pdf",
    "annual/2025.pdf": "2026/03/HM-Group-Annual-and-sustainability-report-2025.pdf",
    "annual/2024.pdf": "2025/03/HM-Group-Annual-and-sustainability-report-2024.pdf",
    "annual/2023.pdf": "2024/03/HM-Group-Annual-and-Sustainability-Report-2023.pdf",
    "annual/2022.pdf": "2023/03/HM-Group-Annual-and-Sustainability-Report-2022.pdf",
    "annual/2021.pdf": "2022/03/HM-Group-Annual-and-Sustainability-Report-2021.pdf",
    "annual/2020.pdf": "2021/04/HM-Annual-Report-2020.pdf",
    "annual/2019.pdf": "2020/10/HM_Annual-Report-2019.pdf",
    "annual/2018.pdf": "2020/09/Annual-Report-2018.pdf",
}


def main():
    failed = []
    for name, path in REPORTS.items():
        target = OUT / name
        if target.exists():
            print(f"skip  {name}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
        except Exception as e:
            failed.append(name)
            print(f"FAIL  {name}: {e}")
            continue
        if not data.startswith(b"%PDF"):
            failed.append(name)
            print(f"FAIL  {name}: not a PDF")
            continue
        target.write_bytes(data)
        print(f"ok    {name} ({len(data) / 1e6:.1f} MB)")
    print(f"\n{len(REPORTS) - len(failed)}/{len(REPORTS)} reports in {OUT}")
    if failed:
        print("failed:", ", ".join(failed))


if __name__ == "__main__":
    main()
