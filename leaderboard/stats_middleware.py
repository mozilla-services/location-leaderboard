import time

from leaderboard.stats import stats_client


class StatsMiddleware(object):

    def process_view(self, request, view, view_args, view_kwargs):
        request._stats_start = time.time()

        view_cls = getattr(view, 'cls', None)

        if view_cls is not None:
            request._stats_view_name = view.cls.__name__

    def process_response(self, request, response):
        if hasattr(request, '_stats_start'):
            duration = (time.time() - request._stats_start) * 1000
            view_name = getattr(request, '_stats_view_name', None)

            if view_name is not None:
                stats_client.timing(
                    'request_timing|{}'.format(
                        request._stats_view_name), duration)
                stats_client.incr(
                    'request_count|{}'.format(request._stats_view_name))

        return response
