# Relock Identity Firewall

**Relock Firewall** is a HTTP based application uses the Relock Server cryptographic keys roattion mechanism to verificate user browser identity. 

---

## Install dependencies

```pip install -r requirements.txt```
Or use the pyproject.toml:
```pip install .```

## Configuration
The Relock Mmiddleware uses environment variables to configure its runtime behavior. You can provide them via a .env file or pass them in directly when running the container.

### Required variables
| Variable |  Default  | Description |
|:-----|:--------:|------:|
| ```RELOCK_SDK_HOST```   | localhost | Host/IP of the TCP SDK |
| ```RELOCK_SDK_PORT```   |  8111     | Port used to connect to SDK |
| ```RELOCK_LOG_LEVEL```   | INFO |    Logging level (DEBUG, etc.) |
| ```RELOCK_SDK_TIMEOUT```  | 30.0 |    TCP socket timeout (seconds)|

Example .env:
```
RELOCK_SDK_HOST=172.17.0.5
RELOCK_SDK_PORT=8111
RELOCK_LOG_LEVEL=DEBUG
RELOCK_SDK_TIMEOUT=30
```

### Docker
Build the image:
```docker build -t relock-mw .```

Run the container:
```
docker run --rm --name relock-middleware \
  -p 8080:8080 \
  -e RELOCK_SDK_HOST=172.17.0.5 \
  -e RELOCK_SDK_PORT=8111 \
  -e RELOCK_LOG_LEVEL=DEBUG \
  -e RELOCK_SDK_TIMEOUT=30 \
  relock-mw
```

### Testing
Run all endpoint tests using:
```pytest tests/```
Each test sends a POST request with minimal payload to all exposed endpoints.

### Project Structure
```
.
├── app/
│   ├── core/           # TCP client, logger, settings
│   ├── routes/         # FastAPI endpoints
│   ├── schemas/        # Pydantic models for requests/responses
│   ├── services/       # Core logic: RelockService
│   └── main.py         # Entry point
├── tests/              # Test suite
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── README.md
```

### API Endpoints
All endpoints are available under the /device prefix.

```
curl -X POST http://localhost:8080/device/members \
  -H 'Content-Type: application/json' \
  -d '{"route": "members"}'
```

Expected response:
```
{
  "status": true,
  "payload": { ... },
  "error": null
}
```