# Relock Identity Firewall

**Relock Firewall** is an mini HTTP-based application that leverages the Relock Server’s cryptographic key rotation mechanism to verify the identity of the user's browser. This ensures that each request is authenticated securely and passively, without relying on shared secrets or interrupting the user experience."

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
| ```RELOCK_SERVICE_HOST```   | 127.0.0.1 | Host/IP of the TCP Server |
| ```RELOCK_SERVICE_API```   |  | Host/IP of the TCP Server |
| ```RELOCK_SERVICE_PORT```   | 8111 | Port used to connect to SDK |
| ```RELOCK_SERVICE_POOL```   | 3 | Number of socket connections by server |
| ```RELOCK_SERVICE_PING```  | True | pre-ping connection before query |
| ```RELOCK_SERVICE_TIMEOUT```  | 60 | connection timeout |
| ```RELOCK_SERVICE_TAB_LOGOUT```  | True | control session integrity between user browser tabs |
| ```RELOCK_SERVICE_MULTITABS```  | True | allow multitab browsing |
| ```RELOCK_SERVICE_PROTECTED```  | True | restrict access to any route by default |
| ```RELOCK_BLUEPRINT```  | True | HTTP route name |

Example .env:
```
DB_USER=admin
DB_PASS=#SupperHidden123
DB_HOST=172.17.0.3
DB_PORT=3306
DB_NAME=demo

REDIS_HOST=172.17.0.2
REDIS_PORT=6379
REDIS_DB=1

RELOCK_SERVICE_HOST=127.0.0.1
RELOCK_SERVICE_API=
RELOCK_SERVICE_PORT=8111
RELOCK_SERVICE_POOL=3
RELOCK_SERVICE_PING=True
RELOCK_SERVICE_TIMEOUT=60
RELOCK_SERVICE_TAB_LOGOUT=True
RELOCK_SERVICE_MULTITABS=True
RELOCK_SERVICE_PROTECTED=True
RELOCK_BLUEPRINT=relock

NAME=Relock-Demo
HOST=relock.demo
MAIN=main
IP=0.0.0.0
VERSION=0.7.8
```

### Docker
Build the image:
```docker build -t relock-firewall .```

Run the server:
```
docker run --rm --name relock-firewall \
  -p 8080:8080 \
  -e RELOCK_SERVICE_HOST=172.17.0.5 \
  -e RELOCK_SERVICE_PORT=8111 \
  -e RELOCK_SERVICE_TIMEOUT=30 \
  relock-firewall
```

### Project Structure
```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── cli
│   ├── contexts
│   ├── models
│   ├── plugins
│   ├── routes
│   ├── static
│   └── templates
├── docker
│   ├── Dockerfile
│   ├── docker-entrypoint
│   ├── init-functions
│   └── valkey.conf
├── main.py
└── service
    ├── service
    └── valkey
```