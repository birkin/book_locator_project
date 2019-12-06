# -*- coding: utf-8 -*-

import json, logging, pprint
from operator import itemgetter
from urllib.parse import unquote

from book_locator_app import settings_app


log = logging.getLogger(__name__)


FILE_MAPPER = {
    'rock': 'rock_meta.json',
    'sci': 'sci_meta.json' }

def arrange_metadata_by_floor( data_code ):
    """ Reorganizes metadata for printing.
        Called by views.print_labels() """
    assert data_code in ['rock', 'sci', 'chinese', 'japanese', 'korean']
    initial_dct = load_json( data_code )
    sorted_floor_list = prep_floor_list( initial_dct )  # TODO: I can do lots more work in this single-pass
    range_data_by_floor = prep_floor_ranges( sorted_floor_list, initial_dct )

def load_json( data_code ):
    """ Loads appropriate json file.
        Called by arrange_metadata_by_floor() """
    target_filename = FILE_MAPPER[data_code]
    initial_dct = {}
    with open( f'{settings_app.DATA_DIR}/{target_filename}', 'r' ) as f:
        initial_dct = json.loads( f.read() )
    log.debug( f'initial_dct.keys(), ```{initial_dct.keys()}```' )
    return initial_dct

def prep_floor_list( initial_dct ):
    """ Preps floor list.
        Example output: ['2', '3', '4', 'a', 'b']
        Called by arrange_metadata_by_floor() """
    floor_list = []
    for ( normalized_cn_key, range_info_dct) in initial_dct.items():
        if range_info_dct['floor']:
            if str(range_info_dct['floor']) not in floor_list:
                floor_list.append( str(range_info_dct['floor']) )
    # sorted_floor_list = sorted( floor_list, key=lambda x: str(x) )
    sorted_floor_list = sorted( floor_list )
    log.debug( f'sorted_floor_list, ```{sorted_floor_list}```' )
    return sorted_floor_list

def prep_floor_ranges( sorted_floor_list, initial_dct ):
    """ Preps ranges for each floor.
        Called by arrange_metadata_by_floor() """
    floor_dct = {}
    for floor in sorted_floor_list:
        floor_dct[floor] = []
    for ( normalized_cn_key, range_info_dct) in initial_dct.items():
        if range_info_dct['floor']:
            floor = str( range_info_dct['floor'] )
            # range_info_dct['normalized_callnumber'] = normalized_cn_key
            range_info_dct['padded_aisle'] = range_info_dct['aisle'].zfill( 5 )  # for possible sorting later
            floor_dct[floor].append( range_info_dct )
        # if len( floor_dct[floor] ) > 100:
        #     break
    log.debug( f'initial floor_dct, ```{pprint.pformat(floor_dct)}```' )
    # for ( floor_key, range_dct_lst ) in floor_dct.items():
    #     # sorted_range_dct_lst = sorted( range_dct_lst, key=itemgetter('normalized_start') )
    #     sorted_range_dct_lst = sorted( range_dct_lst, key=itemgetter('padded_aisle', 'normalized_start') )
    #     floor_dct[floor_key] = sorted_range_dct_lst

    for ( floor_key, range_dct_lst ) in floor_dct.items():
        duplicate_aisle_check = []
        for range_dct in range_dct_lst:
            if range_dct['aisle'] not in duplicate_aisle_check:
                duplicate_aisle_check.append( range_dct['aisle'] )
            else:
                range_dct['duplicate_aisle'] = True

    log.debug( f'final floor_dct, ```{pprint.pformat(floor_dct)}```' )
    return floor_dct


