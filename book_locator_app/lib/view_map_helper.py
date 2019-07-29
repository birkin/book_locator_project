# -*- coding: utf-8 -*-

import logging, pprint

from urllib.parse import unquote


log = logging.getLogger(__name__)


def parse_request( querydct ):
    """ Returns location and callnumber.
        Called by views.map() """
    log.debug( f'querydct, ```{pprint.pformat(querydct)}```' )
    location = querydct.get( 'loc', None )
    callnumber = querydct.get( 'call', None )
    status = querydct.get( 'status', None )
    title = querydct.get( 'title', None )
    ( location, callnumber, status, title ) = apply_unquote( location, callnumber, status, title )
    log.debug( f'location, `{location}`; callnumber, `{callnumber}`; status, `{status}`; title, `{title}`' )
    return ( location, callnumber, status, title )

def apply_unquote( location, callnumber, status, title ):
    """ Unquotes field.
        Called by parse_request() """
    if location:
        location = unquote( location )
    if callnumber:
        callnumber = unquote( callnumber )
    if status:
        status = unquote( status )
    if title:
        title = unquote( title )
    # log.debug( f'location, `{location}`; callnumber, `{callnumber}`; status, `{status}`; title, `{title}`' )
    log.debug( 'unquote applied' )
    return ( location, callnumber, status, title )
