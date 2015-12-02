#!/bin/bash
set -ev

# ex: docker run --net=host -v $PWD/leaderboard/served/:/leaderboard/leaderboard/public/ leaderboard /bin/bash /leaderboard/scripts/start_leaderboard.sh
cp -Rv /leaderboard/leaderboard/served/static/ /leaderboard/leaderboard/public/ && gunicorn -b 0.0.0.0:7001 leaderboard.wsgi
