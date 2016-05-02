import time

from leaderboard.stats import stats_client


class StatsMiddleware(object):

    def process_request(self, request):
        request._stats_start = time.time()

    def process_response(self, request, response):
        duration = (time.time() - request._stats_start) * 1000
        stats_client.timing('request_timing|{}'.format(request.path), duration)
        stats_client.incr('request_count|{}'.format(request.path))

        return response
