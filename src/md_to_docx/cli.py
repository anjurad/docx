"""Convert markdown files to Word documents using pandoc."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from md_to_docx import __version__


def _check_pandoc() -> None:
    """Check if pandoc is installed and accessible.

    Raises:
        FileNotFoundError: If pandoc is not found in PATH.
    """
    try:
        subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "pandoc not found in PATH. Install via: brew install pandoc"
        ) from e


def convert(
    source: Path,
    template: Path,
    resource_path: str | None = None,
) -> Path:
    """Convert markdown to Word document using pandoc.

    Args:
        source: Path to source markdown file.
        template: Path to reference template.docx for styling.
        resource_path: Colon-separated paths for images (e.g., "images:docs").

    Returns:
        Path to the generated Word document.

    Raises:
        FileNotFoundError: If pandoc is not installed or input files don't exist.
        ValueError: If input files have incorrect extensions.
        subprocess.CalledProcessError: If pandoc conversion fails.
        RuntimeError: If pandoc finishes but output is missing.
    """
    # Resolve paths for clearer error messages
    source = source.resolve()
    template = template.resolve()

    # Validate inputs
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    if source.suffix.lower() != ".md":
        raise ValueError(f"Source must be a .md file, got: {source.suffix}")
    
    if not template.exists():
        raise FileNotFoundError(f"Template file not found: {template}")
    if template.suffix.lower() != ".docx":
        raise ValueError(f"Template must be a .docx file, got: {template.suffix}")

    _check_pandoc()

    # Auto-derive output path: <session>/output/<timestamp>.docx
    # Assumes structure: sessions/<session>/input/source.md -> sessions/<session>/output/<timestamp>.docx
    session_dir = source.parent.parent if source.parent.name == "input" else source.parent
    output_dir = session_dir / "output"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output = output_dir / f"{timestamp}.docx"

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
    logging.info(f"Converting {source.name} -> {output.name}")
    
    subprocess.run(cmd, capture_output=True, check=True, text=True)

    if not output.exists():
        raise RuntimeError(f"Pandoc completed but output not created: {output}")

    return output


def main() -> int:
    """CLI entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Convert markdown to Word document",
        prog="md_to_docx",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument("source", type=Path, help="Source markdown file")
    parser.add_argument("--template", type=Path, required=True, help="Template .docx")
    parser.add_argument(
        "--resource-path",
        help="Colon-separated paths for images (e.g., images:docs)",
    )

    args = parser.parse_args()

    try:
        output = convert(args.source, args.template, args.resource_path)
        logging.info(f"✓ Created {output}")
        return 0
    except (FileNotFoundError, ValueError) as e:
        logging.error(f"{e}")
        return 1
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else None
        msg = f"Pandoc error (exit {e.returncode})"
        if stderr:
            msg = f"{msg}: {stderr}"
        logging.error(msg)
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

