from django.utils.deprecation import MiddlewareMixin
from debug_toolbar.middleware import DebugToolbarMiddleware


class AtopdedTo110DebugMiddleware(MiddlewareMixin, DebugToolbarMiddleware):
    """ formtools temporary workaround for Django 1.10 """
    pass
