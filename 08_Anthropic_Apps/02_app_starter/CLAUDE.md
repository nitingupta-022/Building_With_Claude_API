# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` for environment and dependency management.

```bash
# One-time setup
uv venv
uv pip install -e .

# Start the MCP server (stdio transport via FastMCP)
uv run main.py

# Run the full test suite
uv run pytest

# Run a single test file / class / case
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

There is no separate lint or build step configured.

## Architecture

The package is an **MCP server** built on `FastMCP` (from the `mcp` SDK). The wiring is intentionally thin:

- `main.py` instantiates a single `FastMCP("docs")` server, registers each tool function with `mcp.tool()(fn)`, and calls `mcp.run()`. This is the only place tools become visible to MCP clients — a tool that isn't registered here is dead code.
- `tools/` holds plain Python functions, one logical tool per function. They have no MCP-specific imports; they're decorated externally from `main.py`. This keeps tools independently importable and testable.
- `tests/` exercises the underlying tool functions directly (not through the MCP transport). Binary fixtures live in `tests/fixtures/` and are loaded via paths relative to the test file.

`pyproject.toml` declares the package as `app` and pulls `markitdown[docx,pdf]` for document conversion plus `mcp[cli]==1.8.0` (pinned). `tools/` is a flat top-level package — there is no `src/` layout, so imports are `from tools.math import add`, not `from app.tools...`.

## Defining MCP Tools (project convention)

Every tool follows the same shape. Adhere to it when adding new tools — the LLM client relies on the docstring and `Field` descriptions to decide when and how to call the tool.

**1. Write the function in `tools/<area>.py`.** Use `pydantic.Field` for every parameter description; do not rely on the parameter name alone.

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of what the tool does and how it behaves.

    When to use:
    - Concrete situation 1
    - Concrete situation 2

    Examples:
    >>> my_tool("foo", 3)
    expected_output
    """
    # implementation
```

The docstring must contain, in this order:

- A one-line summary as the first line.
- A detailed explanation of functionality.
- An explicit "when to use" section (and, where it matters, when **not** to use the tool — disambiguates overlapping tools for the model).
- Usage examples with expected input/output.

**2. Register the tool in `main.py`** with `mcp.tool()(my_function)`. Registration is what exposes it; merely defining the function is not enough. Existing example: `mcp.tool()(add)`.

**3. Test the underlying function directly** in `tests/`, not through the MCP server. See `tests/test_document.py` for the pattern — it imports `from tools.document import binary_document_to_markdown` and calls it as a normal function.
