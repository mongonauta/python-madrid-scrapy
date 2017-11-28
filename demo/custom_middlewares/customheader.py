import logging

from scrapy.utils.project import get_project_settings


class AddCustomHeaderMiddleware(object):
    def __init__(self):
        super(AddCustomHeaderMiddleware, self).__init__()

    def process_request(self, request, spider):
        user_agent = request.headers.get('User-Agent')

        if not user_agent:
            settings = get_project_settings()
            request.headers.setdefault(settings.get('ENABLE_REQUESTS_STATS', False))
