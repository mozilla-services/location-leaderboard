printf '{"commit":"%s","version":"%s","source":"https://github.com/mozilla-services/location-leaderboard"}\n' "$(git rev-parse HEAD)" "$(git describe --tags)"
