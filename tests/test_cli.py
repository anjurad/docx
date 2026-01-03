"""Tests for CLI entry point."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from md_to_docx.cli import main


class TestCLI:
    """Test suite for CLI entry point."""

    def test_cli_version(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test --version flag."""
        with patch.object(sys, "argv", ["md-to-docx", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            assert "1.0.0" in captured.out

    def test_cli_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test --help flag."""
        with patch.object(sys, "argv", ["md-to-docx", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            assert "Convert markdown to Word document" in captured.out

    def test_cli_missing_template(self, markdown_file: Path) -> None:
        """Test error when template argument is missing."""
        with patch.object(
            sys, "argv", ["md-to-docx", str(markdown_file)]
        ), pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2  # argparse error

    def test_cli_success(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test successful CLI execution."""
        with patch.object(
            sys,
            "argv",
            [
                "md-to-docx",
                str(markdown_file),
                "--template",
                str(template_file),
            ],
        ), patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
                output_idx = cmd.index("-o") + 1
                output_path = Path(cmd[output_idx])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(b"mock")
                return MagicMock(returncode=0)
            
            mock_run.side_effect = side_effect
            result = main()
            
            assert result == 0

    def test_cli_with_resource_path(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test CLI with resource-path argument."""
        with patch.object(
            sys,
            "argv",
            [
                "md-to-docx",
                str(markdown_file),
                "--template",
                str(template_file),
                "--resource-path",
                "images:docs",
            ],
        ), patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            main()
            
            call_args = mock_run.call_args[0][0]
            assert "--resource-path" in call_args
            assert "images:docs" in call_args

    def test_cli_file_not_found(
        self,
        template_file: Path,
        tmp_path: Path,
    ) -> None:
        """Test CLI error handling for missing file."""
        missing_file = tmp_path / "missing.md"
        
        with patch.object(
            sys,
            "argv",
            [
                "md-to-docx",
                str(missing_file),
                "--template",
                str(template_file),
            ],
        ):
            result = main()
            
            assert result == 1

    def test_cli_invalid_extension(
        self,
        template_file: Path,
        tmp_path: Path,
    ) -> None:
        """Test CLI error handling for invalid file extension."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("test")
        
        with patch.object(
            sys,
            "argv",
            [
                "md-to-docx",
                str(txt_file),
                "--template",
                str(template_file),
            ],
        ):
            result = main()
            
            assert result == 1

    def test_cli_pandoc_error(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test CLI error handling for pandoc failure."""
        with patch.object(
            sys,
            "argv",
            [
                "md-to-docx",
                str(markdown_file),
                "--template",
                str(template_file),
            ],
        ), patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            from subprocess import CalledProcessError
            
            mock_run.side_effect = CalledProcessError(1, ["pandoc"])
            result = main()
            
            assert result == 1
