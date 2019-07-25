# -*- coding: utf-8 -*-

import json, logging, os


log = logging.getLogger(__name__)


README_URL = os.environ['BK_LCTR__README_URL']

INFO_URL = os.environ['BK_LCTR__README_URL']

LOCATE_LOCATIONS = ['rock', 'sci']

DATA_DIR = os.environ['BK_LCTR__DATA_DIR_PATH']  # data saved from google-sheet
log.debug( f'DATA_DIR, ```{DATA_DIR}``' )


## auth
# SUPER_USERS = json.loads( os.environ['BK_LCTR__UPER_USERS_JSON'] )
# STAFF_USERS = json.loads( os.environ['BK_LCTR__STAFF_USERS_JSON'] )  # users permitted access to admin
# STAFF_GROUP = os.environ['BK_LCTR__STAFF_GROUP']  # not grouper-group; rather, name of django-admin group for permissions
# TEST_META_DCT = json.loads( os.environ['BK_LCTR__TEST_META_DCT_JSON'] )
# POST_LOGIN_ADMIN_REVERSE_URL = os.environ['BK_LCTR__POST_LOGIN_ADMIN_REVERSE_URL']  # tricky; for a direct-view of a model, the string would be in the form of: `admin:APP-NAME_MODEL-NAME_changelist`
