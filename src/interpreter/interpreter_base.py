################################################################################
# The extension of the cmd library
# Inspired by MadAnalysis 5
################################################################################
"""  A file containing different extension of the cmd basic python library"""

# packages
import cmd
import logging
import os
import re
import subprocess

#===============================================================================
# InterpreterBase
#===============================================================================
class InterpreterBase(cmd.Cmd):
    """Extension of the cmd.Cmd command line that supports line breaking,
       history, comments, internal call to cmdline, tab completion, ..."""

    class InvalidCmd(Exception):
        """Expection for a wrong command"""
        pass

    def __init__(self, *arg, **opt):
        """Init history and line continuation"""
        # Logger
        self.logger=logging.getLogger('PyRules')

        # string table for history
        self.history = []

        # beginning of the incomplete line (line break with '\') 
        self.save_line = ''
        cmd.Cmd.__init__(self, *arg, **opt)
        self.__initpos = os.path.abspath(os.getcwd())

    # Formatting the line before interpreting
    def precmd(self, line):
        """ A suite of additional functions to clean command (history, line
        breaking, comment treatment,...)"""

        # Ignore empty line
        if not line:
            return line

        # Removing additionnal whitespace characters
        line = line.lstrip()

        # Add the line to the history
        # except for a few commands
        self.logger.debug(self.history)
        if not any([line.startswith(x) for x in ['history', '#', 'help']]):
            self.history.append(line)

        # Multiple-line commands
        if self.save_line:
            line = self.save_line + line
            self.save_line = ''

        # Check if the line is complete
        if line.endswith('\\'):
            self.save_line = line[:-1]
            return '' # do nothing

        # Remove comment (ugly but I haven't found better so far)
        open_singlequote = False
        open_doublequote = False
        for i in range(len(line)):
            if line[i]=="'" and not open_doublequote:
                open_singlequote = not open_singlequote
            elif line[i]=='"' and not open_singlequote:
                 open_doublequote = not open_doublequote
            elif line[i]=='#' and not open_singlequote and not open_doublequote:
               line = line[0:i]
               break

        # Isolating operator
        operators = ['(',')','[',']','&','|','&','^','!','=','>','<',',']
        if not line.startswith('shell'):
            for item in operators:
                line=line.replace(item,' '+item+' ')

        # Deal with line splitting
        if ';' in line and not any([line.startswith(x) for x in ['shell','!']]):
            for subline in line.split(';'):
                stop = self.onecmd(subline)
                stop = self.postcmd(stop, subline)
            return ''

        # debug
        self.logger.debug('Entered command: ' + str(self.split_arg(line)))

        # execute the line command
        return line

    def exec_cmd(self, line, errorhandling=False):
        """for third party call, call the line with pre and postfix treatment
        without global error handling """

        self.logger.info(line)
        line = self.precmd(line)
        if errorhandling:
            stop = self.onecmd(line)
        else:
            stop = cmd.Cmd.onecmd(self, line)
        stop = self.postcmd(stop, line)
        return stop

    def run_cmd(self, line):
        return self.exec_cmd(line, errorhandling=True)

    def emptyline(self):
        pass

    def default(self, line):
        # Faulty command
        self.logger.warning("Command \"%s\" not implemented." % \
             line.split()[0])

    # Quit
    def do_quit(self, line):
        """ Exit the mainloop() """
        return True

    def help_quit(self):
        self.logger.info("This commands exits the program")

    # Aliases
    do_EOF   = do_quit
    do_exit  = do_quit
    help_EOF = help_quit
    help_exit= help_quit

    @staticmethod
    def list_completion(text, list):
        """Propose completions of text in list"""
        if not text:
            completions = list
        else:
            completions = [ f
                            for f in list
                            if f.startswith(text)
                            ]
        return completions

    @staticmethod
    def path_completion(text, base_dir=None, only_dirs=False, relative=True):
        """Propose completions of text to compose a valid path"""

        if base_dir is None:
            base_dir = os.getcwd()

        prefix, text = os.path.split(text)
        base_dir = os.path.join(base_dir, prefix)

        if prefix:
            prefix += os.path.sep

        if only_dirs:
            completion = [prefix + f for f in os.listdir(base_dir) if \
                (f.startswith(text) and \
                 os.path.isdir(os.path.join(base_dir, f)) and \
                 (not f.startswith('.') or text.startswith('.'))) ]
        else:
            completion = [ prefix + f for f in os.listdir(base_dir) if \
                (f.startswith(text) and \
                 os.path.isfile(os.path.join(base_dir, f)) and \
                 (not f.startswith('.') or text.startswith('.'))) ]

            completion = completion + \
              [prefix + f + os.path.sep for f in os.listdir(base_dir) if \
                 (f.startswith(text) and \
                  os.path.isdir(os.path.join(base_dir, f)) and \
                  (not f.startswith('.') or text.startswith('.'))) ]

        if relative:
            completion += [prefix + \
                f for f in ['.'+os.path.sep, '..'+os.path.sep] if \
                (f.startswith(text) and not prefix.startswith('.')) ]

        return completion


    # Write the list of command line use in this session
    def do_history(self, line):
        """write in a file the suite of command that was used"""

        args = self.split_arg(line)

        if len(args) == 0:
            self.logger.info('\n'.join(self.history))
            return
        elif args[0] == 'clean':
            self.history = []
            self.logger.info('History is cleaned')
            return
        elif len(args)==1:
            if os.path.exists(args[0]):
                self.logger.error('The file ' + args[0] + ' already exists.' + \
                    ' Please chose another filename.')
                return
            else:
                file = open(args[0], 'w')
                file.write('\n'.join(self.history))
                file.close()
                self.logger.info('Command history written to the file ' + \
                    args[0] + '.')
                return
        else:
            self.logger.error("'history' takes either zero or one argument")
            return

    def help_help(self):
        self.logger.info("   Syntax: help [<command>]")
        self.logger.info("   Display the list of all available commands.");
        self.logger.info("   If a command is passed as an argument, its " + \
            "manual is displayed to the screen.")

    def help_history(self):
        self.logger.info("   Syntax: history [clean] ")
        self.logger.info("   Displays the history of the commands type-in by" +\
             "the user.")
        self.logger.info("   The option \"clean\" removes all entries from " + \
             "the history.")

    def do_shell(self, line):
        "run a shell command"
        if line.strip() is '':
            self.help_shell()
        else:
            self.logger.info("Running the shell command: " + line + ".")
            subprocess.call(line, shell=True)

    def help_shell(self):
        self.logger.info("   Syntax: shell <command> (or !CMD)")
        self.logger.info("   Runs the command CMD on a shell and retrieves " + \
             "the output.")

    def complete_history(self, text, line, begidx, endidx):
        "complete the history command"
        output = ["clean"]
        if text:
            output = [ f for f in output if f.startswith(text) ]
        return output

    def complete_shell(self, text, line, bgidx, endidx):
        """ add path for shell """
        if len(self.split_arg(line[0:bgidx]))>1 and line[bgidx-1]==os.path.sep:
            if not text:
                text = ''
            output = self.path_completion(text,
                base_dir=self.split_arg(line[0:bgidx])[-1])
        else:
            output = self.path_completion(text)
        return output

    @staticmethod
    def split_arg(line):
        """Split a line of arguments"""
        split = line.split()
        out=[]
        tmp=''
        for data in split:
            if data[-1] == '\\':
                tmp += data[:-1]+' '
            elif tmp:
                out.append(tmp+data)
            else:
                out.append(data)
        return out

