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

results_search = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
print("\nres.partner> is_company=True: ", results_search)

results_search_offset_limit = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {"offset": 5, "limit": 5})
print("\nres.partner> is_company=True, offset=10: ", results_search_offset_limit)

results_search_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
print("\nres.partner> is_company=True, count: ", results_search_count)

results_read = models.execute_kw(db, uid, password, 'res.partner', 'read', [results_search])
print("\nres.partner> is_company=True, number of records: ", len(results_read))

results_read_with_fields = models.execute_kw(db, uid, password, 'res.partner', 'read', [results_search], {"fields": ["name", "country_id", "comment"]})
print("\nres.partner> is_company=True, records(name, country_id, comment): ", results_read_with_fields)

results_fields_get = models.execute_kw(db, uid, password, "res.partner", "fields_get", [], {"attributes": ["string", "help", "type"]})
print("\nres.partner> fields: ", results_fields_get)

results_search_read = models.execute_kw(db, uid, password, "res.partner", "search_read", [[["is_company", "=", True]]], {"fields": ["name", "country_id", "comment"], "limit": 5})
print("\nres.partner> is_company=True, records(name, country_id, comment): ", results_search_read)


created_record = models.execute_kw(db, uid, password, "res.partner", "create", [{"name": "New Partner"}])
print("res.partner> created record: ", created_record)



updated_record = models.execute_kw(db, uid, password, "res.partner", "write", [[created_record], {"name": "Newer Partner"}])
print("res.partner> update created record: ", updated_record)


deleted_record = models.execute_kw(db, uid, password, "res.partner", "unlink", [[created_record]])
print("res.partner> delete created record: ", deleted_record)