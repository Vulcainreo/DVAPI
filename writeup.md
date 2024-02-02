
# Get specific device
curl http://localhost:5000/v1/device/1


# Get specific customer
curl http://localhost:5000/v1/customer/1


# Push status to a specific device
curl -H "X-API-Token: vfuzd2nvaweojqolm4kq" -H "Content-Type: application/hal+json"  -X POST http://localhost:5000/v1/device/1/status -d '{"status":"alert"}'

# Get information on specific company
curl -H "X-API-Token: 7eojwd75kqd80m4sm169" http://localhost:5000/v1/company
{"data":{"id":2,"name":"Martin's health corp"},"success":true}


# Get all devices in alerting status
curl -H "X-API-Token: 7eojwd75kqd80m4sm169" http://localhost:5000/v1/devices/alert
{"devices":[2],"success":true}

# Get all devices related to a company
curl -H "X-API-Token: 7eojwd75kqd80m4sm169" http://localhost:5000/v1/company/devices
{"devices":[{"id":1,"status":"standby","version":100}],"success":true}


# Device authentication to get token
curl -H "Content-Type: application/hal+json"  -X POST http://localhost:5000/authenticate -d '{"login":"smiller", "password":"smiller"}'
