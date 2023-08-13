## Nonsecure API
### Create new log 
```bash
curl --request POST \
  --url http://localhost:8000/api/u/log \
  --header 'Content-Type: application/json' \
  --data '{
	"service": "authorisation",
	"level": "error",
	"payload": {
		"message": "root user created"
	}
}'
```

### Get log by id
```bash
curl --request GET \
  --url http://localhost:8000/api/u/log/64d2b96e65330e4fc8415422
```

### Get today's logs with pagination
Without pagination:
```bash
curl --request GET \
  --url http://localhost:8000/api/u/logs
```

With:
```bash
curl --request GET \
  --url 'http://localhost:8000/api/u/logs?offset=0&limit=100'
```

### Filter today's logs by service or level
```bash
curl --request GET \
  --url 'http://localhost:8000/api/u/logs?service=authorisation&level=error'
```
## Secured API
Secured API pretty same as nonsecure, but with `Authorisation` header and some permissions.
Get log by id and today's logs same as nonsecure.
### Create new log 
When creating new log you need to encrypt data with public key and send it in `payload` field, service name is used from `JWT` token.

```bash
curl --request POST \
  --url http://localhost:8000/api/s/log \
  --header 'Authorisation: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE2OTQ1NTUwMTQuMzg3ODc5LCJzZXJ2aWNlX25hbWUiOiJiYW5raW5nIiwiYWNjZXNzIjoxLCJhY2Nlc3NfY29kZSI6NzY3MzY4NX0.abe0mcMfg6hsLqarm66OMj7rTioXikhr6qmr3jIrlbQ' \
  --header 'Content-Type: application/json' \
  --data '{
	"level": "error",
	"payload": "EfIe6NVFw9Jmi/pRLqtuhBGH0+Oa6OxD0mqziLRZN64xwsmwGUnQn4PXy1lBZsFcrw4XjfLT3D/7D2xBzxfapdk9qzwtbFIff4tfJr6US8lDZFlukTf6CvH5bxdS/UveNv9H5fHKlaeZeZ/arR12M9+yoZKC7zsU7knhPXSBqkezc86dqEWYq36X1bQ+qi3k0akM6CW6N9kZY5/SUsNTYVd3N0i0BMXvER36Cqupnqltsv1qvV5VsjxelM25JhsYEM7aVi0RE1Cyo6/inXUcXtvqinPNoWOur0UPXyATc+n+yopLngQzbQiECQHgISsdiMXuBV3xgRwjwI/LGUfRWw=="
}'
```


## Keys API
### Get public key
```bash
curl --request GET \
  --url http://localhost:8000/api/rsa/publicKey
```
### Validate key
```bash
curl --request POST \
  --url http://localhost:8000/api/rsa/validateKey \
  --header 'Content-Type: application/json' \
  --data '{
	"key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlaD7oI2/BR6xgn1IiqOG\nCHzCT6sYooXp805E2Z6SYyX+6iUxpykB+KKzUHZmEmSx4xly00CCy2hjxeFFSXkm\nrhoQhpqz4RLPH62DC6gpPRSSp1DHt3boJK4lXyjv09sbYrHCOVQD7P/jg5VHHsmN\n0EGSJ9zpKyJxfaK3xc83De+9V4PwCqNQIrGozh8blA5t/qnpXSftX7VOCOpdtziE\nufmKpFNX1kfwKBMsCVVicCAODVUiqfK1yRetDcHluCiR5wzXQSaQxaTWGVwQIFJ6\nb7nK8C1TniNWM+P9cfGeaGJbfJITUfMhZxUQzKtQw4V26vS2BNkP0xIKTbteMxBN\niwIDAQAB\n-----END PUBLIC KEY-----\n"
}'
```

## User API
### Authorisation
Credentials for root user are stored in `.env` file.  
In feature it will be possible to create new users with `POST` request to `/api/user/` endpoint with permissions management.
```bash
curl --request POST \
  --url http://localhost:8000/api/user/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "denver",
	"password": "code"
}'
```

### Add new Service
```bash
curl --request POST \
  --url http://localhost:8000/api/user/addService \
  --header 'Authorisation: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE2OTQzNzE3MzYuNTYyNzksInVzZXJuYW1lIjoiZGVudmVyIiwiYWNjZXNzIjo2NjZ9.yxSL98TFHviu4uakJV9150aHvQPN4FA8JsEqb7Gxmwo' \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "banking",
	"description": "Economy transactions",
	"access": 1
}'
```