#!/usr/bin/env python
import sys
import os

# Ensure we're using venv
print("Python executable:", sys.executable)
print("Sys.path:")
for p in sys.path[:5]:
    print("  ", p)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo.settings')

print("\nImporting MySQLdb...")
import MySQLdb
print(f"MySQLdb file: {MySQLdb.__file__}")
print(f"MySQLdb.__version__: {MySQLdb.__version__}")
print(f"MySQLdb.version_info: {MySQLdb.version_info}")

print("\nImporting Django...")
import django
django.setup()
print("Django setup successful!")
