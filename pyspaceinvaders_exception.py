# $LastChangedDate: 2009-08-19 15:06:10 -0500 (Wed, 19 Aug 2009) $
# Exception handling.  Exception class Oops.
# Author:   Jim Brooks  http://www.jimbrooks.org
# Date:     initial 2004/08, rewritten 2009/08
# License:  GNU General Public License Version 2 (GPL2).
#===============================================================================

import traceback

#-------------------------------------------------------------------------------
# Exception handling.  Exception class Oops.
#-------------------------------------------------------------------------------

def PrintCallStack():
    """ Print call stack. """
    traceback.print_exc( file=sys.stderr )

def PrintException( exception=None ):
    """ Print information when an exception occurs. """
    """ Historically, PrintException() with no arg was placed in an "except:" clause. """
    """ However, the recommended new usage is to pass an exception object. """
    if ( exception == None ):
        print( "EXCEPTION: " )
    else:
        try:
            print(( "EXCEPTION: \"" + str(exception) + "\"" ))
        except:
            print( "EXCEPTION: " )

    PrintCallStack()

class Oops(Exception):  # class Oops(object) would be incorrect
    """ User-defined exception class. """
    """ """
    """ Example: """
    """ try: """
    """    raise Oops( "file missing" ) """
    """ except Exception as exception:  # class as instance """
    """    PrintException( exception ) """
    """ """
    """ Note: 'except class as instance' is the new Python 2.6/3.x syntax. """
    def __init__( self, text="" ):
        self.text = text[:]
        
    def __repr__( self ):
        return self.text

    def __str__( self ):  # need both __repr__ and __str__ despite Python docs
        return self.text
