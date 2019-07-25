# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from . import settings_app
from book_locator_app.lib import view_info_helper
from book_locator_app.lib.locator import ServiceLocator
# from book_locator_app.lib.shib_auth import shib_login  # decorator
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)

bk_locator = ServiceLocator()


def map( request ):
    """ Manages build and display of map. """
    log.debug( 'map hit' )
    ## check params
    location = request.GET.get( 'loc', None )
    call_number = request.GET.get( 'call', None )
    if ( location is None ) or ( call_number is None ):
        return HttpResponseBadRequest( '400 / Bad Request -- Location and call number required.' )
    log.debug( f'Map requested for location ```{location}``` and call_number ```{call_number}```' )
    ## check location
    if location.lower() not in settings_app.LOCATE_LOCATIONS:
        return HttpResponseNotFound( '404 / Not Found -- No maps for this location.' )

    item_key = f'{location}-{call_number.strip()}'
    log.debug( f'item_key, ```{item_key}```' )

    loc_data = bk_locator.run(call_number.strip(), location)
    log.debug( f'loc_data, ```{loc_data}```' )

    return HttpResponse( 'coming' )


def info( request  ):
    """ Redirects to something useful. """
    log.debug( 'info hit' )
    return HttpResponseRedirect( settings_app.INFO_URL )


def version( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


# @shib_login
# def login( request ):
#     """ Handles authNZ, & redirects to admin.
#         Called by click on login or admin link. """
#     next_url = request.GET.get( 'next', None )
#     if not next_url:
#         redirect_url = reverse( settings_app.POST_LOGIN_ADMIN_REVERSE_URL )
#     else:
#         redirect_url = request.GET['next']  # will often be same page
#     log.debug( 'redirect_url, ```%s```' % redirect_url )
#     return HttpResponseRedirect( redirect_url )
