# $LastChangedDate: 2009-08-19 15:06:10 -0500 (Wed, 19 Aug 2009) $
# Python library of utility functions.
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

from pyspaceinvaders_exception import *

#-------------------------------------------------------------------------------
# Functions (list).
#-------------------------------------------------------------------------------

def PruneList( list ):
    """ Prune invalid objects in a list. """
    """ Requires: Objects in elements have a .valid member. """
    """           List is flat (no nested sequences). """
    """ Iterating thru a list and deleting items """
    """ is an error in Python so a copy is used. """
    tmp = list[:]  # copy list (shallow copy)
    i = -1
    for obj in tmp:
        i += 1
        if not obj.valid:
            del list[i]
            i -= 1

def PruneListList( listList ):
    """ Prune invalid objects in a list of lists (2D list). """
    """ Requires: Objects in elements have a .valid member. """
    """           List must not be deeper than 2 levels. """
    tmpListList = listList[:]  # copy list (shallow copy)
    i = -1
    for list2 in tmpListList:  # for each 2nd-level list
        i += 1
        j = -1
        for obj in list2:
            j += 1
            if not obj.valid:
                del listList[i][j]
                j -= 1
