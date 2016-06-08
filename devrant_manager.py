from web_parser import WebParser
from gui import GUI
import re

class DevRantManager:
    __ADDRESS_BASE = "/api/devrant/"
    def __init__(self):
        self.gui = GUI()
        self.web_parser = WebParser("www.devrant.io")
        
    def start(self):
        running = True
        rants = None
        while running == True:
            user_input = self.gui.show_menu("MAIN_MENU")
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
            if user_input == "exit":
                running = False
            if None != rants:
                self.gui.print_rants(rants)             