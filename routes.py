import json
import server

def row2dict(row):
	"""Takes sqlite3.Row objects and converts them to dictionaries.
	This is important for JSON serialization because otherwise
	Python has no idea how to turn a sqlite3.Row into JSON."""
	x = {}
	for col in row.keys():
		x[col] = row[col]
	return x


@server.app.route('/v1/device/<device_id>')
def getDevice(device_id):
	c = server.get_db().cursor()
	device = c.execute("SELECT * FROM devices WHERE id=?", [device_id]).fetchone()

	if device is not None:
		result = {"success": True, "data": row2dict(device)}
		return result
	else:
		result = {"success": False, "error": "Device ID {} not found".format(device_id)}
		return result

@server.app.route('/v1/customer/<customer_id>')
def getCustomer(customer_id):
	c = server.get_db().cursor()
	customer = c.execute("SELECT * FROM customers WHERE id=?", [customer_id]).fetchone()

	if customer is not None:
		result = {"success": True, "data": row2dict(customer)}
		return result
	else:
		result = {"success": False, "error": "Customer ID {} not found".format(customer_id)}
		return result

@server.app.route('/v1/device/<device_id>/status', methods=["POST"])
def pushStatus(device_id):
	api_token = server.request.headers.get('X-API-Token')
	auth = checkToken(api_token)
	if not auth["success"]:
		return auth

	content = server.request.json
	if content is None:
		response = {"success": False, "error": "Expected JSON content"}
		return response
	try:
		status = content["status"]
		print(status)
	except KeyError:
		response = {"success": False, "error": "Missing 'device_id', or 'status'"}
		return response
	except ValueError:
		response = {"success": False, "error": "Value of 'status' should be standby/alert/error"}
		return response

	db = server.get_db()
	c = db.cursor()
	try:
		c.execute('UPDATE INTO devices VALUES (null, ?, ?)', [device_id, status])
		db.commit()
	except:
		response = {"success": False, "error": "Unknown SQL error"}
		raise
		return response

	response = {"success": True}
	return response

@server.app.route('/v1/company')
def getCompany():
	api_token = server.request.headers.get('X-API-Token')
	auth = checkToken(api_token)
	if not auth["success"]:
		return auth

	c = server.get_db().cursor()
	company = c.execute("SELECT companies.id, companies.name FROM companies, tokens WHERE companies.id=tokens.recipient_id AND tokens.api_token=?", [api_token]).fetchone()

	if company is not None:
		result = {"success": True, "data": row2dict(company)}
		return result
	else:
		result = {"success": False, "error": "No company was found".format(company)}
		return result

@server.app.route('/v1/devices/alert')
def getAlertingDevices():
	api_token = server.request.headers.get('X-API-Token')
	auth = checkToken(api_token)
	if not auth["success"]:
		return auth

	c = server.get_db().cursor()
	c.execute("SELECT * FROM devices WHERE status=?", ["alert"])
	rows = c.fetchall()
	response = {
		"success": True,
		"devices": []
	}

	for row in rows:
		# x = row2dict(row)
		response["devices"].append(row["id"])
	return response

@server.app.route('/v1/company/devices')
def getCompanyDevices():
	api_token = server.request.headers.get('X-API-Token')
	auth = checkToken(api_token)
	if not auth["success"]:
		return auth

	c = server.get_db().cursor()
	c.execute("SELECT devices.id, devices.version, devices.status FROM devices, tokens WHERE api_token=? AND devices.company_id=tokens.recipient_id", [api_token])
	rows = c.fetchall()
	response = {
		"success": True,
		"devices": []
	}

	for row in rows:
		x = row2dict(row)
		response["devices"].append(x)
	return response

@server.app.route('/token/<token>', methods=['DELETE'])
def deleteToken(token):
	api_token = server.request.headers.get('X-API-Token')
	auth = checkToken(api_token)
	if not auth["success"]:
		return auth

	db = server.get_db()
	c = db.cursor()

	# Crazy logic to say "Delete only if there's at least 1 more token for this company."
	c.execute('DELETE FROM tokens WHERE api_token=?', [token])

	db.commit()
	if c.rowcount > 0:
		result = {"success": True}
	else:
		result = {"success": False, "error": "No such token"}
	return result


def checkToken(api_token):
	c = server.get_db().cursor()
	c.execute("SELECT tokens.api_token FROM tokens WHERE tokens.api_token=?", [api_token])
	authenticatedContext = c.fetchone()
	if authenticatedContext is not None:
		reponse = {"success": True}
	else:
		response = {"success": False, "error": "Invalid API token"}
	return response



@server.app.route('/authenticate', methods=['POST'])
def authenticate():
	content = server.request.json
	try:
		login = content["login"]
		password = content["password"]

		c = server.get_db().cursor()
		if login is not None:
			c.execute("SELECT login FROM customers WHERE login=? AND password=?", [login, password])
			customer = c.fetchone()
			if customer is not None:
				token is md5sum(customer["login"])
				c.execute("INSET INTO tokens VALUES(null, ?, ?)", token, customer["id"])
		response["token"] = {"Token": token}
		return response
	except KeyError:
		response = {"success": False, "error": "Invalid credentials."}
		return response
