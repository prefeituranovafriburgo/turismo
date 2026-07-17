import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turismo.settings')
import django
django.setup()
from django.test import Client
c = Client()
resp = c.get('/gera_senha_pdf/C922/23NF')
print('STATUS', resp.status_code)
html = resp.content.decode('utf-8')
print(html.count('qr_code'))
start = html.find('id="qr_code"')
print(html[start-200:start+400])
