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
print("\nres.partner> created record: ", created_record)



updated_record = models.execute_kw(db, uid, password, "res.partner", "write", [[created_record], {"name": "Newer Partner"}])
print("\nres.partner> update created record: ", updated_record)


deleted_record = models.execute_kw(db, uid, password, "res.partner", "unlink", [[created_record]])
print("\nres.partner> delete created record: ", deleted_record)



# Create models
try:
    created_model1 = models.execute_kw(db, uid, password, "ir.model", "create", [{
        "name": "Custom Model",
        "model": "x_custom_model",
        "state": "manual"
    }])
    print("\nir.model> create: ", created_model1)
except Exception:
    print("\nx_custom_model model already exists.")

created_model1_fields = models.execute_kw(db, uid, password, 'x_custom_model', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
print("\nx_custom_model> fields: ", created_model1_fields)


try:
    created_model2 = models.execute_kw(db, uid, password, "ir.model", "create", [{
        "name": "Custom Model",
        "model": "x_custom",
        "state": "manual"
    }])
    print("\nir.model> create: ", created_model1)

    created_model2_fields = models.execute_kw(db, uid, password, "ir.model.fields", "create", [{
        "model_id": created_model2,
        "name": "x_name",
        "ttype": "char",
        "state": "manual",
        "required": True
    }])
    print("\nir.model.fields> create: ", created_model2_fields)
    record_id = models.execute_kw(db, uid, password, 'x_custom', 'create', [{'x_name': "test record"}])
    models.execute_kw(db, uid, password, 'x_custom', 'read', [[record_id]])
except Exception:
    print("\nx_custom model already exists.")