# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask import request, url_for, Markup


class Paginator(object):
    themes = {
        'bootstrap3': {
            'prev_page': '<li class="previous"><a href="{0}">{1}</a></li>',
            'next_page': '<li class="next"><a href="{0}">{1}</a></li>',
            'next_page_disabled': '<li class="next disabled"><a> {0} </a></li>',
            'prev_page_disabled': '<li class="previous disabled"><a> {0} </a></li>',
            'next_label': '&raquo;',
            'prev_label': '&laquo;',
            'current': '<li class="active"><a>{0}</a></li>',
            'link': '<li><a href="{0}">{1}</a></li>',
            'disabled_link': '<li class="disabled"><a>{0}</a></li>',
            'container_start': '<nav><ul class="pagination{0}">',
            'container_end': '</ul></nav>'
        },
        'bootstrap': {
            'prev_page': '<li class="page-item"><a class="page-link" href="{0}" aria-label="Previous">{1} <span class="sr-only">Previous</span></a></li>',
            'next_page': '<li class="page-item"><a class="page-link" href="{0}" aria-label="Next">{1} <span class="sr-only">Next</span></a></li>',
            'next_page_disabled': '<li class="page-item disabled"><a class="page-link" href="#" aria-label="Next"> {0} <span class="sr-only">Next</span></a></li>',
            'prev_page_disabled': '<li class="page-item disabled"><a class="page-link" href="#" aria-label="Previous"> {0} <span class="sr-only">Previous</span></a></li>',
            'next_label': '&raquo;',
            'prev_label': '&laquo;',
            'current': '<li class="page-item active"><a class="page-link" href="#">{0} <span class="sr-only">(current)</span></a></li>',
            'link': '<li class="page-item"><a class="page-link" href="{0}">{1}</a></li>',
            'disabled_link': '<li class="page-item disabled"><a>{0}</a></li>',
            'container_start': '<nav><ul class="pagination pagination-sm{0}">',
            'container_end': '</ul></nav>'
        },
        'foundation': {
            'prev_page': '<li class="pagination-previous"><a href="{0}">{1}</a></li>',
            'next_page': '<li class="pagination-next"><a href="{0}">{1}</a></li>',
            'next_page_disabled': '<li class="pagination-next disabled">{0}</li>',
            'prev_page_disabled': '<li class="pagination-previous disabled">{0}</li>',
            'prev_label': 'Previous <span class="show-for-sr">page</span>',
            'next_label': 'Next <span class="show-for-sr">page</span></a>',
            'current': '<li class="current"><span class="show-for-sr">You\'re on page</span> {0}</a></li>',
            'link': '<li><a href="{0}">{1}</a></li>',
            'disabled_link': '<li class="ellipsis" aria-hidden="true"></li>',
            'container_start': '<nav><ul class="pagination{0}" role="navigation" aria-label="Pagination">',
            'container_end': '</ul></nav>'
        }
    }

    def __init__(self, **kwargs):
        self.page = kwargs.pop('page') or 1
        self.page = int(self.page)
        self.query = kwargs.pop('query')
        self.cquery = self.query.clone()

        self.theme = Paginator.themes[kwargs.pop('theme', 'bootstrap3')]
        self.per_page = kwargs.pop('per_page', 10)
        self.inner_range = kwargs.pop('inner_range', 2)
        self.outer_range = kwargs.pop('outer_range', 1)

        self.items = self.query.limit(position=((self.page - 1) * self.per_page), limit=self.per_page)
        self.current_total = self.cquery.count()

    # HTML
    @property
    def prev_page_url(self):
        if self.has_prev:
            page = self.page - 1 if self.page > 2 else None
            return self.page_href(page)
        return False

    @property
    def next_page_url(self):
        if self.has_next:
            return self.page_href(self.page + 1)
        return False

    @property
    def prev_page(self):
        if self.has_prev:
            page = self.page - 1 if self.page > 2 else None
            url = self.page_href(page)
            return self.theme['prev_page'].format(url, self.theme['prev_label'])

        return self.theme['prev_page_disabled'].format(self.theme['prev_label'])

    @property
    def next_page(self):
        if self.has_next:
            url = self.page_href(self.page + 1)
            return self.theme['next_page'].format(url, self.theme['next_label'])

        return self.theme['next_page_disabled'].format(self.theme['next_label'])

    @property
    def first_page(self):
        if self.has_prev:
            return self.theme['link'].format(self.page_href(None), 1)
        return self.theme['current'].format(1)

    @property
    def last_page(self):
        if self.has_next:
            url = self.page_href(self.total_pages)
            return self.theme['link'].format(url, self.total_pages)
        return self.theme['current'].format(self.page)

    def single_page(self, page):
        if page == self.page:
            return self.theme['current'].format(page)
        if page == 1:
            return self.first_page
        if page == self.total_pages:
            return self.last_page

        return self.theme['link'].format(self.page_href(page), page)

    @property
    def links(self):
        if self.total_pages <= 1:
            return ''

        s = [self.theme['container_start'].format('')]
        s.append(self.prev_page)
        for page in self.pages:
            s.append(self.single_page(page) if page else self.theme['disabled_link'].format('...'))

        s.append(self.next_page)
        s.append(self.theme['container_end'])
        return Markup(''.join(s))

    # Utils
    def page_href(self, page):
        return url_for(self.endpoint, page=page, **self.args)

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def endpoint(self):
        return request.endpoint

    @property
    def total_pages(self):
        pages = divmod(self.current_total, self.per_page)
        return pages[0] + 1 if pages[1] else pages[0]

    @property
    def args(self):
        request_args = request.args.iteritems(multi=True)
        view_args = request.view_args.iteritems()

        args = {}
        for k, value in list(request_args) + list(view_args):
            if k == 'page':
                continue
            if k not in args:
                args[k] = value
            elif not isinstance(args[k], list):
                args[k] = [args[k], value]
            else:
                args[k].append(value)

        return args

    @property
    def pages(self):
        if self.total_pages < self.inner_range * 2 - 1:
            return range(1, self.total_pages + 1)

        pages = []
        range_from = self.page - self.inner_range
        range_to = self.page + self.inner_range
        if range_to > self.total_pages:
            range_from -= range_to - self.total_pages
            range_to = self.total_pages

        if range_from < 1:
            range_to = range_to + 1 - range_from
            range_from = 1
            if range_to > self.total_pages:
                range_to = self.total_pages

        if range_from > self.inner_range:
            pages.extend(range(1, self.outer_range + 1 + 1))
            pages.append(None)
        else:
            pages.extend(range(1, range_to + 1))

        if range_to < self.total_pages - self.inner_range + 1:
            if range_from > self.inner_range:
                pages.extend(range(range_from, range_to + 1))

            pages.append(None)
            pages.extend(range(self.total_pages - 1, self.total_pages + 1))
        elif range_from > self.inner_range:
            pages.extend(range(range_from, self.total_pages + 1))
        else:
            pages.extend(range(range_to + 1, self.total_pages + 1))

        return pages
