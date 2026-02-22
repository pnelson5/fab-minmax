# Development Notes

## Python Package Management

Use `uv` instead of pip for all Python operations:

```bash
# Install dependencies
uv pip install -e .

# Run scripts
uv run python script.py

# Run tests
uv run pytest tests/
```

## Running the Project

- Use `uv run` prefix for all Python commands
- See `pyproject.toml` for dependencies
