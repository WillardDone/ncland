# -*- coding: utf-8 -*-

from math import ceil

def getPageNum(index):
    try:
        _index = int(index)
    except Exception, e:
        _index = 1
    return _index


def slice_list(list, slice_into):
    for i in xrange(0, len(list), slice_into):
        yield list[i:i+slice_into]


def object_list(Query, per_page, page):
    
    object_list = []

    for list in slice_list(Query, per_page):
        object_list.append(list)

    if not object_list:
        object_list = [[]]
    try:
        result = object_list[page-1]
    except IndexError:
        result = object_list[0]
    return result


class Pagination(object):

    def __init__(self, Query, page, per_page):
        self.page = page
        self.per_page = per_page
        self.Query = Query

        if type(Query) != list:
            self.total_count = Query.query.count()
        else:
            self.total_count = len(Query)

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def list(self):
        if type(self.Query) != list: 
            result = self.Query.query.offset((self.page-1)*self.per_page)\
                .limit(self.per_page).all()
        else:
            result = object_list(self.Query, self.per_page, self.page)

        return result


class Paginate(object):

    def __init__(self, page, per_page, total):
        self.page = page
        self.per_page = per_page
        self.total_count = total

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num