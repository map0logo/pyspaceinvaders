# $LastChangedDate: 2009-08-23 18:40:21 -0500 (Sun, 23 Aug 2009) $
"""Class for drawing lines of text (specific to Space Invaders)"""
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

import pygame
from pyspaceinvaders_conf import Conf, Color

#-------------------------------------------------------------------------------
# Window class.
#-------------------------------------------------------------------------------

class Window:
    """Window main class"""
    def __init__(self, width, height, title):
        """Create pygame window with specified geometry and title"""
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        try:
            pygame.display.set_icon(pygame.image.load(Conf.WINDOW_ICON))
        except:
            pass

    def Clear( self ):
        """Clear surface"""
        self.surface.fill(Color.BG)
