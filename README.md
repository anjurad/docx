# md-to-docx

> Convert Markdown files to Word documents using pandoc with custom templates and image support.

## ✨ Features

- 📝 Convert Markdown to professionally formatted Word documents
- 🎨 Custom Word template support
- 🖼️ Automatic image handling with resource path resolution
- ⏱️ Timestamped output files for version control
- 🔍 Comprehensive input validation
- 🧪 Fully tested with pytest

## 📋 Requirements

- **Python 3.9+**
- **[pandoc](https://pandoc.org/)** - Universal document converter
  
  > **Note:** If using the devcontainer, pandoc is pre-installed and ready to use.
  
  ```bash
  # macOS
  brew install pandoc
  
  # Ubuntu/Debian
  sudo apt-get install pandoc
  
  # Windows
  choco install pandoc
  ```
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package installer (recommended)
  
  > **Note:** If using the devcontainer, uv is pre-installed and ready to use.
  
  ```bash
  # Install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd docx

# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
uv pip install -e .
```

## 📖 Usage

### Basic Conversion

```bash
md-to-docx path/to/source.md --template path/to/template.docx
```

### Full Example with Images

```bash
md-to-docx sessions/example/input/source.md \
  --template templates/word/template.docx \
  --resource-path "sessions/example/input/images:docs/images"
```

### Command Options

```bash
md-to-docx --help     # Display help information
md-to-docx --version  # Show version number
```

### Output Location

Converted documents are automatically saved to:
```
<session-directory>/output/<timestamp>.docx
```

For example: `sessions/example/output/20260103135809.docx`

## 🏗️ Project Structure

```
docx/
├── src/md_to_docx/       # Main application code
│   ├── cli.py            # Command-line interface
│   └── __init__.py       # Package initialization
├── sessions/             # Conversion sessions
│   └── example/
│       ├── session.manifest.yml
│       ├── input/        # Source markdown and images
│       └── output/       # Generated Word documents
├── templates/word/       # Word document templates
├── tests/                # Test suite
└── pyproject.toml        # Project configuration
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install with development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_cli.py

# Run with coverage
pytest --cov=src/md_to_docx
```

### Code Quality

```bash
# Type checking with mypy
mypy src/

# Linting with ruff
ruff check src/

# Format code
ruff format src/
```

### Development Dependencies

- `pytest>=8.0.0` - Testing framework
- `mypy>=1.8.0` - Static type checker
- `ruff>=0.1.0` - Fast Python linter and formatter

## 🧪 Testing

The project includes comprehensive tests covering:

- ✅ CLI argument parsing and validation
- ✅ File conversion workflows
- ✅ Error handling and edge cases
- ✅ Input validation (file extensions, paths)
- ✅ Pandoc integration

Run the test suite:
```bash
pytest -v
```

Expected output: `24 passed`

## 📝 Session Manifest

Use a `session.manifest.yml` file to configure conversion settings:

```yaml
source: sessions/example/input/source.md
template: templates/word/template.docx
resource_path: sessions/example/input/images:docs/images
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT

## 🙏 Acknowledgments

Built with:
- [pandoc](https://pandoc.org/) - Universal document converter
- [uv](https://github.com/astral-sh/uv) - Ultra-fast Python package installer
- [pytest](https://pytest.org/) - Testing framework
