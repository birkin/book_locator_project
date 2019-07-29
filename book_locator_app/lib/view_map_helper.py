# -*- coding: utf-8 -*-

import logging, pprint

from urllib.parse import unquote


log = logging.getLogger(__name__)


def parse_request( querydct ):
    """ Returns locatin and callnumber. """
    log.debug( f'querydct, ```{pprint.pformat(querydct)}```' )
    call_number = querydct.get( 'call', None )
    call_number = unquote( call_number )
    location = querydct.get( 'loc', None )
    location = unquote( location )
    log.debug( f'location, `{location}`; call_number, `{call_number}`' )
    return ( location, call_number )
