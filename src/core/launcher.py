################################################################################
# CLI launcher
################################################################################
"""This is a nice launcher of the CLI interface where all options passed to the
   executable are treated."""

# packages
import getopt
import logging
import sys
from src.interpreter.interpreter import Interpreter

def Usage():
    logger=logging.getLogger('PyRules')
    logger.info('PyRules syntax')
    logger.info('--------------')
    logger.info(' ./bin/pyrules [options]')
    logger.info(' List of options:')
    logger.info('   ** -D or --debug  : debug mode')
    logger.info('   ** -V or --version: display the version number')

def LaunchPyRules(version, date, pyrules_dir):
    ## Logger
    logger=logging.getLogger('PyRules')

    ## Decoding options and arguments
    try:
        optlist,arglist = getopt.getopt(sys.argv[1:], 'DV', ['debug','version'])
    except getopt.GetoptError, err:
         logger.error(err)
         Usage()
         sys.exit()
    for o,a in optlist:
        if o in ["-D", "--debug"]:
            logger.setLevel(logging.DEBUG)
            logger.debug('Debug mode activated')
            logger.debug('--------------------')
        elif o in ["-V", "--version"]:
            logger.info("PyRules version " + version + " [ " + date  + " ]")
            sys.exit()

    ## The readline module is necessary for tab completion
    try:
        logger.debug('Trying to import readline')
        import readline
        logger.debug('  --> Success')
    except ImportError:
        try:
            logger.debug('  --> Failed.')
            logger.debug('Trying to import pyreadline')
            import pyreadline as readline
            logger.debug('  --> Success')
        except:
            logger.warning("For tab completion and history, install readline.")
    else:
        logger.debug('Importing rlcompletr')
        import rlcompleter
        logger.debug('  --> Success')
        apple_gcc_421 = ['GCC 4.2.1 (Apple Inc. build 5646)', 'r261:67515']
        if all([(x in sys.version) for x in apple_gcc_421]):
            readline.parse_and_bind("bind ^I rl_complete")
            readline.__doc__ = 'libedit'  
        elif hasattr(readline, '__doc__'):
            if 'libedit' not in readline.__doc__:
                readline.parse_and_bind("tab: complete")
            else:
                readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.__doc__ = 'GNU'
            readline.parse_and_bind("tab: complete")

    # Welcome message
    logger.info("")
    logger.info("*************************************************************")
    logger.info("*                                                           *")
    logger.info("*             W E L C O M E  to  P Y R U L E S              *")
    logger.info("*   __________        __________      .__                   *")
    logger.info("*   \______   \___.__.\______   \__ __|  |   ____   ______  *")
    logger.info("*    |     ___<   |  | |       _/  |  \  | _/ __ \ /  ___/  *")
    logger.info("*    |    |    \___  | |    |   \  |  /  |_\  ___/ \___ \   *")
    logger.info("*    |____|    / ____| |____|_  /____/|____/\___  >____  >  *")
    logger.info("*              \/             \/                \/     \/   *")
    logger.info("*                                                           *")
    logger.info("*    PyRules version "+"%-24s"%version + "%+12s"%date + "   *")
    logger.info("*                                                           *")
    logger.info("*                 Type 'help' for in-line help.             *")
    logger.info("*                                                           *")
    logger.info("*************************************************************")

    # loading the interpretr
    interpreter = Interpreter(pyrules_dir)
    interpreter = interpreter.cmdloop()

