docker buildx build --platform linux/amd64 -t python3arm . 
docker run -it --mount type=bind,source="$(pwd)",target=/app python3arm

