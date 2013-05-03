#-*- coding:utf-8 -*-

from apps.views import index_r
from apps.member.views import member
from apps.batch.views import batch
from apps.ground.views import ground
from apps.examine.views import examine

URLS = (
    (index_r, ''),
    (member, '/member'),
    (batch, '/batch'),
    (ground, '/ground'),
    (examine, '/examine'),
)