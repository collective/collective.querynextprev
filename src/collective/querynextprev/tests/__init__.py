# -*- coding: utf-8 -*-
import json


query = json.dumps(
    {
        "portal_type": "Document",
        "sort_on": "sortable_title",
    }
)

query_utf8 = json.dumps(
    {
        "portal_type": "Document",
        "sort_on": "id",
        "Title": "é",
    }
)


class DummyView(object):
    pass
