from gui import GUI
from web_parser import WebParser
import re

class InputHandler:
    __ADDRESS_BASE = "/api/devrant/"
    def __init__(self):
        self.gui = GUI()
        self.web_parser = WebParser("www.devrant.io")
        self.executed_commands = []
        self.page = 0
        self.limit = 20
        self.sort = "recent"
        self.state = "NO_STATE"
        
    def handle_input(self):
        running = True
        while(running == True):
            user_input = self.gui.show_menu("NO_STATE")
            if 'exit' == user_input:
                return
            command = self.get_command(user_input)
            if command[0] == True:
                if 'r' != user_input and 'b' != user_input and 'n' != user_input:
                    self.executed_commands.append(user_input)
                rants = self.web_parser.execute_command(command[1], command[2])
                if None != rants:
                    self.gui.print_rants(rants, int(self.page / self.limit))
            
    def get_command(self, user_input):
        retval = [False, None, None]
        if 'r' == user_input:
            if len(self.executed_commands) > 0:
                return self.get_command(self.executed_commands[-1])
        if 'b' == user_input:
            if len(self.executed_commands) > 0:
                if self.page - self.limit >= 0 and True == self.__pageState(self.state):
                    self.page -= self.limit
                elif len(self.executed_commands) > 1:
                    self.executed_commands.pop()
                return self.get_command(self.executed_commands[-1])
        if 'n' == user_input:
            if len(self.executed_commands) > 0:
                self.page += self.limit
                return self.get_command(self.executed_commands[-1])
        if 'surprise' == user_input:
            self.__set_state("SURPRISE")
            retval[1] = InputHandler.__ADDRESS_BASE + "rants/" + user_input
            retval[2] = {'app' : 3}
            retval[0] = True
        res = re.match('sort(\s)(algo|recent)', user_input)
        if res:
            self.sort = res.group(2)
            self.page = 0
        res = re.match('view(\s)(\d+)', user_input)
        if res:
            self.__set_state("VIEW")
            self.limit = int(res.group(2))
            retval[1] = InputHandler.__ADDRESS_BASE + "rants"
            retval[2] = {'app' : 3, 'sort' : self.sort, 'limit' : self.limit, 'skip' : self.page}
            retval[0] = True
        else:
            res = re.match('view', user_input)
            if res:
                self.__set_state("VIEW")
                self.limit = 20
                retval[1] = InputHandler.__ADDRESS_BASE + "rants"
                retval[2] = {'app' : 3, 'sort' : self.sort, 'limit' : self.limit, 'skip' : self.page}
                retval[0] = True
        res = re.match('search(\s)(.*)', user_input)
        if res:
            self.__set_state("SEARCH")
            retval[1] = InputHandler.__ADDRESS_BASE + "search"
            retval[2] = {'app' : 3, 'term' : res.group(2), 'skip' : self.page}
            retval[0] = True   
        res = re.match('top(\s)(\d+)', user_input)
        if res:
            self.__set_state("TOP")
            self.limit = int(res.group(2))
            retval[1] = InputHandler.__ADDRESS_BASE + "rants"
            retval[2] = {'app' : 3, 'sort' : 'top', 'limit' : self.limit, 'skip' : self.page}
            retval[0] = True
        res = re.match('get(\s)(\d+)', user_input)
        if res:
            self.__set_state("GET")
            retval[1] = InputHandler.__ADDRESS_BASE + "rants/" + res.group(2)
            retval[2] = {'app' : 3}
            retval[0] = True            
        return retval
    
    def __set_state(self, state):
        if self.state != state:
            if self.__pageState(state) and self.__pageState(self.state):
                self.page = 0
                self.limit = 20
        self.state = state
        
    def __pageState(self, state):
        if state == "VIEW" or state == "TOP" or state == "SEARCH":
            return True
     
        return False