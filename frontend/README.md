# Build

```
docker build . -t a51frontend
```

# Configure

You need to update the public backend address in the file Map.js

# Run

Running backend at local port 6000, which is mapped to container port 80.
```
docker run -p 6000:80 a51frontend
```