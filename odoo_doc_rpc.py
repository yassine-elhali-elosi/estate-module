import xmlrpc.client

info = xmlrpc.client.ServerProxy("http://demo.odoo.com/start").start()
url, db, username, password = info["host"], info["database"], info["user"], info["password"]

print(url, db, username, password)