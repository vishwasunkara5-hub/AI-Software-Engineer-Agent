import ast


def analyze_python_code(code: str):
    results = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                results.append({
                    "type": "function",
                    "name": node.name,
                    "line": node.lineno
                })

            elif isinstance(node, ast.ClassDef):
                results.append({
                    "type": "class",
                    "name": node.name,
                    "line": node.lineno
                })

        return {
            "status": "success",
            "items": results
        }

    except SyntaxError as error:
        return {
            "status": "error",
            "message": str(error)
        }