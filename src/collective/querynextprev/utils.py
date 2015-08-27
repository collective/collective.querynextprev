# -*- coding: utf-8 -*-
"""Utils."""
WINDOW_SIZE = 10


def expire_session_data(request):
    """Expire all querynextprev data in session."""
    for key in request.SESSION.keys():
        if key.startswith('querynextprev'):
            del request.SESSION[key]

def first_common_item(l1, l2):
    """Get first item in l2 that is also in l1."""
    for item in l2:
        if item in l1:
            return item

    return None


def get_next_items(l, index):
    """Get WINDOW_SIZE next items."""
    last_index = min(index + WINDOW_SIZE, len(l))
    return l[index+1:last_index+1]


def get_previous_items(l, index):
    """Get WINDOW_SIZE previous items."""
    first_index = max(index - 10, 0)
    return l[first_index:index]
