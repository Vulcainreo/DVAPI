# DVAPI
## Objectives
Damn Vulnerable API is a platform designed to :
* Help understanding well-known API vulnerabilities and exploitation
* Help to evaluate WAF (Web Application Firewall) protection efficiency
* Help to evaluate discovery efficiency of attacker tools

## Get started
```bash
docker build -t api .
```

```bash
docker run -it -d -p 5000:5000 api
or
docker-compose up -d
```

## Documentations
### API routes
* GET /v1/device/<device_id> 			use to get all info of the device
* POST /v1/device/<device_id>/status	use to push status on a specific device
* GET /v1/devices/alert					use to get all alert
* GET /v1/customer/<customer_id>		use to get specific custom data
* GET /v1/company/<company_id>/devices	use to list all devics from a company

### Vulnerabilities
#### device_id / company_id are predictable
Description of the vulnerability

#### Unauthenticated inforamtion leakage related to customer
/v1/customer/<customer_id>'

#### Token can be crafted md5(login)
Description of the vulnerability

#### SQL injection in login endpoint
Description of the vulnerability

#### Password are stored in clear text
Passwords are stored in clear text
