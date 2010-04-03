# $LastChangedDate: 2009-08-19 15:06:10 -0500 (Wed, 19 Aug 2009) $
# Classes for drawing lines of text (generic).
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

import pygame
from pyspaceinvaders_exception import *
from pyspaceinvaders_conf import *
from pyspaceinvaders_objects import *

#-------------------------------------------------------------------------------
# Functions.
#-------------------------------------------------------------------------------

defaultFont = None
def GetDefaultFont():
    """ Get pygame's default font object. """
    global defaultFont
    if defaultFont:
        return defaultFont
    else:
        # Try to load font.
        try:
            defaultFont = pygame.font.SysFont( Conf.FONT_NAME, Conf.FONT_SIZE )
        except:
            try:
                defaultFont = pygame.font.Font( None, Conf.FONT_SIZE )
            except:
                raise Oops( "ERROR: pygame missing fonts!  Cannot render text!" )
        # Succeeded.
        return defaultFont

#-------------------------------------------------------------------------------
# Class that defines one line of text and its attributes.  Contained by TextPage.
#-------------------------------------------------------------------------------

class TextLine(Drawable):
    """ TextLine is a primitive object for one line of text and its attributes. """
    """ TextPage is a container of TextLine objects. """
    """ The user can build paragraphs as a list of TextLine objects. """

    def __init__( self, text="", x=0, y=0, color=(0xff,0xff,0xff,0xff), center=False, font=None ):
        """ font=None selects the pygame default font. """
        self.text   = text
        self.x      = x
        self.y      = y
        self.color  = color
        self.center = center
        self.font   = font or GetDefaultFont()  # font=GetDefaultFont() as default arg would break startup
        assert( self.font )

    def Draw( self, surface ):
        image = self.font.render( self.text, 1, self.color )
        rect = image.get_rect()
        if self.center:
            rect.centerx = self.x
            rect.centery = self.y
        else:
            rect.left = self.x
            rect.top  = self.y
        surface.blit( image, rect )

    def SetText( self, text ):
        self.text = text

    def SetPosition( self, x, y ):
        self.x = x
        self.y = y

    def SetColor( self, color ):
        self.color = color

    def SetFont( self, font ):
        self.font = font

#-------------------------------------------------------------------------------
# TextPage is a container of TextLine objects.
#-------------------------------------------------------------------------------

class TextPage(Drawable):
    """ TextPage is a container of TextLine objects. """
    """ Draw() is what actually renders text. """
    """ Effects of Show()/Hide() are delayed until Draw() is called. """
    """ Client must call Draw() every frame/tick. """

    def __init__( self ):
        self.textLines = { }

    def Draw( self, surface ):
        """ Draw all text lines of this TextPage. """
        for textLine in self.textLines:
            textLine.Draw( surface )

    def Show( self, textLine, show=True ):
        if show:
            # Insert text line.
            self.textLines[textLine] = textLine
        else:
            self.Hide( textLine )  # synonym

    def Hide( self, textLine ):
        # Remove text line.
        try:
            del self.textLines[textLine]
        except:
            pass

    def IfShowing( self, textLine ):
        """ True if text line is showing. """
        return textLine in self.textLines
