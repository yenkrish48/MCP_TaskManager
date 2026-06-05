# mcp_servers/tasks_server.py
"""
MCP Server: Task Manager
=========================
A simple MCP server that exposes local markdown tasks to AI agents.
Built with FastMCP from the official MCP Python SDK.

Tools Exposed:
  - list_tasks: List all available markdown tasks with metadata
  - read_task: Read the full contents of a specific task
  - search_tasks: Search tasks by keyword across all files

Transport: stdio (launched as subprocess by MCP client)
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# ─── Initialize MCP Server ───────────────────────────────────────────
mcp = FastMCP("TaskManager")

# ─── Configuration ────────────────────────────────────────────────────
# Tasks directory - relative to project root
TASKS_DIR = Path(__file__).parent.parent / "tasks"


# ─── Tool: List Tasks ─────────────────────────────────────────────────
@mcp.tool()
def list_tasks() -> list[dict]:
    """List all available markdown tasks with metadata.

    Returns a list of dictionaries containing:
      - filename: Name of the markdown file
      - size_bytes: File size in bytes
      - last_modified: Last modification timestamp
    """
    tasks = []
    for filepath in sorted(TASKS_DIR.glob("*.md")):
        stat = filepath.stat()
        tasks.append({
            "filename": filepath.name,
            "size_bytes": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })
    return tasks


# ─── Tool: Read Task ──────────────────────────────────────────────────
@mcp.tool()
def read_task(filename: str) -> str:
    """Read the full contents of a specific markdown task.

    Args:
        filename: Name of the markdown file to read (e.g., 'meeting_tasks.md')

    Returns:
        The full text content of the task.

    Raises:
        ValueError: If path traversal is detected
        FileNotFoundError: If the task doesn't exist
    """
    # Security: Prevent path traversal attacks
    safe_path = (TASKS_DIR / filename).resolve()
    if not str(safe_path).startswith(str(TASKS_DIR.resolve())):
        raise ValueError("Access denied: path traversal detected")

    if not safe_path.exists():
        raise FileNotFoundError(f"Task '{filename}' not found")

    if not safe_path.suffix == ".md":
        raise ValueError("Only markdown (.md) files are supported")

    return safe_path.read_text(encoding="utf-8")


# ─── Tool: Search Tasks ───────────────────────────────────────────────
@mcp.tool()
def search_tasks(query: str) -> list[dict]:
    """Search across all tasks for a keyword or phrase.

    Performs case-insensitive search across all markdown files.

    Args:
        query: The search term or phrase to look for

    Returns:
        List of matches with filename and matching line excerpts.
    """
    results = []
    query_lower = query.lower()

    for filepath in sorted(TASKS_DIR.glob("*.md")):
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
        matching_lines = []

        for i, line in enumerate(lines, 1):
            if query_lower in line.lower():
                matching_lines.append({
                    "line_number": i,
                    "text": line.strip(),
                })

        if matching_lines:
            results.append({
                "filename": filepath.name,
                "matches": matching_lines,
                "total_matches": len(matching_lines),
            })

    return results


# ─── Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting Tasks MCP Server...", file=sys.stderr, flush=True)
    mcp.run(transport="stdio")
