# -*- coding: utf-8 -*-

import logging

from book_locator_app.lib import view_map_helper
from django.test import TestCase
# from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this


log = logging.getLogger(__name__)
TestCase.maxDiff = None


class RootUrlTest( TestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url'. """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/'. """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )


class MapHelperTest( TestCase ):
    """ Checks view_map_helper functions. """

    def test_parse_request__non_encoded_spaces(self):
        """ Checks location with non-encoded spaces. """
        querydct = {'loc': 'rock', 'call': 'BL1442.Z4 B59 v.1'}
        self.assertEqual( ('rock', 'BL1442.Z4 B59 v.1'), view_map_helper.parse_request(querydct) )

    def test_parse_request__encoded_spaces(self):
        """ Checks location with non-encoded spaces. """
        querydct = {'loc': 'rock', 'call': 'BL1442.Z4%20B59%20v.1'}
        self.assertEqual( ('rock', 'BL1442.Z4 B59 v.1'), view_map_helper.parse_request(querydct) )
