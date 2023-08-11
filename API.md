
### Create new log 
```bash
curl --request POST \
  --url http://localhost:8000/log \
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
  --url http://localhost:8000/log/64d2b96e65330e4fc8415422
```

### Get today's logs with pagination
Without pagination:
```bash
curl --request GET \
  --url http://localhost:8000/logs
```

With:
```bash
curl --request GET \
  --url 'http://localhost:8000/logs?offset=0&limit=100'
```

### Filter today's logs by service or level
```bash
curl --request GET \
  --url 'http://localhost:8000/logs?service=authorisation&level=error'
```