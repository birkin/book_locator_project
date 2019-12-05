# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from . import settings_app
from book_locator_app.lib import view_map_helper, view_version_helper
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
    ( location, callnumber, status, title ) = view_map_helper.parse_request( request.GET )
    if ( location is None ) or ( callnumber is None ):
        return HttpResponseBadRequest( '400 / Bad Request -- Location and call number required.' )
    log.debug( f'Map requested for location ```{location}``` and callnumber ```{callnumber}```' )

    ## check location
    if location.lower() not in settings_app.LOCATE_LOCATIONS:
        return HttpResponseNotFound( '404 / Not Found -- No maps for this location.' )

    ## prepare data
    loc_data = bk_locator.run( callnumber.strip(), location )
    log.debug( f'loc_data, ```{loc_data}```' )
    floor = loc_data['floor']
    log.debug( f'floor, ```{floor}```' )
    floor_template = f'book_locator_app_templates/locations/{location}{floor}.html'
    log.debug( f'floor_template, ```{floor_template}```' )

    ## assemble data
    context = {
        'callnumber': callnumber,
        'floor_template': floor_template,
        'item': loc_data,
        'location': location,
        'status': status,
        'title': title,
    }
    log.debug( f'context, ```{pprint.pformat(context)}```' )

    ## spec template based on location
    item_template = f'book_locator_app_templates/{location}_item.html'
    log.debug( f'item_template, ```{item_template}```' )

    ## render response
    resp = render( request, item_template, context )
    return resp


def print_labels( request ):
    """ Manages labels for signage. """
    data = {
        'range_list': [
        {   'range_start': '65A',
            'callnumber_start': '2-SIZE N1 A25 v.8',
            'callnumber_end': '2-SIZE N9 J2 7',
            'building': 'Rock',
            'level': 'A',
            'date': '11/19' },
        {   'range_start': '65B',
            'callnumber_start': '2-SIZE N9 J2 8',
            'callnumber_end': '2-SIZE NA1288 S94 1998',
            'building': 'Rock',
            'level': 'A',
            'date': '11/19' },
        {   'range_start': '66A',
            'callnumber_start': 'N123456 A25 v.8',
            'callnumber_end': 'N901234 J2 7',
            'building': 'Rock',
            'level': 'A',
            'date': '11/19' },
        {   'range_start': '66B',
            'callnumber_start': 'P123456 A25 v.8',
            'callnumber_end': 'P901234 J2 7',
            'building': 'Rock',
            'level': 'A',
            'date': '11/19' },
        ] }
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse( json.dumps(data, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        resp = render( request, 'book_locator_app_templates/print_labels.html', data )
    log.debug( 'returning resp' )
    return resp

    return HttpResponse( 'labels under construction' )


def info( request  ):
    """ Redirects to something useful. """
    log.debug( 'info hit' )
    return HttpResponseRedirect( settings_app.INFO_URL )


# ===========================
# for development convenience
# ===========================


def version( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_version_helper.get_commit()
    branch = view_version_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_version_helper.make_context( request, rq_now, info_txt, taken )
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
