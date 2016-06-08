from web_parser import WebParser
from gui import GUI
import re

class DevRantManager:
    __ADDRESS_BASE = "/api/devrant/"
    def __init__(self):
        self.state = "NO_STATE"
        self.gui = GUI()
        self.web_parser = WebParser("www.devrant.io")
        self.curr_command = None
        self.prev_command = None
        self.page = 0
        self.curr_limit = 0
        
    def start(self):
        running = True
        while running == True:
            user_input = self.gui.show_menu("MAIN_MENU")
            if "b" != user_input:
                self.prev_command = self.curr_command
            self.curr_command = self.__handle_input(user_input)
            #if None != self.prev_command and self.curr_command != None:
            #    print("curr_command: " + self.curr_command + "prev_command: " + self.prev_command)
            if user_input == "exit":
                running = False
                
    def __handle_input(self, user_input):
        rants = None
        command = None
        address = None
        if user_input == "r":
            if None != self.curr_command:
                self.__handle_input(self.curr_command)
            return self.curr_command
        if user_input == "n":
            if None != self.curr_command:
                self.page += self.curr_limit
                self.__handle_input(self.curr_command)
            return self.curr_command
        if user_input == "b":
            if None != self.prev_command:
                if self.page - self.curr_limit >= 0:
                    self.page -= self.curr_limit                
                self.__handle_input(self.prev_command)
            return self.prev_command
        match_obj = re.match('surprise', user_input)
        if match_obj:
            self.state = "SURPRISE"
            address = DevRantManager.__ADDRESS_BASE + "rants/" + match_obj.group(0)
            command = {'app' : 3}        
        match_obj = re.match('get (.*)', user_input)
        if match_obj:            
            address = DevRantManager.__ADDRESS_BASE + "rants/" + match_obj.group(1)
            command = {'app' : 3} 
        match_obj = re.match('top (.*)', user_input)
        if match_obj:
            if self.state != "TOP":
                self.page = 0            
            self.state = "TOP"
            address = DevRantManager.__ADDRESS_BASE + "rants"
            self.curr_limit = int(match_obj.group(1))
            command = {'app' : 3, 'sort' : 'top', 'limit' : match_obj.group(1), 'skip' : self.page}   
        match_obj = re.match('view (.*)', user_input)
        if match_obj:
            if self.state != "VIEW":
                self.page = 0            
            self.state = "VIEW"
            address = DevRantManager.__ADDRESS_BASE + "rants"
            self.curr_limit = int(match_obj.group(1))
            command = {'app' : 3, 'sort' : 'recent', 'limit' : match_obj.group(1), 'skip' : self.page}
        else:
            match_obj = re.match('view', user_input)
            if match_obj:
                if self.state != "VIEW":
                    self.page = 0
                self.state = "VIEW"
                self.curr_limit = 20
                address = DevRantManager.__ADDRESS_BASE + "rants"
                command = {'app' : 3, 'sort' : 'recent', 'skip' : self.page}  
        match_obj = re.match('search (.*)', user_input)
        if match_obj:
            if self.state != "SEARCH":
                self.page = 0             
            self.state = "SEARCH"
            self.curr_limit = 20
            address = DevRantManager.__ADDRESS_BASE + "search"
            command = {'app' : 3, 'term' : match_obj.group(1), 'skip' : self.page}
            
        if None != command and None != address:
            rants = self.web_parser.execute_command(address, command)
        else:
            user_input = self.curr_command
        if None != rants:
            self.gui.print_rants(rants)
        return user_input