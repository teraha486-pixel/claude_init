import importlib
import pathlib
import sys

def import_all_modules_from(package_name: str):
    base_path = pathlib.Path(__file__).resolve().parent.parent / package_name
    for path in base_path.rglob("*.py"):
        if path.name == "__init__.py":
            continue
        module_path = path.with_suffix("").relative_to(pathlib.Path(__file__).resolve().parent.parent)
        module_name = ".".join(module_path.parts)
        importlib.import_module(module_name)