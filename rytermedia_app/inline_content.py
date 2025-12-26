from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import html as html_lib
import re
from pathlib import Path

_SCRIPT_CHILDREN_RE = re.compile(
    r'<script(?P<before>[^>]*)\schildren="(?P<js>[^"]*)"(?:\s(?P<after>[^>]*))?>\s*</script>',
    flags=re.IGNORECASE,
)


def fix_script_children_attributes(doc: str) -> str:
    """
    Convert:
      <script children="console.log(1)"></script>
    Into:
      <script>console.log(1)</script>

    This is required because some build steps can serialize unhead "children"
    as an HTML attribute instead of script contents.
    """

    def repl(m: re.Match[str]) -> str:
        before = (m.group("before") or "").strip()
        after = (m.group("after") or "").strip()

        # HTML-unescape so things like &quot; become real quotes.
        js = html_lib.unescape(m.group("js") or "")

        # Preserve any other attributes, but drop the bogus children="...".
        attrs = " ".join(x for x in [before, after] if x).strip()
        attrs = (" " + attrs) if attrs else ""

        return f"<script{attrs}>{js}</script>"

    return _SCRIPT_CHILDREN_RE.sub(repl, doc)


def patch_html_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    text2 = fix_script_children_attributes(text)
    if text2 != text:
        path.write_text(text2, encoding="utf-8")


def patch_all_html(root: Path) -> None:
    for html_path in root.rglob("*.html"):
        patch_html_file(html_path)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _collect_sql_dumps(public_dir: Path) -> dict[str, str]:
    root = public_dir / "__nuxt_content"
    if not root.exists():
        raise FileNotFoundError(f"Expected {root} to exist (did you run `pnpm generate`?)")

    dumps: dict[str, str] = {}
    for dump_path in sorted(root.rglob("sql_dump.txt")):
        rel = dump_path.relative_to(public_dir).as_posix()
        dumps[rel] = _read_text(dump_path)

    if not dumps:
        raise RuntimeError(f"No sql_dump.txt files found under {root}")

    return dumps


def _make_bootstrap_js(dumps: dict[str, str]) -> str:
    # Build a JS object literal with JSON-escaped keys/values.
    # Keys are paths like "__nuxt_content/blog/sql_dump.txt".
    entries = []
    for k, v in dumps.items():
        entries.append(f"{json.dumps(k)}: {json.dumps(v)}")
    obj = ",\n".join(entries)

    # Fetch shim:
    # - strips query string
    # - strips leading "./" or "/"
    # - matches the embedded key set
    shim = r"""
(function () {
  var map = window.__NUXT_OFFLINE_DUMPS__;
  if (!map) return;

  var origFetch = window.fetch;
  if (typeof origFetch !== "function") return;

  window.fetch = function (input, init) {
    try {
      var url = "";
      if (typeof input === "string") url = input;
      else if (input && typeof input.url === "string") url = input.url;

      // Drop query string
      var q = url.indexOf("?");
      if (q !== -1) url = url.slice(0, q);

      // Drop origin if any (should not exist for file:// cases)
      // Normalize leading "./" or "/"
      if (url.startsWith("./")) url = url.slice(2);
      if (url.startsWith("/")) url = url.slice(1);

      var hit = map[url];
      if (typeof hit === "string") {
        return Promise.resolve(
          new Response(hit, {
            status: 200,
            headers: { "Content-Type": "text/plain; charset=utf-8" }
          })
        );
      }
    } catch (e) {
      // fall through
    }
    return origFetch(input, init);
  };
})();
""".strip("\n")

    return "window.__NUXT_OFFLINE_DUMPS__ = {\n" + obj + "\n};\n" + shim + "\n"


def _strip_crossorigin_attrs(html: str) -> str:
    # In file://, crossorigin on <link>/<script> can trigger CORS failures.
    return re.sub(r"\s+crossorigin(?=[\s>])", "", html)


def _inject_script_tag(html: str, script_src: str) -> str:
    tag = f'<script src="{script_src}"></script>'

    # Prefer to inject before the first module script (so fetch is patched early).
    needle = '<script type="module"'
    idx = html.find(needle)
    if idx != -1:
        return html[:idx] + tag + html[idx:]

    # Fallback: inject before </head>
    head_close = "</head>"
    idx2 = html.lower().find(head_close)
    if idx2 != -1:
        return html[:idx2] + tag + html[idx2:]

    # Last resort: prepend
    return tag + html


def _patch_all_html(public_dir: Path, bootstrap_path: Path) -> None:
    html_files = sorted(public_dir.rglob("*.html"))
    if not html_files:
        raise RuntimeError(f"No .html files found under {public_dir}")

    for html_path in html_files:
        html = _read_text(html_path)

        # Remove crossorigin attributes (helps file:// loads).
        html = _strip_crossorigin_attrs(html)

        # Compute a relative path from this HTML file to the bootstrap file.
        rel = Path(os.path.relpath(bootstrap_path, start=html_path.parent)).as_posix()

        # Inject bootstrap <script>.
        html = _inject_script_tag(html, rel)

        _write_text(html_path, html)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--public-dir",
        type=Path,
        default=Path(".output/public"),
        help="Path to Nuxt static output (default: .output/public)",
    )
    ap.add_argument(
        "--keep-sql-dumps",
        action="store_true",
        help="Keep __nuxt_content/**/sql_dump.txt files (default: delete after embedding)",
    )
    args = ap.parse_args()

    public_dir: Path = args.public_dir
    if not public_dir.exists():
        raise FileNotFoundError(f"{public_dir} does not exist")

    dumps = _collect_sql_dumps(public_dir)

    bootstrap_path = public_dir / "__offline" / "nuxt_content_bootstrap.js"
    _write_text(bootstrap_path, _make_bootstrap_js(dumps))

    _patch_all_html(public_dir, bootstrap_path)

    if not args.keep_sql_dumps:
        # Remove the on-disk dumps so the site no longer relies on file:// fetch.
        for p in (public_dir / "__nuxt_content").rglob("sql_dump.txt"):
            p.unlink(missing_ok=True)

    print(f"Embedded {len(dumps)} sql_dump.txt files into {bootstrap_path}")
    patch_all_html(public_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
