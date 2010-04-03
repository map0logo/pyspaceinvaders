# $LastChangedDate: 2009-08-19 15:06:10 -0500 (Wed, 19 Aug 2009) $
# Game object classes.
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

import random
import pygame
from pyspaceinvaders_exception import *
from pyspaceinvaders_conf import *

#-------------------------------------------------------------------------------
# Base class of drawable objects.
#-------------------------------------------------------------------------------

class Drawable(object):
    """ Base class of drawable objects. """

    def __init__( self ):
        pass

    def Draw( self, surface ):
        pass

#-------------------------------------------------------------------------------
# Base class of game objects (player, aliens).
#-------------------------------------------------------------------------------

class Object(Drawable):
    """ Base class of game objects (player, aliens). """

    def __init__( self, game ):
        Drawable.__init__( self )
        self.game     = game
        self.valid    = True
        self.hit      = 0
        self.movement = ( 0, 0 )

#-------------------------------------------------------------------------------
# Player class.
#-------------------------------------------------------------------------------

class Player(Object):

    def __init__( self, game ):
        Object.__init__( self, game )
        self.game        = game
        self.image       = pygame.image.load( "img/player.png" ).convert()
        self.image2      = pygame.image.load( "img/playerb.png" ).convert()
        self.imageHit    = pygame.image.load( "img/explosion.png" ).convert()
        self.rect        = self.image.get_rect()
        self.imageFlip   = False
        self.step        = 3 * self.game.stride
        self.fire        = False
        self.fireLatency = 3
        self.salvo       = 5
        self.livesReset  = Conf.PLAYER_LIVES
        self.lives       = Conf.PLAYER_LIVES
        # Reset() does the rest.
        self.Reset( self.livesReset )

    def Reset( self, lives ):
        """ Let Game decide whether to reset lives or let lives decrease. """
        self.lives        = lives
        self.valid        = True
        self.hit          = 0  # counts down
        self.rect.centerx = self.game.window.width // 2
        self.rect.bottom  = self.game.ground

    def Hit( self ):
        self.hit = 30
        self.lives -= 1
        if self.lives <= 0:  # player out of lives?
            self.game.GameOver()

    def Draw( self, surface ):
        if self.hit <= 0:
            if self.imageFlip:
                surface.blit( self.image, self.rect )
            else:
                surface.blit( self.image2, self.rect )
        else:
            surface.blit( self.imageHit, self.rect )

#-------------------------------------------------------------------------------
# Alien class.
#-------------------------------------------------------------------------------

class Alien(Object):

    # Class constants:
    POINTS    = 50
    COL_CNT   = 10
    ROW_CNT   = 6
    TOTAL_CNT = COL_CNT * ROW_CNT

    # Class vars:
    imageFlip = False


    def __init__( self, game, fname, fname2 ):
        """ Pass filenames of 2 images that animation will alternate. """
        Object.__init__( self, game )
        self.image    = pygame.image.load( fname  ).convert()
        self.image2   = pygame.image.load( fname2 ).convert()
        self.imageHit = pygame.image.load( "img/explosion.png" ).convert()
        self.rect     = self.image.get_rect()
    
    def Hit( self ):
        self.hit = 7

    def Draw( self, surface ):
        if self.hit <= 0:
            if Alien.imageFlip:
                surface.blit( self.image, self.rect )
            else:
                surface.blit( self.image2, self.rect )
        else:
            surface.blit( self.imageHit, self.rect )

#-------------------------------------------------------------------------------
# Player missile class.
#-------------------------------------------------------------------------------

class PlayerMissile(Object):

    def __init__( self, game ):
        Object.__init__( self, game )
        self.image        = pygame.image.load( "img/missile_player.png" ).convert()
        self.rect         = self.image.get_rect()
        self.rect.centerx = self.game.player.rect.centerx
        self.rect.centery = self.game.player.rect.centery - self.game.player.rect.height

    def Draw( self, surface ):
        surface.blit( self.image, self.rect )

#-------------------------------------------------------------------------------
# Alien missile class.
#-------------------------------------------------------------------------------

class AlienMissile(Object):

    def __init__( self, game, alien ):
        Object.__init__( self, game )
        self.image        = pygame.image.load( "img/missile_alien.png" ).convert()
        self.rect         = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx + random.randint( -8, 8 )
        self.rect.centery = alien.rect.centery + alien.rect.height

    def Draw( self, surface ):
        surface.blit( self.image, self.rect )

#-------------------------------------------------------------------------------
# Mothership class.
#-------------------------------------------------------------------------------

class Mothership(Object):

    # Class constants:
    POINTS    = 100

    # Class vars:
    imageFlip = False
    horzDir   = -1

    def __init__( self, game):
        """ Pass filenames of 2 images that animation will alternate. """
        Object.__init__( self, game )
        self.image    = pygame.image.load( "img/mothership.png"  ).convert()
        self.image2   = pygame.image.load( "img/mothershipb.png" ).convert()
        self.imageHit = pygame.image.load( "img/explosion.png" ).convert()
        self.rect     = self.image.get_rect()
        self.tick = self.game.tick + random.randint( 20, 25)
        self.movement[0] = random.choice([-1,1])
        
    def SetAppearing( self ):
        self.tick = self.tick + random.randint( 20, 25)
        self.movement[0] = random.choice([-1,1])
    
    def Hit( self ):
        self.hit = 7

    def Draw( self, surface ):
        if self.hit <= 0:
            if Mothership.imageFlip:
                surface.blit( self.image, self.rect )
            else:
                surface.blit( self.image2, self.rect )
        else:
            surface.blit( self.imageHit, self.rect )
            
