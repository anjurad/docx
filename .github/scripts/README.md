Render helper scripts

Usage

1. Run the render helper (requires `pandoc`):

```bash
# from repo root
.github/scripts/render.sh example
```

By default the script renders `sessions/<session>/source.md` to `out/<session>-output.docx` using `templates/word/template.docx`. After a successful render it attempts to update the session manifest at `sessions/<session>/session.manifest.yml` and append a history entry.

Notes

- The manifest updater uses PyYAML if installed; if not available it falls back to a conservative text edit.
- You can customize the output path by modifying the script.
