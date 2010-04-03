#!/usr/bin/env python
# $LastChangedDate: 2009-08-19 15:06:10 -0500 (Wed, 19 Aug 2009) $
# Python Space Invaders.
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

import sys
from pyspaceinvaders_exception import *
from pyspaceinvaders_conf import *
from pyspaceinvaders_window import *
from pyspaceinvaders_game import *

#===============================================================================
# Run.
#===============================================================================

pygame.init()
window = Window( Conf.WINDOW_WIDTH, Conf.WINDOW_HEIGHT, Conf.WINDOW_TITLE )
game = Game( window )
game.Run()
sys.exit( 0 )
