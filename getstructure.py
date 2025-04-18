import os

def walk(path, depth=0, max_depth=3):
    if depth > max_depth: return []
    result = []
    for name in sorted(os.listdir(path)):
        if name in {'venv', '.git', '__pycache__', '.mypy_cache', '.idea'}:
            continue
        full = os.path.join(path, name)
        result.append(('    ' * depth) + name)
        if os.path.isdir(full):
            result += walk(full, depth + 1, max_depth)
    return result

with open("structure.txt", "w") as f:
    f.write('\n'.join(walk('.')))
