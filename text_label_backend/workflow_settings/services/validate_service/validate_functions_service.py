import ast
from RestrictedPython import compile_restricted, safe_globals

def validate_variable_assignments(code):
    tree = ast.parse(code, mode='exec')
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.Assign, ast.Name, ast.Constant, ast.Load, ast.Store, ast.UnaryOp, ast.USub)):
            raise ValueError(f"You only have permission to assign variables: {type(node).__name__}")
    return True

def compile_variable_assignments(code):
    compile_restricted(code, '<string>', 'exec')