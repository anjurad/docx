# md-to-docx

> Convert Markdown files to Word documents using pandoc with custom templates and image support.

## ✨ Features

- 📝 Convert Markdown to professionally formatted Word documents via pandoc
- 🎨 Custom Word template support with `--reference-doc`
- 🖼️ Automatic image handling with flexible resource path resolution
- ⏱️ Auto-generated timestamped output files (no output path required)
- 📁 Smart output directory creation (auto-derived from session structure)
- 🔍 Comprehensive input validation (file existence, extensions, pandoc availability)
- 🧪 Fully tested with pytest (18 tests covering CLI, conversion, and validation)

## 📋 Requirements

### Dev Container (Automatic)

If using the dev container, **everything is pre-installed** - skip to [Dev Container section](#-dev-container-recommended).

### Local Setup (Manual)

- **Python 3.9+** (Python 3.14 used in dev container)
- **[pandoc](https://pandoc.org/)** - Universal document converter
  
  ```bash
  # macOS
  brew install pandoc
  
  # Ubuntu/Debian
  sudo apt-get install pandoc
  
  # Windows
  choco install pandoc
  ```

- **[uv](https://github.com/astral-sh/uv)** - Fast Python package installer (recommended)
  
  ```bash
  # Install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## � Dev Container (Recommended)

This project includes a fully configured dev container that automatically sets up your development environment.

### What's Pre-Installed

When you open this project in a dev container (VS Code + Docker), the following are **automatically configured**:

- ✅ **Python 3.14** (Debian Trixie base image)
- ✅ **pandoc** (via devcontainer feature)
- ✅ **uv** (fast Python package installer via devcontainer feature)
- ✅ **Virtual environment** (`.venv` created automatically)
- ✅ **Project dependencies** (installed via `postCreateCommand`)
- ✅ **Python interpreter** (pre-configured in VS Code settings)

### Getting Started with Dev Container

1. **Install Prerequisites:**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in Container:**
   ```bash
   # Clone and open
   git clone <repo-url>
   cd docx
   code .
   ```
   - VS Code will prompt: "Reopen in Container" → Click it
   - Wait for container to build and initialize (~2-3 minutes first time)

3. **Start Working:**
   ```bash
   # Everything is ready! Just run:
   md-to-docx --version
   pytest -v
   ```

### What Happens Automatically

The `postCreateCommand` in `.devcontainer/devcontainer.json` runs:
```bash
if [ ! -d .venv ]; then uv venv; fi
uv pip install -e ".[dev]"
```

This ensures:
- Virtual environment exists
- Package is installed in editable mode
- All dev dependencies are available (pytest, mypy, ruff)

## 🚀 Quick Start (Local Setup)

If you prefer **not** to use the dev container, follow these steps:

```bash
# Clone the repository
git clone <repo-url>
cd docx

# Install pandoc (see Requirements section above)
# Install uv (see Requirements section above)

# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
uv pip install -e ".[dev]"
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

### Error Handling

The CLI provides clear error messages for common issues:
- ❌ Missing or invalid file paths
- ❌ Incorrect file extensions (`.md` required for source, `.docx` for template)
- ❌ Pandoc not installed or not in PATH
- ❌ Pandoc conversion errors with stderr output

### Output Location

Output files are **automatically generated** with timestamped names - no need to specify an output path!

**Auto-derivation logic:**
- If your markdown is at `sessions/example/input/source.md`
- Output will be `sessions/example/output/<timestamp>.docx`
- The output directory is created automatically if it doesn't exist

**Example:**
```bash
md-to-docx sessions/example/input/source.md --template templates/word/template.docx
# Creates: sessions/example/output/20260103135809.docx
```

**Note:** If your markdown is not in an `input/` subdirectory, the output directory will be created as a sibling to the source file.

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

**Dev Container:** Already configured! Dev dependencies are installed automatically.

**Local Setup:**
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

Expected output: `18 passed` covering:
- 8 CLI tests (version, help, arguments, error handling)
- 5 conversion tests (success paths, resource paths, output creation)
- 5 validation tests (file existence, extensions, pandoc availability)

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
