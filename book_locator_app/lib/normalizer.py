# -*- coding: utf-8 -*-

import logging, re

from book_locator_app.lib import lc


log = logging.getLogger(__name__)


SIZE = re.compile('^([1-3]\s?\-?SIZE|Size)\s(.*)', re.I)
# log.debug( f'SIZE, ```{SIZE}```' )

## Handling named collections.
## JAPANESE COLLECTION 2-SIZE Z9999 Z9
COLL = re.compile('''^
        (JAPANESE|CHINESE|KOREAN)\s #leading word, japanese, chinese, etc
        COLLECTION\s
        ((?:[1-3]-SIZE|Size)\s)? #optional size
        (.*) #lc
        ''', re.VERBOSE)
# log.debug( f'COLL, ```{COLL}```' )

## Reference collections
## RREF DE5 E RREF DS41 M44
REF = re.compile('''^
        (RREF)\s #leading description
        ((?:[1-3]-SIZE|Size)\s)? #optional size
        (.*) #lc
        ''', re.VERBOSE)
# log.debug( f'REF, ```{REF}```' )


class Item():
    """
    With an input of a call number and location code,
    normalize a call number to a sortable string using
    Brown specific logic.
    """

    def __init__(self, callnumber, location):
        self.callnumber = callnumber
        self.location = location

    def is_sci(self):
        bname = self.location
        if (bname == 'sciences') or (bname == 'sci'):
            return True

    def size_normalizer(self):
        """
        Brown specific normalizing routine for call numbers with size
        prefixes, e.g. 1-SIZE, 2-SIZE, 3-SIZE.
        """
        size_match = SIZE.search(self.callnumber)
        if size_match:
            size, lc = size_match.groups()
            # Try to normalize - if we can't return null.
            try:
                normalized_lc = self.lc_normalizer(number=lc)
            except ValueError:
                return
            # If normalization fails, stop here.
            if not normalized_lc:
                return
            if self.is_sci() is True:
                # Sciences inter-files 1-size only. So just normalize lc portion of call
                # for those.
                if size.lower() != '1-size':
                    return '%s %s' % (size, normalized_lc)
            return '%s %s' % (size, normalized_lc)

    def named_collections_normalizer(self):
        """
        Handle named collections.
        """
        match = COLL.search(self.callnumber)
        if match is not None:
            collection, size, lc = match.groups()
            # Normalize grabbed lc portion
            nc = self.lc_normalizer(number=lc)
            # Return if normalizing LC portion fails.
            if nc is None:
                return
            if size:
                return "%s %s %s" % (collection, size, nc)
            else:
                return "%s %s" % (collection, nc)

    def sized_formatter(self, collection, size, number):
        """
        Formatting tool for sized collection.
        Called by named and ref collection functions.
        """
        if size:
            return "%s %s %s" % (collection, size, number)
        else:
            return "%s %s" % (collection, number)

    def reference_collections_normalizer(self):
        match = REF.search(self.callnumber)
        if match is not None:
            ref, size, lc = match.groups()
            return self.sized_formatter(ref, size, lc)

    def lc_normalizer(self, number=None):
        """
        Straight normalizer via the LC call number normalization library:
        http://code.google.com/p/library-callnumber-lc/.

        """
        if number is None:
            number = self.callnumber
        try:
            n = lc.normalize(number)
        except ValueError:
            return
        return n

    def normalize(self):
        # Return first normalized call number
        by_size = self.size_normalizer()
        if by_size is not None:
            return by_size
        by_named = self.named_collections_normalizer()
        if by_named is not None:
            return by_named
        by_reference = self.reference_collections_normalizer()
        if by_reference is not None:
            return by_reference
        normal = self.lc_normalizer()
        return normal
