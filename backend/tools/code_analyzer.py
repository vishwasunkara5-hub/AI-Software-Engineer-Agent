import ast


def analyze_python_code(code: str) -> dict:

    result = {
        "valid_syntax": True,
        "issues": [],
        "functions": [],
        "classes": [],
        "lines": len(code.splitlines())
    }

    try:
        tree = ast.parse(code)

    except SyntaxError as error:
        result["valid_syntax"] = False

        result["issues"].append({
            "type": "SyntaxError",
            "message": error.msg,
            "line": error.lineno
        })

        return result

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)

        elif isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)

    if len(code.splitlines()) > 300:
        result["issues"].append({
            "type": "CodeQuality",
            "message": "File has more than 300 lines.",
            "line": None
        })

    return result