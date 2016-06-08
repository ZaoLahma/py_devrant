from web_parser import WebParser
from gui import GUI
import re

class DevRantManager:
    __ADDRESS_BASE = "/api/devrant/"
    def __init__(self):
        self.gui = GUI()
        self.web_parser = WebParser("www.devrant.io")
        self.prev_command = None
        
    def start(self):
        running = True
        while running == True:
            user_input = self.gui.show_menu("MAIN_MENU")
            self.prev_command = self.__handle_input(user_input)
            if user_input == "exit":
                running = False
                
    def __handle_input(self, user_input):
        rants = None
        if user_input == "r":
            if None != self.prev_command:
                self.__handle_input(self.prev_command)
            return self.prev_command
        match_obj = re.match('surprise', user_input)
        if match_obj:
            address = DevRantManager.__ADDRESS_BASE + "rants/" + match_obj.group(0)
            command = {'app' : 3}
            rants = self.web_parser.execute_command(address, command)         
        match_obj = re.match('get (.*)', user_input)
        if match_obj:
            address = DevRantManager.__ADDRESS_BASE + "rants/" + match_obj.group(1)
            command = {'app' : 3}
            rants = self.web_parser.execute_command(address, command)   
        match_obj = re.match('top (.*)', user_input)
        if match_obj:
            address = DevRantManager.__ADDRESS_BASE + "rants"
            command = {'app' : 3, 'sort' : 'top', 'limit' : match_obj.group(1)}
            rants = self.web_parser.execute_command(address, command)    
        match_obj = re.match('view (.*)', user_input)
        if match_obj:
            address = DevRantManager.__ADDRESS_BASE + "rants"
            command = {'app' : 3, 'sort' : 'recent', 'limit' : match_obj.group(1)}
            rants = self.web_parser.execute_command(address, command)
        else:
            match_obj = re.match('view', user_input)
            if match_obj:
                address = DevRantManager.__ADDRESS_BASE + "rants"
                command = {'app' : 3, 'sort' : 'recent'}
                rants = self.web_parser.execute_command(address, command)    
        match_obj = re.match('search (.*) (.*)', user_input)
        if match_obj:
            address = DevRantManager.__ADDRESS_BASE + "search"
            print("Search term: " + str(match_obj.group(1)))
            command = {'app' : 3, 'term' : match_obj.group(1), 'limit' : match_obj.group(2)}
            rants = self.web_parser.execute_command(address, command)
        match_obj = re.match('search (.*)', user_input)
        if match_obj:
            address = DevRantManager.__ADDRESS_BASE + "search"
            print("Search term: " + str(match_obj.group(1)))
            command = {'app' : 3, 'term' : match_obj.group(1)}
            rants = self.web_parser.execute_command(address, command)
        if None != rants:
            self.gui.print_rants(rants)
        return user_input