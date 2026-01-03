"""Tests for input validation."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from md_to_docx.cli import convert


def create_mock_output(output_path: Path) -> None:
    """Helper to create mock output file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"mock docx content")


class TestInputValidation:
    """Test suite for input validation."""

    def test_source_file_not_found(self, template_file: Path, tmp_path: Path) -> None:
        """Test error when source file doesn't exist."""
        missing_file = tmp_path / "missing.md"
        
        with pytest.raises(FileNotFoundError, match="Source file not found"):
            convert(missing_file, template_file)

    def test_template_file_not_found(self, markdown_file: Path, tmp_path: Path) -> None:
        """Test error when template file doesn't exist."""
        missing_template = tmp_path / "missing.docx"
        
        with pytest.raises(FileNotFoundError, match="Template file not found"):
            convert(markdown_file, missing_template)

    @pytest.mark.parametrize(
        ("filename", "expected_error"),
        [
            ("test.txt", "Source must be a .md file, got: .txt"),
            ("test.doc", "Source must be a .md file, got: .doc"),
            ("test", "Source must be a .md file, got: "),
            ("test.MD", None),  # Should work (case-insensitive)
        ],
        ids=["txt-file", "doc-file", "no-extension", "uppercase-md"],
    )
    def test_source_file_extension(
        self,
        template_file: Path,
        tmp_path: Path,
        filename: str,
        expected_error: str | None,
    ) -> None:
        """Test validation of source file extension."""
        source = tmp_path / filename
        source.write_text("test content")
        
        if expected_error:
            with pytest.raises(ValueError, match=expected_error):
                convert(source, template_file)
        else:
            # Should not raise for .MD (case-insensitive)
            with patch("md_to_docx.cli._check_pandoc"), patch(
                "md_to_docx.cli.subprocess.run"
            ) as mock_run:
                def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
                    output_idx = cmd.index("-o") + 1
                    output_path = Path(cmd[output_idx])
                    create_mock_output(output_path)
                    return MagicMock(returncode=0)
                
                mock_run.side_effect = side_effect
                convert(source, template_file)

    @pytest.mark.parametrize(
        ("filename", "expected_error"),
        [
            ("template.txt", "Template must be a .docx file, got: .txt"),
            ("template.doc", "Template must be a .docx file, got: .doc"),
            ("template", "Template must be a .docx file, got: "),
            ("template.DOCX", None),  # Should work (case-insensitive)
        ],
        ids=["txt-file", "doc-file", "no-extension", "uppercase-docx"],
    )
    def test_template_file_extension(
        self,
        markdown_file: Path,
        tmp_path: Path,
        filename: str,
        expected_error: str | None,
    ) -> None:
        """Test validation of template file extension."""
        template = tmp_path / filename
        template.write_bytes(b"mock content")
        
        if expected_error:
            with pytest.raises(ValueError, match=expected_error):
                convert(markdown_file, template)
        else:
            # Should not raise for .DOCX (case-insensitive)
            with patch("md_to_docx.cli._check_pandoc"), patch(
                "md_to_docx.cli.subprocess.run"
            ) as mock_run:
                def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
                    output_idx = cmd.index("-o") + 1
                    output_path = Path(cmd[output_idx])
                    create_mock_output(output_path)
                    return MagicMock(returncode=0)
                
                mock_run.side_effect = side_effect
                convert(markdown_file, template)

    def test_pandoc_not_installed(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test error when pandoc is not installed."""
        with patch("md_to_docx.cli.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            
            with pytest.raises(FileNotFoundError, match="pandoc not found in PATH"):
                convert(markdown_file, template_file)
