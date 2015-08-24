# -*- coding: utf-8 -*-
from __future__ import unicode_literals

OPEN = 'OPEN'
IN_PROGRESS = 'PROGRESS'
IN_REVIEW = 'REVIEW'
DONE = 'DONE'
BLOCKED = 'BLOCKED'
TASK_STATUS = (
    (OPEN, OPEN),
    (IN_PROGRESS, IN_PROGRESS),
    (IN_REVIEW, IN_REVIEW),
    (DONE, DONE),
    (BLOCKED, BLOCKED),
)

DETAIL = 'DETAIL'
DELETE = 'DELETE'
CREATE = 'CREATE'
LIST = 'LIST'
UPDATE = 'UPDATE'
ACTION = (
    (DETAIL, DETAIL),
    (DELETE, DELETE),
    (CREATE, CREATE),
    (LIST, LIST),
    (UPDATE, UPDATE),
)

CSS_CLASS = (
    ('bg-todo', OPEN),
    ('bg-inprogress', IN_PROGRESS),
    ('bg-inreview', IN_REVIEW),
    ('bg-done', DONE),
    ('bg-blocked', BLOCKED)
)
