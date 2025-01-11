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
    
def validate_code_for_imports_only(import_code):
    FORBIDDEN_MODULES = ['os', 'shutil', 'subprocess', 'pickle', 'openpyxl', 'socket', 'ctypes', 'base64',
                               'requests', 'paramiko', 'Crypto', 'BeautifulSoup', 'sys', 'multiprocessing', 'django']
    tree = ast.parse(import_code, mode='exec')
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Module, ast.alias)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in FORBIDDEN_MODULES or any(alias.name.startswith(prefix) for prefix in FORBIDDEN_MODULES):
                        raise ValueError(f"Forbidden module imported: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module in FORBIDDEN_MODULES or any(node.module.startswith(prefix) for prefix in FORBIDDEN_MODULES):
                    raise ValueError(f"Forbidden module imported: {node.module}")
        else:
            raise ValueError(f"Nicht erlaubte Operation gefunden: {type(node).__name__}")
    return True

def validate_labelfunction(code):
    FORBIDDEN_FUNCTIONS = ['exec', 'eval', 'open']

    tree = ast.parse(code, mode='exec')
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError(f"Labelfunction can't contain import statements")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in FORBIDDEN_FUNCTIONS:
                    raise ValueError(f"Forbidden function called: {node.func.id}")

def execute_code_in_safe_env(code):
    secure_globals = {}
    secure_locals = {}
    compiled_code = compile(code, '<string>', 'exec')
    exec(compiled_code, secure_globals, secure_locals)