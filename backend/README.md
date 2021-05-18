# Build

```
docker build . -t a51backend
```

# Configure

You need these environment variables in a file.

```
DB_USERNAME=***
DB_PASSWORD=***
DB_ADDRESS=http://***.***.***.***:***
```

# Run

Running backend at local port 5000, which is mapped to container port 8000.
```
docker run -p 5000:8000 --env-file .env a51backend
```