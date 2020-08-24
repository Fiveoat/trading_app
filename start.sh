
docker build -q -t local:trading_app .
docker run /$PWD:/home/default_user/opt -it local:trading_app /bin/bash