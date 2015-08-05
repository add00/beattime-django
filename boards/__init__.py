# -*- coding: utf-8 -*-
from __future__ import unicode_literals

DONE = 'DONE'
IN_PROGRESS = 'IN PROGRESS'
REVIEW = 'REVIEW'
BLOCKED = 'BLOCKED'
TASK_STATUS = (
    (DONE[0], DONE),
    (IN_PROGRESS[0], IN_PROGRESS),
    (REVIEW[0], REVIEW),
    (BLOCKED[0], BLOCKED),
)
