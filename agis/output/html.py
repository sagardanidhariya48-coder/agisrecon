"""
AgisRecon2 - HTML Output

Handles formatting and saving reconnaissance results as a
single self-contained HTML report.

The generated report is one standalone file with embedded
styles and scripts, so it can be opened in any browser or
attached to a scan without shipping extra assets.

Features
--------
- Summary header with scan metadata
- Statistic cards per report
- Search across every finding
- Severity and status filtering
- Collapsible per-tool sections
- Print friendly layout
"""

from __future__ import annotations

import html as _html
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union


# ANSI escape sequences emitted by colourful CLI tools.
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

# Severity tokens used by vulnerability scanners such as Nuclei.
SEVERITY_PATTERN = re.compile(
    r"\[(critical|high|medium|low|info|unknown)\]",
    re.IGNORECASE,
)

# Nmap style port entries: 631/tcp open  ipp  CUPS 2.4
PORT_PATTERN = re.compile(
    r"^(\d+)/(tcp|udp)\s+(open|closed|filtered|open\|filtered)",
    re.IGNORECASE,
)

# HTTP status codes reported by HTTPX and similar tools.
HTTP_STATUS_PATTERN = re.compile(r"\[(\d{3})\]")

# Order used when several tools are part of the same report.
TOOL_ORDER = (
    "subfinder",
    "assetfinder",
    "dnsx",
    "httpx",
    "nmap",
    "waybackurls",
    "katana",
    "nuclei",
)


# --------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------

STYLES = """
:root {
  --bg: #0b0f14;
  --bg-soft: #10161d;
  --panel: #131b24;
  --panel-alt: #17212c;
  --border: #22303d;
  --text: #e6edf3;
  --muted: #8b98a5;
  --accent: #38bdf8;
  --accent-soft: rgba(56, 189, 248, 0.12);
  --critical: #f43f5e;
  --high: #fb923c;
  --medium: #fbbf24;
  --low: #a3e635;
  --info: #60a5fa;
  --ok: #34d399;
  --shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--text);
  font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 15px;
  line-height: 1.55;
}

a {
  color: var(--accent);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code,
pre {
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  font-size: 13px;
}

/* ---------------------------------------------------------
   Header
   --------------------------------------------------------- */

.hero {
  border-bottom: 1px solid var(--border);
  background:
    radial-gradient(1200px 400px at 15% -10%, rgba(56, 189, 248, 0.16), transparent),
    linear-gradient(180deg, #0e141b 0%, var(--bg) 100%);
  padding: 34px 24px 28px;
}

.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.eyebrow {
  margin: 0 0 6px;
  color: var(--accent);
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.hero h1 {
  margin: 0 0 16px;
  font-size: 28px;
  line-height: 1.25;
  word-break: break-word;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--panel);
  color: var(--muted);
  font-size: 13px;
}

.chip b {
  color: var(--text);
  font-weight: 600;
}

/* ---------------------------------------------------------
   Statistic cards
   --------------------------------------------------------- */

.stats {
  max-width: 1200px;
  margin: 0 auto;
  padding: 22px 24px 6px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
}

.stat {
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--panel);
  padding: 14px 16px;
}

.stat .label {
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.stat .value {
  margin-top: 4px;
  font-size: 24px;
  font-weight: 700;
}

.stat .value.accent {
  color: var(--accent);
}

.stat .value.critical {
  color: var(--critical);
}

.stat .value.high {
  color: var(--high);
}

.stat .value.medium {
  color: var(--medium);
}

.stat .value.low {
  color: var(--low);
}

.stat .value.info {
  color: var(--info);
}

/* ---------------------------------------------------------
   Toolbar
   --------------------------------------------------------- */

.toolbar {
  position: sticky;
  top: 0;
  z-index: 20;
  max-width: 1200px;
  margin: 16px auto 0;
  padding: 12px 14px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: rgba(19, 27, 36, 0.95);
  backdrop-filter: blur(6px);
  box-shadow: var(--shadow);
}

.toolbar input[type="search"] {
  flex: 1 1 240px;
  min-width: 200px;
  padding: 9px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-soft);
  color: var(--text);
  font-size: 14px;
}

.toolbar input[type="search"]:focus {
  outline: 1px solid var(--accent);
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.filters button,
.actions button {
  padding: 7px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-soft);
  color: var(--muted);
  font-size: 13px;
  cursor: pointer;
}

.filters button:hover,
.actions button:hover {
  color: var(--text);
  border-color: var(--accent);
}

.filters button.active {
  background: var(--accent-soft);
  border-color: var(--accent);
  color: var(--accent);
}

.spacer {
  flex: 1 1 auto;
}

.actions {
  display: flex;
  gap: 6px;
}

/* ---------------------------------------------------------
   Panels
   --------------------------------------------------------- */

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 18px 24px 40px;
}

.panel {
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--panel);
  margin-bottom: 16px;
  overflow: hidden;
}

.panel > h2 {
  margin: 0;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  background: var(--panel-alt);
  font-size: 15px;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  color: var(--muted);
}

.panel-body {
  padding: 14px 16px;
}

/* ---------------------------------------------------------
   Scan sections
   --------------------------------------------------------- */

.scan-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  padding: 13px 16px;
  cursor: pointer;
  user-select: none;
}

.scan-head:hover {
  background: var(--panel-alt);
}

.scan-title {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1 1 auto;
}

.scan-meta {
  color: var(--muted);
  font-size: 12.5px;
  word-break: break-all;
}

.chevron {
  color: var(--muted);
  transition: transform 0.15s ease;
}

.scan.collapsed .chevron {
  transform: rotate(-90deg);
}

.scan.collapsed .scan-body {
  display: none;
}

.scan-body {
  border-top: 1px solid var(--border);
  padding: 12px 16px 16px;
}

.badge {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  border: 1px solid transparent;
}

.badge.tool {
  background: var(--accent-soft);
  border-color: var(--accent);
  color: var(--accent);
}

.badge.count {
  background: var(--panel-alt);
  border-color: var(--border);
  color: var(--muted);
}

.badge.sev-critical { background: rgba(244, 63, 94, 0.16); border-color: var(--critical); color: var(--critical); }
.badge.sev-high     { background: rgba(251, 146, 60, 0.16); border-color: var(--high); color: var(--high); }
.badge.sev-medium   { background: rgba(251, 191, 36, 0.16); border-color: var(--medium); color: var(--medium); }
.badge.sev-low      { background: rgba(163, 230, 53, 0.16); border-color: var(--low); color: var(--low); }
.badge.sev-info     { background: rgba(96, 165, 250, 0.16); border-color: var(--info); color: var(--info); }
.badge.sev-unknown  { background: rgba(139, 152, 165, 0.16); border-color: var(--muted); color: var(--muted); }

.badge.state-open     { background: rgba(52, 211, 153, 0.16); border-color: var(--ok); color: var(--ok); }
.badge.state-closed   { background: rgba(139, 152, 165, 0.16); border-color: var(--muted); color: var(--muted); }
.badge.state-filtered { background: rgba(251, 191, 36, 0.14); border-color: var(--medium); color: var(--medium); }

.badge.http-2xx { background: rgba(52, 211, 153, 0.16); border-color: var(--ok); color: var(--ok); }
.badge.http-3xx { background: rgba(96, 165, 250, 0.16); border-color: var(--info); color: var(--info); }
.badge.http-4xx { background: rgba(251, 191, 36, 0.16); border-color: var(--medium); color: var(--medium); }
.badge.http-5xx { background: rgba(244, 63, 94, 0.16); border-color: var(--critical); color: var(--critical); }

/* ---------------------------------------------------------
   Result tables
   --------------------------------------------------------- */

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  text-align: left;
  vertical-align: top;
  word-break: break-word;
}

th {
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  background: var(--panel-alt);
}

tbody tr:hover {
  background: rgba(56, 189, 248, 0.05);
}

td.idx {
  width: 1%;
  color: var(--muted);
  font-size: 12px;
  white-space: nowrap;
}

td.tag {
  width: 1%;
  white-space: nowrap;
}

.empty {
  margin: 0;
  padding: 12px 0;
  color: var(--muted);
  font-style: italic;
}

.key {
  color: var(--accent);
  font-weight: 600;
  white-space: nowrap;
  vertical-align: top;
}

.nested {
  border-left: 2px solid var(--border);
  padding-left: 12px;
}

pre.raw {
  margin: 0;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-soft);
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

/* ---------------------------------------------------------
   Footer
   --------------------------------------------------------- */

footer {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 34px;
  color: var(--muted);
  font-size: 12.5px;
  text-align: center;
}

.hidden {
  display: none !important;
}

/* ---------------------------------------------------------
   Print
   --------------------------------------------------------- */

@media print {
  body {
    background: #ffffff;
    color: #111111;
  }

  .toolbar {
    display: none;
  }

  .hero {
    background: #ffffff;
    border-bottom: 2px solid #111111;
  }

  .eyebrow,
  .chip,
  .scan-meta,
  .stat .label {
    color: #444444;
  }

  .chip,
  .stat,
  .panel {
    background: #ffffff;
    border-color: #cccccc;
  }

  .stat .value {
    color: #111111 !important;
  }

  .panel > h2 {
    background: #f0f0f0;
    color: #222222;
  }

  .scan-body {
    display: block !important;
  }
}
"""


# --------------------------------------------------------------------
# Scripts
# --------------------------------------------------------------------

SCRIPTS = """
(function () {
  var search = document.getElementById("search");
  var rows = Array.prototype.slice.call(
    document.querySelectorAll("tr[data-row]")
  );
  var scans = Array.prototype.slice.call(
    document.querySelectorAll(".scan")
  );
  var filters = Array.prototype.slice.call(
    document.querySelectorAll(".filters button")
  );
  var counter = document.getElementById("visible-count");
  var active = "all";

  function currentFilter() {
    return active;
  }

  function apply() {
    var query = search ? search.value.trim().toLowerCase() : "";
    var filter = currentFilter();
    var visible = 0;

    rows.forEach(function (row) {
      var text = (row.textContent || "").toLowerCase();
      var tag = row.getAttribute("data-tag") || "";

      var matchText = !query || text.indexOf(query) !== -1;
      var matchTag = filter === "all" || tag === filter;

      if (matchText && matchTag) {
        row.classList.remove("hidden");
        visible += 1;
      } else {
        row.classList.add("hidden");
      }
    });

    scans.forEach(function (scan) {
      var body = scan.querySelector(".scan-body");
      var shown = body
        ? body.querySelectorAll("tr[data-row]:not(.hidden)").length
        : 0;

      var label = scan.querySelector(".badge.count");
      var total = scan.getAttribute("data-total") || "0";

      if (label) {
        if (query || filter !== "all") {
          label.textContent = shown + " / " + total;
        } else {
          label.textContent = total + " findings";
        }
      }
    });

    if (counter) {
      counter.textContent = visible;
    }
  }

  if (search) {
    search.addEventListener("input", apply);
  }

  filters.forEach(function (button) {
    button.addEventListener("click", function () {
      filters.forEach(function (item) {
        item.classList.remove("active");
      });
      button.classList.add("active");
      active = button.getAttribute("data-tag") || "all";
      apply();
    });
  });

  scans.forEach(function (scan) {
    var head = scan.querySelector(".scan-head");
    if (!head) {
      return;
    }
    head.addEventListener("click", function () {
      scan.classList.toggle("collapsed");
    });
  });

  var expand = document.getElementById("expand-all");
  var collapse = document.getElementById("collapse-all");

  if (expand) {
    expand.addEventListener("click", function () {
      scans.forEach(function (scan) {
        scan.classList.remove("collapsed");
      });
    });
  }

  if (collapse) {
    collapse.addEventListener("click", function () {
      scans.forEach(function (scan) {
        scan.classList.add("collapsed");
      });
    });
  }

  var print = document.getElementById("print-report");
  if (print) {
    print.addEventListener("click", function () {
      window.print();
    });
  }

  apply();
})();
"""


class HTMLOutput:
    """Handle AgisRecon2 HTML output."""

    def __init__(
        self,
        output_dir: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize the HTML output handler.

        Args:
            output_dir: Directory where HTML reports
                        will be stored.
        """

        if output_dir is None:
            output_dir = Path("output") / "html"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # Format results
    # ---------------------------------------------------------

    def format_results(
        self,
        results: Any = None,
        target: Optional[str] = None,
        module: Optional[str] = None,
        tool: Optional[str] = None,
        command: Optional[str] = None,
        title: str = "AgisRecon2 Reconnaissance Report",
        scans: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> str:
        """
        Convert reconnaissance results into a standalone HTML report.

        Args:
            results: Results returned by a reconnaissance module.
            target: Target being scanned.
            module: Name of the module that produced the results.
            tool: External tool used by the scan.
            command: Command executed by the scan.
            title: Report title.
            scans: Optional list of scan records used to build a
                   consolidated report covering one or many tools.

        Returns:
            The complete HTML document.
        """

        records = self._build_records(
            results=results,
            target=target,
            module=module,
            tool=tool,
            command=command,
            scans=scans,
        )

        return self._render_page(
            records=records,
            title=title,
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(
        self,
        results: Any = None,
        filename: Optional[str] = None,
        target: Optional[str] = None,
        module: Optional[str] = None,
        tool: Optional[str] = None,
        command: Optional[str] = None,
        title: str = "AgisRecon2 Reconnaissance Report",
        scans: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> Path:
        """
        Save reconnaissance results as an HTML report.

        Returns:
            Path to the generated HTML file.
        """

        content = self.format_results(
            results=results,
            target=target,
            module=module,
            tool=tool,
            command=command,
            title=title,
            scans=scans,
        )

        if filename is None:
            filename = self._generate_filename(
                target=target,
                module=module,
                consolidated=bool(scans),
            )

        if not filename.endswith(".html"):
            filename += ".html"

        file_path = self.output_dir / filename

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return file_path

    # ---------------------------------------------------------
    # Records
    # ---------------------------------------------------------

    def _build_records(
        self,
        results: Any,
        target: Optional[str],
        module: Optional[str],
        tool: Optional[str],
        command: Optional[str],
        scans: Optional[Sequence[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        """
        Build a normalized list of scan records.

        A record holds the tool, module, target, command,
        timestamp, and the collected results.
        """

        records: List[Dict[str, Any]] = []

        if scans:

            for scan in scans:

                if not isinstance(scan, dict):
                    continue

                records.append(
                    {
                        "tool": str(
                            scan.get("tool")
                            or scan.get("module")
                            or "unknown"
                        ),
                        "module": str(
                            scan.get("module")
                            or scan.get("tool")
                            or "unknown"
                        ),
                        "target": scan.get("target"),
                        "command": scan.get("command"),
                        "timestamp": scan.get("timestamp"),
                        "results": scan.get("results"),
                    }
                )

            return records

        records.append(
            {
                "tool": str(tool or module or "unknown"),
                "module": str(module or tool or "unknown"),
                "target": target,
                "command": command,
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "results": results,
            }
        )

        return records

    # ---------------------------------------------------------
    # Page rendering
    # ---------------------------------------------------------

    def _render_page(
        self,
        records: List[Dict[str, Any]],
        title: str,
    ) -> str:
        """
        Render the complete HTML document.
        """

        generated = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        sections: List[str] = []
        tag_counts: Dict[str, int] = {}

        for index, record in enumerate(records):

            section, counts = self._render_scan(
                record=record,
                index=index,
            )

            sections.append(section)

            for tag, count in counts.items():
                tag_counts[tag] = tag_counts.get(tag, 0) + count

        targets = sorted(
            {
                str(record.get("target"))
                for record in records
                if record.get("target")
            }
        )

        tools = sorted(
            {
                str(record.get("tool"))
                for record in records
            }
        )

        total_findings = sum(
            self._count_results(record.get("results"))
            for record in records
        )

        head = [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1">',
            f"<title>{self._safe_text(title)}</title>",
            f"<style>{STYLES}</style>",
            "</head>",
            "<body>",
        ]

        hero = self._render_hero(
            title=title,
            targets=targets,
            tools=tools,
            total_findings=total_findings,
            generated=generated,
        )

        stats = self._render_stats(
            records=records,
            tag_counts=tag_counts,
            total_findings=total_findings,
        )

        toolbar = self._render_toolbar(
            tag_counts=tag_counts,
        )

        summary = self._render_summary(records)

        tail = [
            "<footer>",
            "Generated by AgisRecon2 - "
            "AgisRecon2 Reconnaissance Framework",
            "</footer>",
            f"<script>{SCRIPTS}</script>",
            "</body>",
            "</html>",
        ]

        parts = head
        parts.append(hero)
        parts.append(stats)
        parts.append(toolbar)
        parts.append("<main>")
        parts.append(summary)
        parts.extend(sections)
        parts.append("</main>")
        parts.extend(tail)

        return "\n".join(parts)

    # ---------------------------------------------------------
    # Hero
    # ---------------------------------------------------------

    def _render_hero(
        self,
        title: str,
        targets: List[str],
        tools: List[str],
        total_findings: int,
        generated: str,
    ) -> str:
        """Render the report header."""

        target_text = ", ".join(targets) if targets else "N/A"

        chips = [
            ("Target", target_text),
            ("Tools", str(len(tools))),
            ("Findings", str(total_findings)),
            ("Generated", generated),
        ]

        chips_html = "\n".join(
            (
                f'<span class="chip"><b>{self._safe_text(label)}</b> '
                f"{self._safe_text(value)}</span>"
            )
            for label, value in chips
        )

        return (
            '<header class="hero">\n'
            '<div class="hero-inner">\n'
            '<p class="eyebrow">AgisRecon2 &middot; Reconnaissance Report</p>\n'
            f"<h1>{self._safe_text(title)}</h1>\n"
            f'<div class="meta">\n{chips_html}\n</div>\n'
            "</div>\n"
            "</header>"
        )

    # ---------------------------------------------------------
    # Statistic cards
    # ---------------------------------------------------------

    def _render_stats(
        self,
        records: List[Dict[str, Any]],
        tag_counts: Dict[str, int],
        total_findings: int,
    ) -> str:
        """Render the statistic cards."""

        targets = sorted(
            {
                str(record.get("target"))
                for record in records
                if record.get("target")
            }
        )

        tools = sorted(
            {
                str(record.get("tool"))
                for record in records
            }
        )

        cards: List[tuple[str, str, str]] = [
            ("Targets", str(len(targets)), "accent"),
            ("Tools", str(len(tools)), "accent"),
            ("Scans", str(len(records)), ""),
            ("Findings", str(total_findings), ""),
        ]

        for tag in ("critical", "high", "medium", "low", "info"):
            count = tag_counts.get(tag, 0)
            if count:
                cards.append(
                    (tag.capitalize(), str(count), tag)
                )

        cards_html = "\n".join(
            (
                '<div class="stat">'
                f'<div class="label">{self._safe_text(label)}</div>'
                f'<div class="value {css_class}">{self._safe_text(value)}</div>'
                "</div>"
            )
            for label, value, css_class in cards
        )

        return f'<section class="stats">\n{cards_html}\n</section>'

    # ---------------------------------------------------------
    # Toolbar
    # ---------------------------------------------------------

    def _render_toolbar(
        self,
        tag_counts: Dict[str, int],
    ) -> str:
        """Render the search and filter toolbar."""

        buttons = [
            '<button type="button" class="active" data-tag="all">'
            "All</button>"
        ]

        for tag in ("critical", "high", "medium", "low", "info"):
            count = tag_counts.get(tag, 0)
            if not count:
                continue
            buttons.append(
                f'<button type="button" data-tag="{tag}">'
                f"{tag.capitalize()} ({count})</button>"
            )

        for tag in ("open", "closed", "filtered"):
            count = tag_counts.get(tag, 0)
            if not count:
                continue
            buttons.append(
                f'<button type="button" data-tag="{tag}">'
                f"{tag.capitalize()} ({count})</button>"
            )

        return (
            '<div class="toolbar">\n'
            '<input type="search" id="search" '
            'placeholder="Search across every finding..." '
            'autocomplete="off">\n'
            f'<div class="filters">{"".join(buttons)}</div>\n'
            '<div class="spacer"></div>\n'
            '<div class="actions">\n'
            '<button type="button" id="expand-all">Expand</button>\n'
            '<button type="button" id="collapse-all">Collapse</button>\n'
            '<button type="button" id="print-report">Print</button>\n'
            "</div>\n"
            "</div>"
        )

    # ---------------------------------------------------------
    # Summary table
    # ---------------------------------------------------------

    def _render_summary(
        self,
        records: List[Dict[str, Any]],
    ) -> str:
        """Render the scan summary table."""

        rows = []

        for record in records:

            count = self._count_results(record.get("results"))

            status = (
                "Completed"
                if count
                else "No results"
            )

            rows.append(
                "<tr>"
                f'<td class="tag">'
                f'<span class="badge tool">'
                f"{self._safe_text(record.get('tool'))}</span></td>"
                f"<td>{self._safe_text(record.get('target') or 'N/A')}</td>"
                f'<td class="idx">{count}</td>'
                f"<td>{self._safe_text(record.get('timestamp') or 'N/A')}</td>"
                f"<td><code>"
                f"{self._safe_text(record.get('command') or 'N/A')}"
                "</code></td>"
                f"<td>{status}</td>"
                "</tr>"
            )

        return (
            '<section class="panel">\n'
            "<h2>Scan Summary</h2>\n"
            '<div class="panel-body">\n'
            "<table>\n"
            "<thead><tr>"
            "<th>Tool</th><th>Target</th><th>Findings</th>"
            "<th>Timestamp</th><th>Command</th><th>Status</th>"
            "</tr></thead>\n"
            "<tbody>\n"
            f"{''.join(rows)}\n"
            "</tbody>\n"
            "</table>\n"
            "</div>\n"
            "</section>"
        )

    # ---------------------------------------------------------
    # Scan section
    # ---------------------------------------------------------

    def _render_scan(
        self,
        record: Dict[str, Any],
        index: int,
    ) -> tuple[str, Dict[str, int]]:
        """
        Render a single tool section.

        Returns:
            Tuple containing the section HTML and the tag counts.
        """

        results = record.get("results")

        count = self._count_results(results)

        body, tag_counts = self._render_results(
            results,
        )

        meta_parts = []

        if record.get("target"):
            meta_parts.append(
                f"Target: {self._safe_text(record.get('target'))}"
            )

        if record.get("timestamp"):
            meta_parts.append(
                f"Run: {self._safe_text(record.get('timestamp'))}"
            )

        if record.get("command"):
            meta_parts.append(
                f"Command: {self._safe_text(record.get('command'))}"
            )

        meta_html = " &middot; ".join(meta_parts)

        section = (
            f'<section class="scan" id="scan-{index}" '
            f'data-total="{count}">\n'
            '<header class="scan-head">\n'
            '<div class="scan-title">\n'
            f'<span class="badge tool">'
            f"{self._safe_text(record.get('tool'))}</span>"
            f'<span class="badge count">{count} findings</span>'
            "</div>\n"
            f'<div class="scan-meta">{meta_html}</div>\n'
            '<span class="chevron">&#9662;</span>\n'
            "</header>\n"
            f'<div class="scan-body">\n{body}\n</div>\n'
            "</section>"
        )

        return section, tag_counts

    # ---------------------------------------------------------
    # Results rendering
    # ---------------------------------------------------------

    def _render_results(
        self,
        results: Any,
    ) -> tuple[str, Dict[str, int]]:
        """
        Render the result block of a tool section.

        Returns:
            Tuple containing the HTML and the tag counts.
        """

        tag_counts: Dict[str, int] = {}

        if results is None:
            return (
                '<p class="empty">No results found.</p>',
                tag_counts,
            )

        if isinstance(results, dict):
            html = self._render_mapping(results, tag_counts)

            return html, tag_counts

        if isinstance(results, (list, tuple, set)):
            items = list(results)

            if not items:
                return (
                    '<p class="empty">No results found.</p>',
                    tag_counts,
                )

            if all(
                isinstance(item, dict)
                for item in items
            ):
                html = self._render_records(items, tag_counts)

                return html, tag_counts

            html = self._render_lines(items, tag_counts)

            return html, tag_counts

        text = self._safe_text(results)

        if not text:
            return (
                '<p class="empty">No results found.</p>',
                tag_counts,
            )

        return (
            f'<pre class="raw">{text}</pre>',
            tag_counts,
        )

    # ---------------------------------------------------------
    # List of scalar results
    # ---------------------------------------------------------

    def _render_lines(
        self,
        items: List[Any],
        tag_counts: Dict[str, int],
    ) -> str:
        """Render a list of scalar results as a table."""

        rows = []

        for index, item in enumerate(items, start=1):

            text = self._safe_text(item)

            if not text:
                continue

            tag, badge = self._classify(text)

            if tag:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            rows.append(
                "<tr data-row>"
                f'<td class="idx">{index}</td>'
                f'<td class="tag">{badge}</td>'
                f"<td>{text}</td>"
                "</tr>"
            )

        if not rows:
            return '<p class="empty">No results found.</p>'

        return (
            "<table>\n"
            "<thead><tr>"
            "<th>#</th><th>Type</th><th>Result</th>"
            "</tr></thead>\n"
            "<tbody>\n"
            f"{''.join(rows)}\n"
            "</tbody>\n"
            "</table>"
        )

    # ---------------------------------------------------------
    # List of structured results
    # ---------------------------------------------------------

    def _render_records(
        self,
        items: List[Dict[str, Any]],
        tag_counts: Dict[str, int],
    ) -> str:
        """Render a list of dictionary results as a table."""

        columns: List[str] = []

        for item in items:
            for key in item.keys():
                if key not in columns:
                    columns.append(str(key))

        rows = []

        for index, item in enumerate(items, start=1):

            cells = [
                f'<td class="idx">{index}</td>'
            ]

            for column in columns:

                value = item.get(column)

                text = self._safe_text(value)

                tag, badge = self._classify(text)

                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

                cells.append(
                    f'<td>{badge}{text}</td>'
                )

            rows.append(
                f"<tr data-row>{''.join(cells)}</tr>"
            )

        header = "".join(
            f"<th>{self._safe_text(column)}</th>"
            for column in columns
        )

        return (
            "<table>\n"
            f"<thead><tr><th>#</th>{header}</tr></thead>\n"
            "<tbody>\n"
            f"{''.join(rows)}\n"
            "</tbody>\n"
            "</table>"
        )

    # ---------------------------------------------------------
    # Dictionary results
    # ---------------------------------------------------------

    def _render_mapping(
        self,
        data: Dict[str, Any],
        tag_counts: Dict[str, int],
    ) -> str:
        """Render a dictionary result as a key/value table."""

        if not data:
            return '<p class="empty">No results found.</p>'

        rows = []

        for key, value in data.items():

            label = self._safe_text(key)

            if isinstance(value, dict):
                nested = self._render_mapping(
                    value,
                    tag_counts,
                )
                cell = f'<div class="nested">{nested}</div>'

            elif isinstance(value, (list, tuple, set)):
                items = list(value)

                if items and all(
                    isinstance(item, dict)
                    for item in items
                ):
                    nested = self._render_records(
                        items,
                        tag_counts,
                    )
                    cell = f'<div class="nested">{nested}</div>'

                else:
                    lines = []
                    for item in items:
                        text = self._safe_text(item)
                        tag, badge = self._classify(text)
                        if tag:
                            tag_counts[tag] = (
                                tag_counts.get(tag, 0) + 1
                            )
                        lines.append(
                            f'<div>{badge}{text}</div>'
                        )

                    cell = (
                        f'<div class="nested">'
                        f"{''.join(lines) or '<em>empty</em>'}"
                        "</div>"
                    )

            else:
                text = self._safe_text(value)
                tag, badge = self._classify(text)
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
                cell = f"{badge}{text}"

            rows.append(
                "<tr>"
                f'<td class="key">{label}</td>'
                f"<td>{cell}</td>"
                "</tr>"
            )

        return (
            "<table>\n"
            "<tbody>\n"
            f"{''.join(rows)}\n"
            "</tbody>\n"
            "</table>"
        )

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @staticmethod
    def _classify(text: str) -> tuple[str, str]:
        """
        Classify a result line.

        Returns:
            Tuple containing the filter tag and the badge HTML.
            Both are empty when the line carries no classification.
        """

        if not text:
            return "", ""

        match = SEVERITY_PATTERN.search(text)

        if match:

            severity = match.group(1).lower()

            return (
                severity,
                f'<span class="badge sev-{severity}">'
                f"{severity}</span> ",
            )

        match = PORT_PATTERN.match(text.strip())

        if match:

            state = match.group(3).lower()

            return (
                state,
                f'<span class="badge state-{state}">'
                f"{state}</span> ",
            )

        match = HTTP_STATUS_PATTERN.search(text)

        if match:

            code = match.group(1)

            family = code[0]

            return (
                code,
                f'<span class="badge http-{family}xx">'
                f"{code}</span> ",
            )

        return "", ""

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _safe_text(value: Any) -> str:
        """Convert a value into safe HTML text."""

        if value is None:
            return ""

        text = str(value)

        text = ANSI_ESCAPE_PATTERN.sub("", text)

        return _html.escape(text)

    @staticmethod
    def _count_results(results: Any) -> int:
        """Count the number of results held by a result set."""

        if isinstance(results, dict):
            return len(results)

        if isinstance(results, (list, tuple, set)):
            return len(results)

        if results is None:
            return 0

        return 1

    @staticmethod
    def _generate_filename(
        target: Optional[str] = None,
        module: Optional[str] = None,
        consolidated: bool = False,
    ) -> str:
        """Generate a timestamp-based HTML filename."""

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        target_name = (
            str(target)
            .replace("://", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            if target
            else "target"
        )

        module_name = (
            str(module).replace(" ", "_")
            if module
            else "scan"
        )

        if consolidated:
            module_name = "all"

        return (
            f"{target_name}_"
            f"{module_name}_"
            f"{timestamp}.html"
        )


# -------------------------------------------------------------
# Default HTML output instance
# -------------------------------------------------------------

html_output = HTMLOutput()


# -------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------

def save_html(
    results: Any = None,
    filename: Optional[str] = None,
    target: Optional[str] = None,
    module: Optional[str] = None,
    tool: Optional[str] = None,
    command: Optional[str] = None,
    title: str = "AgisRecon2 Reconnaissance Report",
    scans: Optional[Sequence[Dict[str, Any]]] = None,
) -> Path:
    """Save results as an HTML report."""

    return html_output.save(
        results=results,
        filename=filename,
        target=target,
        module=module,
        tool=tool,
        command=command,
        title=title,
        scans=scans,
    )


def format_html(
    results: Any = None,
    target: Optional[str] = None,
    module: Optional[str] = None,
    tool: Optional[str] = None,
    command: Optional[str] = None,
    title: str = "AgisRecon2 Reconnaissance Report",
    scans: Optional[Sequence[Dict[str, Any]]] = None,
) -> str:
    """Create an HTML report without saving it."""

    return html_output.format_results(
        results=results,
        target=target,
        module=module,
        tool=tool,
        command=command,
        title=title,
        scans=scans,
    )
