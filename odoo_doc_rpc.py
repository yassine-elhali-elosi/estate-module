import xmlrpc.client

url = 'http://localhost:8069'
db = 'community-enterprise'
username = 'admin'
password = 'admin'

# 1. Authentification
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
print("UID:", uid)