# ~*~ coding: utf-8 ~*~
import wsmeext.pecan as wsme_pecan


def expose(*args, **kwargs):
    """
    确保返回的数据为Json格式.
    """
    if 'rest_content_types' not in kwargs:
        kwargs['rest_content_types'] = ('json',)
    return wsme_pecan.wsexpose(*args, **kwargs)

