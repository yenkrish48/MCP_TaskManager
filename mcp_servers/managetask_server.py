# mcp_servers/managetask_server.py
"""
MCP Server: Smart Task Manager
==============================
An MCP server that exposes task management operations to AI agents.
Demonstrates task manipulation capabilities alongside the Tasks server.

Tools Exposed:
  - add: Adding the task to the list of tasks
  - update: Updating an existing task
  - delete: Deleting a task
  - list_tasks: Listing all tasks

Transport: stdio
"""

import sys
from mcp.server.fastmcp import FastMCP

# ─── Initialize MCP Server ───────────────────────────────────────────
mcp = FastMCP("TaskManager")


# ─── Tool: Add ────────────────────────────────────────────────────────
@mcp.tool()
def add_task(task: str) -> str:
    """Add a new task to the list.

    Args:
        task: The task description

    Returns:
        Confirmation message.
    """
    # Implementation for adding a task would go here
    return f"Task added: {task}"


# ─── Tool: Update ────────────────────────────────────────────────────
@mcp.tool()
def update_task(task_id: str, new_description: str) -> str:
    """Update an existing task.

    Args:
        task_id: The ID of the task to update
        new_description: The new description for the task

    Returns:
        Confirmation message.
    """
    # Implementation for updating a task would go here
    return f"Task updated: {task_id} -> {new_description}"


# ─── Tool: Delete ────────────────────────────────────────────────────
@mcp.tool()
def delete_task(task_id: str) -> str:
    """Delete a task.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Confirmation message.
    """
    # Implementation for deleting a task would go here
    return f"Task deleted: {task_id}"


# ─── Tool: List Tasks ────────────────────────────────────────────────
@mcp.tool()
def list_tasks() -> list[str]:
    """List all tasks.

    Returns:
        A list of all tasks.
    """
    # Implementation for listing tasks would go here
    return ["Task 1", "Task 2", "Task 3"]



# ─── Entry Point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting Task Manager MCP Server...", file=sys.stderr, flush=True)
    mcp.run(transport="stdio")
