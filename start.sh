
docker build -t local:trading_app .
docker run -it -p 5000:5000 local:trading_app /bin/sh

# docker build -q -t trading_app:latest .
# docker run
