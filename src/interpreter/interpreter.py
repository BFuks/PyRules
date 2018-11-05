################################################################################
# The CLI
################################################################################
"""A user-friendly command line interface to run PyRules. It uses a homemade
   extension of the cmd package for command interpretation and tab completion.
   """

# Packages
import logging
import readline
import os

from src.interpreter.interpreter_base import InterpreterBase

# The interpreter class
class Interpreter(InterpreterBase):
    def __init__(self, pyrules_dir, *arg, **opt):
        # Getting the directry in which th program is stored
        self.pyrules_dir = pyrules_dir
        self.logger = logging.getLogger('PyRules')

        # Calling the constructor from InterpreterBase
        self.logger.debug("Starting the interpreter")
        InterpreterBase.__init__(self, *arg, **opt)

        # All homemade commands should be declared here
        # no command for the moment (add Benjamin for more information)

        # Importing history
        self.logger.debug("Loading the previous history")
        self.history_file=os.path.join(self.pyrules_dir,'.PyRulesHistory')
        try:
            readline.read_history_file(self.history_file)
            self.logger.debug('  --> Success')
        except:
            self.logger.debug('  --> Failed')
            pass

    def __del__(self):
        self.logger.debug("Stopping the interpreter")
        try:
            self.logger.debug('Saving the history in ' + self.history_file)
            readline.set_history_length(100)
            readline.write_history_file(self.history_file)
            self.logger.debug('  --> Success')
        except:
            self.logger.debug('  --> Failed')
            pass

    ## Here should comme the definition of all commands to be implemented
    ## with links to the help messages and autocompltion information


    # PreLoop
    def preloop(self):
        """Initializing before starting the main loop"""
        self.prompt = 'pyrules>'

    def deal_multiple_categories(self, dico):
        """convert the multiple category in a formatted list understand by our
        specific readline parser"""

        if 'libedit' in readline.__doc__:
            # No parser in this case, just send all the valid options
            out = []
            for name, opt in dico.items():
                out += opt
            return out

        # That's the real work
        out = []
        valid=0
        # if the key starts with number order the key with that number.
        for name, opt in dico.items():
            if not opt:
                continue
            name = name.replace(' ', '_')
            valid += 1
            out.append(opt[0].rstrip()+'@@'+name+'@@')
            # Remove duplicate
            d = {}
            for x in opt:
                d[x] = 1    
            opt = list(d.keys())
            opt.sort()
            out += opt

        if valid == 1:
            out = out[1:]
        return out

    def print_suggestions(self, substitution, matches, longest_match_length) :
        """print auto-completions by category"""
        longest_match_length += len(self.completion_prefix)
        try:
            if len(matches) == 1:
                self.stdout.write(matches[0]+' ')
                return
            self.stdout.write('\n')
            l2 = [a[-2:] for a in matches]
            if '@@' in l2:
                nb_column = self.getTerminalSize()//(longest_match_length+1)
                pos=0
                for val in self.completion_matches:
                    if val.endswith('@@'):
                        category = val.rsplit('@@',2)[1]
                        category = category.replace('_',' ')
                        self.stdout.write('\n %s:\n%s\n' % \
                           (category, '=' * (len(category)+2)))
                        start = 0
                        pos = 0
                        continue
                    elif pos and pos % nb_column ==0:
                        self.stdout.write('\n')
                    self.stdout.write(self.completion_prefix + val + \
                                      ' ' * (longest_match_length +1 -len(val)))
                    pos +=1
                self.stdout.write('\n')
            else:
                # nb column
                nb_column = self.getTerminalSize()//(longest_match_length+1)
                for i,val in enumerate(matches):
                    if i and i%nb_column ==0:
                        self.stdout.write('\n')
                    self.stdout.write(self.completion_prefix + val + \
                                     ' ' * (longest_match_length +1 -len(val)))
                self.stdout.write('\n')

            self.stdout.write(self.prompt+readline.get_line_buffer())
            self.stdout.flush()
        except Exception as error:
            if __debug__:
                 self.logger.error(error)

    def getTerminalSize(self):
        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                     '1234'))
            except:
                return None
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            try:
                cr = (env['LINES'], env['COLUMNS'])
            except:
                cr = (25, 80)
        return int(cr[1])

    def complete(self,text,state):
        """Return the next possible completion for 'text'.
         If a command has not been entered, then complete against command list.
         Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped

            if ';' in line:
                begin, line = line.rsplit(';',1)
                begidx = begidx - len(begin) - 1
                endidx = endidx - len(begin) - 1
                if line[:begidx] == ' ' * begidx:
                    begidx=0

            if begidx>0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames

            # correct wrong splittion with '\ '
            if line and begidx > 2 and line[begidx-2:begidx] == '\ ':
                Ntext = line.split(os.path.sep)[-1]
                self.completion_prefix = Ntext.rsplit('\ ', 1)[0] + '\ '
                to_rm = len(self.completion_prefix) - 1
                Nbegidx = len(line.rsplit(os.path.sep, 1)[0]) + 1
                data = compfunc(Ntext.replace('\ ', ' '), line, Nbegidx, endidx)
                self.completion_matches = [p[to_rm:] for p in data
                                              if len(p)>to_rm]
            # correct wrong splitting with '-'
            elif line and line[begidx-1] == '-':
             try:    
                Ntext = line.split()[-1]
                self.completion_prefix = Ntext.rsplit('-',1)[0] +'-'
                to_rm = len(self.completion_prefix)
                Nbegidx = len(line.rsplit(None, 1)[0])
                data = compfunc(Ntext, line, Nbegidx, endidx)
                self.completion_matches = [p[to_rm:] for p in data 
                                              if len(p)>to_rm]
             except Exception as error:
                 self.logger.error(error)
            else:
                self.completion_prefix = ''
                self.completion_matches = compfunc(text, line, begidx, endidx)

        self.completion_matches = [ (l[-1] in [' ','@','=',os.path.sep] 
                      and l or (l+' ')) for l in self.completion_matches if l]

        try:
            return self.completion_matches[state]
        except IndexError as error:
            return None

    def correct_splitting(line):
        """if the line finish with a '-' the code splits in a weird way
           on GNU_SPLITTING"""
        line = line.lstrip()
        if line[-1] in [' ','\t']:
            return '', line, len(line),len(enidx)
        return text, line, begidx, endidx
