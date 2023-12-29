import urllib.parse

from rest_framework.pagination import LimitOffsetPagination


class NoDomainLimitOffsetPagination(LimitOffsetPagination):
    def get_next_link(self):
        next_page_url = super().get_next_link()
        if next_page_url is not None:
            parsed_next_page_url = urllib.parse.urlparse(next_page_url)
            next_page_url = next_page_url.split(parsed_next_page_url.hostname)[1]
        return next_page_url

    def get_previous_link(self):
        previous_page_url = super().get_previous_link()
        if previous_page_url is not None:
            parsed_previous_page_url = urllib.parse.urlparse(previous_page_url)
            previous_page_url = previous_page_url.split(parsed_previous_page_url.hostname)[1]
        return previous_page_url
