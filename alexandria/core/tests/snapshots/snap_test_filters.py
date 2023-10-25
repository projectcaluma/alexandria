# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_document_category_filters[filters0-2] 1"] = ["Apple", "Melon"]

snapshots["test_document_category_filters[filters1-1] 1"] = ["Melon"]

snapshots["test_document_category_filters[filters2-1] 1"] = ["Apple"]

snapshots["test_document_category_filters[filters3-0] 1"] = []

snapshots["test_document_category_filters[filters4-3] 1"] = ["Apple", "Melon", "Pear"]

snapshots["test_document_category_filters[filters5-2] 1"] = ["Apple", "Pear"]
