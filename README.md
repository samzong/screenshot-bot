# Screenshot Bot

This is a simple bot that takes a screenshot of a website and sends it to a user.


```bash
docker buildx build --load  --platform linux/amd64 -t screenshot-bot:v3  .

docker run -d --platform linux/amd64 --name screenshot-bot \
  -e CHROMEDRIVER_PATH=/app/bin/chromedriver_linux_amd64 \
  -e API_TOKEN=usk4faMS1dP8Tsr6ytchczb \
  -e DST_ID_OR_URL=dstbVJRkmzWy1YbXuc \
  screenshot-bot:latest
```

