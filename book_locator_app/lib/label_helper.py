# -*- coding: utf-8 -*-

import datetime, json, logging, pprint
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
    floor_dct = prep_floor_ranges( sorted_floor_list, initial_dct )
    duplicates = find_duplicates( floor_dct )
    ( updated_floor_dct, updated_duplicates ) = extract_duplicates( floor_dct, duplicates )
    return updated_floor_dct


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
    """ Attaches range-dct to floor-key for each floor.
        Example output: { 'a': [(aisle-1a-range-dct), (aisle-1b-range-dct)], 'b': ... }
        Called by arrange_metadata_by_floor() """
    floor_dct = {}
    for floor in sorted_floor_list:
        floor_dct[floor] = []
    for ( normalized_cn_key, range_info_dct) in initial_dct.items():
        if range_info_dct['floor']:
            floor = str( range_info_dct['floor'] )
            range_info_dct['padded_aisle'] = range_info_dct['aisle'].zfill( 5 )  # for possible sorting later

            ## data cleanup
            stripped_aisle = range_info_dct['aisle'].strip()
            range_info_dct['date_str'] = '%s/%s' % ( datetime.datetime.today().month, datetime.datetime.today().year )
            if stripped_aisle != range_info_dct['aisle']:
                log.debug( 'updating aisle with stripped version' )
                range_info_dct['aisle'] = stripped_aisle
            if 'location_code' not in range_info_dct.keys() and 'location-code' in range_info_dct.keys():
                range_info_dct['location_code'] = range_info_dct['location-code']
                del range_info_dct['location-code']
            elif 'location_code' not in range_info_dct.keys():
                range_info_dct['location_code'] = 'not_listed'

            # floor_dct[floor].append( range_info_dct )
            if len( floor_dct[floor] ) < 20:
                floor_dct[floor].append( range_info_dct )
    log.debug( f'floor_dct, ```{pprint.pformat(floor_dct)}```' )
    return floor_dct


def find_duplicates( floor_dct ):
    """ Finds the "multiple-aisle" entries and returns them.
        Called by arrange_metadata_by_floor() """
    all_duplicates_check = []  # will add, eg, {'floor': 'a'; 'aisle': '12b'}
    for ( floor_key, range_dct_lst ) in floor_dct.items():
        floor_duplicates_check = []
        for ( i, range_dct ) in enumerate( range_dct_lst ):  # ah, not using the index as I thought I would
            if range_dct['aisle'] not in floor_duplicates_check:
                floor_duplicates_check.append( range_dct['aisle'] )
            else:
                range_dct['duplicate_aisle'] = True  # not necessary for processing, but useful for visual check
                duplicate = {'floor': range_dct['floor'], 'aisle': range_dct['aisle']}
                all_duplicates_check.append( duplicate )
    log.debug( f'duplicates, ```{pprint.pformat(all_duplicates_check)}```' )
    return all_duplicates_check


def extract_duplicates( floor_dct, duplicates ):
    """ Replaces the list of range-dcts attached to each floor with a floor-level dict of aisle-keys:range-dct-values.
        Also merges the duplicate-ranges.
        Called by arrange_metadata_by_floor() """
    updated_floor_dct = {}
    for ( floor_key, range_dct_lst ) in floor_dct.items():
        log.debug( f'floor_key, `{floor_key}`' )
        aisle_dct = {}
        for range_dct in range_dct_lst:
            for dup_dct in duplicates:
                ## if this is one of the duplicates, update duplicates and save a temp-holder to the aisle_dct
                if range_dct['floor'] == dup_dct['floor'] and range_dct['aisle'] == dup_dct['aisle']:
                    if 'dup_list' not in dup_dct.keys():
                        dup_dct['dup_list'] = []
                    dup_dct['dup_list'].append( range_dct )
                    try:
                        temp_holder_dct = {
                            'aisle': range_dct['aisle'],
                            'begin': 'HANDLE-MANUALLY',
                            'end': '',
                            'floor': range_dct['floor'],
                            'location_code': range_dct['location_code'],
                            'normalized_start': '',
                            'note': 'MULTIPLE-ENTRIES for this range; PROCESS-MANUALLY for now with emailed data.',
                            'padded_aisle': range_dct['padded_aisle'],
                            'date_str': '%s/%s' % ( datetime.datetime.today().month, datetime.datetime.today().year )
                            }
                    except:
                        log.exception( 'problem creating temp_holder_dct; traceback follows' )
                        log.debug( f'problemmatic range_dct, ```{pprint.pformat(range_dct)}```')
                        raise Exception( 'see logs' )
                    aisle_dct[range_dct['padded_aisle']] = temp_holder_dct  # so this will happen twice, when the second item is found, but that's ok; the second temp-holder will just overwrite the first.
                else:
                    ## if this is NOT one of the duplicates, save the range-info to the aisle_dct
                    aisle_dct[range_dct['padded_aisle']] = range_dct  # I could pop out the unnecessary 'aisle' element
        updated_floor_dct[floor_key] = aisle_dct
    log.debug( f'updated_floor_dct, ```{pprint.pformat(updated_floor_dct)}```' )
    log.debug( f'enhanced duplicates, ```{pprint.pformat(duplicates)}```' )
    return ( updated_floor_dct, duplicates )


## Old code, when I thought it'd be useful to sort by aisle. No longer necessary; need to trust order of spreadsheet.
# for ( floor_key, range_dct_lst ) in floor_dct.items():
#     # sorted_range_dct_lst = sorted( range_dct_lst, key=itemgetter('normalized_start') )
#     sorted_range_dct_lst = sorted( range_dct_lst, key=itemgetter('padded_aisle', 'normalized_start') )
#     floor_dct[floor_key] = sorted_range_dct_lst


# check_dct = {'floor': range_dct['floor'], 'aisle': range_dct['aisle']}
# if next( (item for item in duplicates if item  == check_dct), False ) is False:  # <https://stackoverflow.com/a/31988734>
#     aisle_dct[range_dct['aisle']] = range_dct  # I could pop out the unnecessary 'aisle' element
# else:
#     pass
