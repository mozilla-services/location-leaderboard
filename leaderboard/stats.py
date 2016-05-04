import statsd

stats_client = statsd.StatsClient(
    'localhost', 8125, prefix='location_leaderboard')
