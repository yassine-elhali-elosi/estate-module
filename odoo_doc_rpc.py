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

results_customer_companies_with_offset = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {"offset": 5, "limit": 5})
print("res.partner> is_company=True, offset=10: ", results_customer_companies_with_offset)

results_customer_companies_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
print("res.partner> is_company=True, count: ", results_customer_companies_count)

results_customer_companies_records = models.execute_kw(db, uid, password, 'res.partner', 'read', [results_customer_companies])
print("res.partner> is_company=True, number of records: ", len(results_customer_companies_records))

results_customer_companies_records_specific_fields = models.execute_kw(db, uid, password, 'res.partner', 'read', [results_customer_companies], {"fields": ["name", "country_id", "comment"]})
print("res.partner> is_company=True, records(name, country_id, comment): ", results_customer_companies_records_specific_fields)
