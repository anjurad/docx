"""Test fixtures for md-to-docx tests."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_session_dir(tmp_path: Path) -> Path:
    """Create a temporary session directory structure.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        Path to session directory with input/output folders.
    """
    session = tmp_path / "test-session"
    (session / "input").mkdir(parents=True)
    (session / "output").mkdir(parents=True)
    return session


@pytest.fixture
def markdown_file(temp_session_dir: Path) -> Path:
    """Create a test markdown file.

    Args:
        temp_session_dir: Session directory fixture.

    Returns:
        Path to created markdown file.
    """
    md_file = temp_session_dir / "input" / "test.md"
    md_file.write_text("# Test Document\n\nThis is a test.\n")
    return md_file


@pytest.fixture
def template_file(tmp_path: Path) -> Path:
    """Create a mock template file.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        Path to mock template.docx file.
    """
    template = tmp_path / "template.docx"
    template.write_bytes(b"mock docx content")
    return template


@pytest.fixture
def images_dir(temp_session_dir: Path) -> Path:
    """Create images directory.

    Args:
        temp_session_dir: Session directory fixture.

    Returns:
        Path to images directory.
    """
    images = temp_session_dir / "input" / "images"
    images.mkdir(parents=True)
    return images
