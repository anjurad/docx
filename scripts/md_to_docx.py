"""Convert markdown files to Word documents using pandoc."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def convert(
    source: Path,
    output: Path,
    template: Path,
    resource_path: str | None = None,
) -> None:
    """Convert markdown to Word document using pandoc.

    Args:
        source: Path to source markdown file.
        output: Path where Word document will be created.
        template: Path to reference template.docx for styling.
        resource_path: Colon-separated paths for images (e.g., "images:docs").

    Raises:
        FileNotFoundError: If pandoc is not installed or input files don't exist.
        subprocess.CalledProcessError: If pandoc conversion fails.
    """
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    if not template.exists():
        raise FileNotFoundError(f"Template file not found: {template}")

    # Check pandoc is available
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        raise FileNotFoundError("pandoc not found. Install via: brew install pandoc")

    # Build pandoc command
    cmd = [
        "pandoc",
        str(source),
        "-o",
        str(output),
        "--reference-doc",
        str(template),
    ]
    if resource_path:
        cmd.extend(["--resource-path", resource_path])

    # Run conversion
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)

    if not output.exists():
        raise RuntimeError(f"Pandoc completed but output not created: {output}")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Convert markdown to Word document")
    parser.add_argument("source", type=Path, help="Source markdown file")
    parser.add_argument("output", type=Path, help="Output .docx file")
    parser.add_argument("--template", type=Path, required=True, help="Template .docx")
    parser.add_argument(
        "--resource-path",
        help="Colon-separated paths for images (e.g., images:docs)",
    )

    args = parser.parse_args()

    try:
        convert(args.source, args.output, args.template, args.resource_path)
        print(f"✓ Created {args.output}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
