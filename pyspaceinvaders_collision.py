# $LastChangedDate: 2009-08-19 15:06:10 -0500 (Wed, 19 Aug 2009) $
# Collision-detection functions.
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

from pyspaceinvaders_exception import *

#-------------------------------------------------------------------------------
# Collision-detection functions.
#-------------------------------------------------------------------------------

def Collided( obj1, obj2 ):
    """ Return true if one object has collided into another. """
    if obj1.valid and obj2.valid:
        return obj1.rect.colliderect( obj2.rect )
    else:
        return False

def MissileMissileCollision( missile, missileIdx, oppMissileList ):
    """ Missile/missile collisions. """
    """ Detects if one missile has collided into any opposite missiles (plural). """
    if missile.valid:
        oppMissileIdx = -1
        for oppMissile in oppMissileList:
            oppMissileIdx += 1
            if oppMissile.valid and Collided( missile, oppMissile ):
                missile.valid = False
                oppMissile.valid = False

def PlayerAlienCollision( player, alienList ):
    """ Has any alien collided into the player? """
    for alien in alienList:
        # Ignore further collisions while both are exploding.
        if alien.valid and Collided( alien, player ):
            if (alien.hit <= 0) and (player.hit <= 0):
                alien.Hit()
                player.Hit()
