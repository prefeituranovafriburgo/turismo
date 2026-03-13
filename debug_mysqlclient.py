#!/usr/bin/env python
import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo.settings')

try:
    import MySQLdb
    print(f"MySQLdb imported from: {MySQLdb.__file__}")
    print(f"MySQLdb.version_info: {MySQLdb.version_info}")
    
    # Check what Django sees
    from django.db import connection
    print(f"Database engine: {connection.settings_dict['ENGINE']}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
