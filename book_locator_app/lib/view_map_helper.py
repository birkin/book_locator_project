# -*- coding: utf-8 -*-

import logging, pprint

from urllib.parse import unquote


log = logging.getLogger(__name__)


def parse_request( querydct ):
    """ Returns location and callnumber.
        Called by views.map() """
    log.debug( f'querydct, ```{pprint.pformat(querydct)}```' )
    location = querydct.get( 'loc', None )
    call_number = querydct.get( 'call', None )
    status = querydct.get( 'status', None )
    title = querydct.get( 'title', None )
    ( location, call_number, status, title ) = apply_unquote( location, call_number, status, title )
    log.debug( f'location, `{location}`; call_number, `{call_number}`; status, `{status}`; title, `{title}`' )
    return ( location, call_number, status, title )

def apply_unquote( location, call_number, status, title ):
    """ Unquotes field.
        Called by parse_request() """
    if location:
        location = unquote( location )
    if call_number:
        call_number = unquote( call_number )
    if status:
        status = unquote( status )
    if title:
        title = unquote( title )
    # log.debug( f'location, `{location}`; call_number, `{call_number}`; status, `{status}`; title, `{title}`' )
    log.debug( 'unquote applied' )
    return ( location, call_number, status, title )
