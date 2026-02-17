import json
from tools.file_tools import create_file, read_file, append_file, list_files

def execute_tool(tool_name, args):
    if tool_name == "create_file":
        return create_file(args["filename"], args["content"])

    if tool_name == "read_file":
        return read_file(args["filename"])

    if tool_name == "append_file":
        return append_file(args["filename"], args["content"])

    if tool_name == "list_files":
        return list_files()

    return "Unknown tool"

def execute_plan(plan_steps):
    """
    plan_steps = [
        {"tool": "create_file", "args": {"filename": "tasks.txt", "content": "Do AI tasks"}},
        {"tool": "append_file", "args": {"filename": "tasks.txt", "content": "Next step"}}
    ]
    """
    results = []
    for step in plan_steps:
        tool = step.get("tool")
        args = step.get("args", {})
        result = execute_tool(tool, args)
        results.append(result)
    return results
