# $LastChangedDate: 2009-08-19 20:25:35 -0500 (Wed, 19 Aug 2009) $
# Top-level of the game.
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

import sys, random
import pygame
from pyspaceinvaders_exception import *
from pyspaceinvaders_lib import *
from pyspaceinvaders_conf import *
from pyspaceinvaders_objects import *
from pyspaceinvaders_collision import *
from pyspaceinvaders_text import *
from pyspaceinvaders_game_text import *

#-------------------------------------------------------------------------------
# Top-level of the game.
#-------------------------------------------------------------------------------

class Game:
    """ Top-level of the game. """

    # Major game states:
    STATE_OVER  = -2  # enums
    STATE_PAUSE = -1
    STATE_STOP  = 0
    STATE_PLAY  = 1

    def __init__( self, window ):
        # Misc vars:
        self.window  = window
        self.state   = Game.STATE_STOP
        self.stride  = 1.0  # effective speed
        self.tick    = 0
        self.tempo   = 1  # fewer aliens will move faster 
        self.score   = 0
        self.level   = 1
        self.cheat   = 0  # 1: 999 lives 2: 999 lives + machine-guns
        self.ground  = window.height - Conf.GROUND_PADDING
        self.ceiling = Conf.CEILING

        # Game objects:
        self.player         = Player( self )
        self.alienColumns   = [ ]
        self.playerMissiles = [ ]
        self.alienMissiles  = [ ]

        # Initialize text-lines.
        self.gameTextPage = GameTextPage( self )

        # Initialize timer-tick.
        self.pollClock = pygame.USEREVENT + 1
        pygame.time.set_timer( self.pollClock, Conf.TIMER_TICK )

        # Initialize chaos.
        random.seed()

        # Start at level 1.
        self.Reset( level=1 )

    def Reset( self, level=1 ):
        """ Reset game state for a level. """
        assert( level >= 1 )
        self.tick  = 0
        self.tempo = 1
        self.level = level
        if level == 1:
            self.score = 0  # keep score while advancing levels

        # Hide "Game Over".
        self.gameTextPage.ShowGameOver( False )

        # Reset player.
        # Renew lives after advancing level.
        self.player.Reset( self.player.livesReset )

        # Delete all aliens (invalidate then prune).
        if len(self.alienColumns):
            for col in range(Alien.COL_CNT):
                for alien in self.alienColumns[col]:
                    alien.valid = False
            PruneListList( self.alienColumns )
            
        # Create a full population of aliens.
        self.alienColumns = [ ]
        for col in range(Alien.COL_CNT):
            self.alienColumns.append( [ ] )
            for row in range(Alien.ROW_CNT):
                if row == 0:
                    fname  = "img/alien1.png"
                    fname2 = "img/alien1b.png"
                elif row <= 2:
                    fname  = "img/alien2.png"
                    fname2 = "img/alien2b.png"
                else:
                    fname  = "img/alien3.png"
                    fname2 = "img/alien3b.png"
                alien = Alien( self, fname, fname2 )
                alien.rect.move_ip( col * 44 + 40, row * 40 + self.ceiling )
                self.alienColumns[col].append( alien )

        # Delete any missiles.
        if len(self.playerMissiles):
            for missile in self.playerMissiles:
                missile.valid = False
            PruneList( self.playerMissiles )
        if len(self.alienMissiles):
            for missile in self.alienMissiles:
                missile.valid = False
            PruneList( self.alienMissiles )

    def GameOver( self ):
        """ Switch to GAME_OVER state. """
        self.state = Game.STATE_OVER
        self.gameTextPage.ShowGameOver( True )

    def TogglePause( self ):
        """ Toggle pause if playing else NOP. """
        if self.state == Game.STATE_PLAY:
            self.state = Game.STATE_PAUSE
        elif self.state == Game.STATE_PAUSE:
            self.state = Game.STATE_PLAY
        # else NOP

    def AlienList( self ):
        """ For convenience, return a single list from the lists of alien columns. """
        """ NOTE: The list returned is a derivation.  It shouldn't be modified (treat as read-only). """
        alienList = [ ]
        for col in range(Alien.COL_CNT):
            for alien in self.alienColumns[col]:
                alienList.append( alien )
        return alienList

    def Draw( self ):
        """ Render a frame. """
        surface = self.window.surface

        # Clear window.
        self.window.Clear()

        # If stopped, only draw text.
        # Draw text lines over whatever was drawn.
        if self.state != self.STATE_STOP:
            self.Draw2()
        self.gameTextPage.Draw( surface )

        # Double-buffering.
        pygame.display.flip()

    def Draw2( self ):
        """ Draw everything (excluding text lines). """
        surface = self.window.surface

        # Draw player.
        self.player.Draw( surface )

        # Draw aliens.
        for alien in self.AlienList():
            alien.Draw( surface )

        # Draw player missiles.
        for missile in self.playerMissiles:
            if (missile.valid) and (missile.rect.centery > 0):
                missile.Draw( surface )

        # Draw alien missiles.
        for missile in self.alienMissiles:
            if (missile.valid) and (missile.rect.centery < self.window.height):
                missile.Draw( surface )

    def Animate( self ):
        """ Main animation function. """
        """ Assumes: invocation driven by timer-tick. """
        # Periodically prune invalid objects.
        PruneList( self.playerMissiles )
        PruneList( self.alienMissiles )
        PruneListList( self.alienColumns )

        # Animate only if playing.
        if self.state == Game.STATE_PLAY:
            alienList = self.AlienList()
            self.AnimatePlayer( alienList )
            self.AnimateAliens( alienList )
            PlayerAlienCollision( self.player, alienList )

    def AnimatePlayer( self, alienList ):
        """ Animate player. """
        # Animate exploding player (ok if not hit).
        self.player.hit -= 1

        # Don't let player move while exploding.
        if self.player.hit <= 0:
            # Continue player movement until key released.
            if self.player.movement != (0,0):
                if  (self.player.rect.left  + self.player.movement[0] > 0) \
                and (self.player.rect.right + self.player.movement[0] < self.window.width):
                    self.player.rect.move_ip( self.player.movement[0], 0 )
                    self.player.imageFlip = not self.player.imageFlip
            # Player's gun has a latency period and a limited salvo.
            if  (self.player.fire) \
            and ((self.tick % self.player.fireLatency) == 0) \
            and (len(self.playerMissiles) < self.player.salvo):
                self.playerMissiles.append( PlayerMissile( self ) )

        # Animate missiles from player.
        missileIdx = -1
        for missile in self.playerMissiles:
            missileIdx += 1
            # Animate missile.
            missile.rect.centery -= 10 * self.stride
            # Off-screen?
            if missile.rect.top < self.ceiling:
                missile.valid = False # will be pruned later
                continue
            # Has player's missiles hit any alien?
            # Exclude any hit alien from further collision-detection
            # in order to allow player missiles to fly thru explosion
            # to hit a higher alien.
            for alien in alienList:
                if Collided( missile, alien ) and (alien.valid) and (alien.hit <= 0):
                    alien.Hit()
                    self.score += Alien.POINTS
                    if self.cheat != 2:
                        missile.valid = False
            # Has this missile hit any opposite missile?
            MissileMissileCollision( missile, missileIdx, self.alienMissiles )

    def AnimateAliens( self, alienList ):
        """ Animate aliens (part 1). """
        # Animate aliens (unless player is hit/exploding).
        if self.player.hit <= 0:
            # Call actual routine.
            (invaded,alienCnt) = self.AnimateAliens2( alienList )
            # Game over if aliens have invaded (reached the ground)
            # even if player has remaining lives.
            # Or were all aliens destroyed?  If so, goto next level.
            if invaded:
                self.GameOver()
            elif alienCnt == 0:
                self.Reset( self.level + 1 )

    def AnimateAliens2( self, alienList ):
        """ Animate aliens (part 2). """
        """ Returns: (invaded,alienCnt) """
        """ "invaded" true if any alien has reached the ground. """
        invaded = False

        # Animate the walking of aliens by flipping their images.
        if (self.tick % 5) == 0:
            Alien.imageFlip = not Alien.imageFlip

        # Only aliens at bottom of columns can fire.
        for list in self.alienColumns:
            if len(list):
                alien = list[-1]  # last element (alien at bottom of column)
                if random.randint( 0, 1000 ) > (999 - min(20,2*self.tempo)):
                    self.alienMissiles.append( AlienMissile( self, alien ) )

        # Animate missiles from aliens.
        missileIdx = -1
        for missile in self.alienMissiles:
            missileIdx += 1
            # Animate missile.
            missile.rect.centery += 10 * self.stride
            # Off-screen?
            if missile.rect.bottom > self.ground:
                missile.valid = False  # will be pruned later
                continue
            # Has an alien missile hit the player?
            # Ignore further hits while player explodes.
            if Collided( missile, self.player ) and (self.player.hit <= 0):
                missile.valid = False
                self.player.Hit()
            # Has this missile hit any opposite missile?
            MissileMissileCollision( missile, missileIdx, self.playerMissiles )

        # Animate alien movement:
        # - right-to-left
        # - down
        # - left-right
        # - down
        # - repeat

        # Move all aliens left or right.
        for alien in alienList:
            alien.rect.centerx += Alien.horzDir * self.tempo * self.stride

        # Has any alien hit the left/right edge of screen?
        hitEdge = False
        padding = 4
        for alien in alienList:
            if (alien.rect.left - padding < 0) \
            or (alien.rect.right + padding > self.window.width):
                hitEdge = True
                break
        if hitEdge:
            # Reverse horizontal direction of aliens.
            Alien.horzDir = -Alien.horzDir
            # Move all aliens downward one step.
            for alien in alienList:
                alien.rect.centery += 4 * self.stride
                # Has this alien invaded (reached the ground)?
                if alien.rect.bottom >= self.ground:
                    invaded = True

        # Decrement alien.hit of every alien
        # in order to animate exploding aliens.
        for alien in alienList:
            alien.hit -= 1
            # Subtle: An alien is dead if .hit was decremented from 1 to 0.
            # .hit is assigned a positive value if alien was struck.
            if alien.hit == 0:
                alien.valid = False

        # Increase tempo (alien movement) as the amount of aliens decreases.
        factor = Alien.TOTAL_CNT / 4.0
        self.tempo = min(10,self.level)
        if len(alienList) > 5:
            self.tempo += 4 - int( len(alienList) / factor ) + 1
        else:
            self.tempo += 12  # very quick when few aliens survive

        return (invaded,len(alienList))

    def Run( self ):
        """ The main event loop. """
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:        
                sys.exit( 0 )
            elif event.type == self.pollClock:
                # New tick/frame.
                self.tick += 1
                self.Animate()
                self.Draw()
            elif event.type == pygame.KEYDOWN:
                # Start game?
                if event.key == pygame.K_1:
                    self.Reset( level=1 )
                    self.state = Game.STATE_PLAY
                    self.gameTextPage.ShowSplash( False )
                # Quit?
                elif event.key == pygame.K_ESCAPE:
                    sys.exit( 0 )
                # Pause/help?
                elif event.key == pygame.K_p:
                    # If paused, keep help showing (don't toggle).
                    if self.state != Game.STATE_STOP:
                        self.gameTextPage.ToggleHelp()
                    self.TogglePause()
                # Cheat?
                elif event.key == pygame.K_F5:
                    self.cheat = 1
                    self.player.livesReset = 999
                    self.player.lives      = 999
                    self.player.salvo = 8
                elif event.key == pygame.K_F6:
                    self.cheat = 2
                    self.player.livesReset = 999
                    self.player.lives      = 999
                    self.player.salvo = 16
            
                #----ignore other keys if not playing----
                if self.state != Game.STATE_PLAY:
                    continue
                #----ignore other keys if not playing----
    
                # Move player left?
                if (event.key == pygame.K_z) or (event.key == pygame.K_LEFT):
                    self.player.movement = ( -self.player.step, 0 )
                # Move player right?
                elif (event.key == pygame.K_x) or (event.key == pygame.K_RIGHT):
                    self.player.movement = ( self.player.step, 0 )
                # Player fired gun?
                elif (event.key == pygame.K_RCTRL) or (event.key == pygame.K_LCTRL):
                    self.player.fire = True
            elif event.type == pygame.KEYUP:
                # Stop moving player?
                if (event.key == pygame.K_z) or (event.key == pygame.K_x) or (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                    self.player.movement = ( 0, 0 )
                # Player stopped firing gun?
                elif (event.key == pygame.K_RCTRL) or (event.key == pygame.K_LCTRL):
                    self.player.fire = False
