#!/usr/bin/env python3
"""Inspect pyindrav2h module structure without paging."""
import pyindrav2h
import inspect

print("=== Module Info ===")
print(f"File: {pyindrav2h.__file__}")
print(f"Package: {pyindrav2h.__package__}")
print(f"Version: {getattr(pyindrav2h, '__version__', 'N/A')}")

print("\n=== Exported Items ===")
for name in dir(pyindrav2h):
    if not name.startswith('_'):
        obj = getattr(pyindrav2h, name)
        obj_type = type(obj).__name__
        print(f"\n{name}: {obj_type}")
        
        if inspect.isclass(obj):
            methods = [m for m in dir(obj) if not m.startswith('_')]
            print(f"  Methods ({len(methods)}): {', '.join(methods[:10])}")
            if len(methods) > 10:
                print(f"  ... and {len(methods) - 10} more")
        elif inspect.ismodule(obj):
            print(f"  Submodule")
        elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
            sig = inspect.signature(obj) if inspect.isfunction(obj) else None
            print(f"  Function: {sig}")
        elif isinstance(obj, dict):
            print(f"  Dict keys: {list(obj.keys())}")
        else:
            print(f"  Value: {obj}")

print("\n=== V2H_MODES ===")
if hasattr(pyindrav2h, 'V2H_MODES'):
    for key, value in pyindrav2h.V2H_MODES.items():
        print(f"  {key}: {value}")

print("\n=== Available Imports ===")
print("Try importing:")
print("  from pyindrav2h.connection import Connection")
print("  from pyindrav2h.v2hclient import v2hClient")
print("  from pyindrav2h.v2hdevice import v2hDevice")

