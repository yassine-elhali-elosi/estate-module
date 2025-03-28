import xmlrpc.client

url = 'http://localhost:8069'
db = 'community-enterprise'
username = 'admin'
password = 'admin'

# 1. Authentification
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
print(common.version())
uid = common.authenticate(db, username, password, {})
print("UID:", uid)

# Call methods in models
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
results_name_search = models.execute_kw(db, uid, password, 'res.partner', 'name_search', ['Agent Elosi'], {'limit': 10})
print("res.partner> name_search(): ", results_name_search)

results_customer_companies = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
print("res.partner> is_company=True: ", results_customer_companies)