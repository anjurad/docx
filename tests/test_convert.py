"""Tests for convert function."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from md_to_docx.cli import convert


def create_mock_output(output_path: Path) -> None:
    """Helper to create mock output file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"mock docx content")


class TestConvert:
    """Test suite for convert function."""

    def test_convert_success(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test successful conversion."""
        with patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
                # Extract output path from command
                output_idx = cmd.index("-o") + 1
                output_path = Path(cmd[output_idx])
                create_mock_output(output_path)
                return MagicMock(returncode=0)
            
            mock_run.side_effect = side_effect
            
            output = convert(markdown_file, template_file)
            
            assert output.exists()
            assert output.suffix == ".docx"
            assert output.parent.name == "output"
            mock_run.assert_called_once()

    def test_convert_with_resource_path(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test conversion with resource path."""
        with patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
                output_idx = cmd.index("-o") + 1
                output_path = Path(cmd[output_idx])
                create_mock_output(output_path)
                return MagicMock(returncode=0)
            
            mock_run.side_effect = side_effect
            
            output = convert(markdown_file, template_file, "images:docs")
            
            assert output.exists()
            # Verify resource-path was passed to pandoc
            call_args = mock_run.call_args[0][0]
            assert "--resource-path" in call_args
            assert "images:docs" in call_args

    def test_convert_creates_output_directory(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test that output directory is created if missing."""
        # Remove output directory
        output_dir = markdown_file.parent.parent / "output"
        output_dir.rmdir()
        assert not output_dir.exists()
        
        with patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            def side_effect(cmd: list[str], **kwargs: object) -> MagicMock:
                output_idx = cmd.index("-o") + 1
                output_path = Path(cmd[output_idx])
                create_mock_output(output_path)
                return MagicMock(returncode=0)
            
            mock_run.side_effect = side_effect
            
            output = convert(markdown_file, template_file)
            
            assert output_dir.exists()

    def test_convert_pandoc_failure(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test handling of pandoc conversion failure."""
        with patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["pandoc"], stderr="Pandoc error message"
            )
            
            with pytest.raises(subprocess.CalledProcessError):
                convert(markdown_file, template_file)

    def test_convert_output_not_created(
        self,
        markdown_file: Path,
        template_file: Path,
    ) -> None:
        """Test error when pandoc completes but output doesn't exist."""
        with patch("md_to_docx.cli._check_pandoc"), patch(
            "md_to_docx.cli.subprocess.run"
        ) as mock_run:
            # Don't create output file - just return success
            mock_run.return_value = MagicMock(returncode=0)
            
            with pytest.raises(RuntimeError, match="output not created"):
                convert(markdown_file, template_file)
