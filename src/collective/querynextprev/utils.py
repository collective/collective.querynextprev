# -*- coding: utf-8 -*-
"""Utils."""


def expire_session_data(request):
    """Expire all querynextprev data in session."""
    for key in request.SESSION.keys():
        if key.startswith('querynextprev'):
            del request.SESSION[key]
