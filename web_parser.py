from http.client import HTTPSConnection
import urllib.parse
import re

class Comment:
    def __init__(self):
        self.text = ""
        self.user = ""
        
class Rant:
    def __init__(self):
        self.id = -1
        self.text = ""
        self.user = ""
        self.score = '0'
        self.num_comments = '0'
        self.comments = []

class WebParser():
    def __init__(self, address):
        self.connection = None
        self.address = address
        
    def execute_command(self, address, command):
        self.connection = HTTPSConnection(self.address)        
        encoded_command = address
        if None != command: 
            encoded_command = encoded_command + "?" + urllib.parse.urlencode(command)
        self.connection.request("GET", encoded_command)
        response = self.connection.getresponse()
        if 200 == response.status:
            raw_rants = response.read()
            #print(raw_rants)
            return self.__parse_entries(raw_rants)
        else:
            print("Failed to fetch rant entries. Status: " + str(response.status) + ". Go rant about it.")
            return None
     
    def __parse_entries(self, raw_rants): 
        parsed_rants = re.findall('\"rants\":(.*?)}\]', str(raw_rants), re.S)
        if [] != parsed_rants:
            return self.__extract_rants(parsed_rants)
        
        else:
            parsed_rant = re.findall('\"rant\":(.*?)\],\"success\":true}', str(raw_rants), re.S)
            comments = re.findall('\"body\":\"(.*?)\",\"(.*?)\"user_username\":\"(.*?)\",\"', str(parsed_rant), re.S)
            rant = self.__extract_rants(parsed_rant)  
            for raw_comment in comments:
                comment = Comment()
                comment.text = self.__cleanup_rant_text(raw_comment[0])
                comment.user = raw_comment[2]
                rant[0].comments.append(comment)
            
            return rant
    
    def __extract_rants(self, parsed_rants):
        parsed_rants = re.findall('\"id\":(\d+)(.*?)\"text\":\"(.*?)\",(.*?)\"score\":(\d+)(.*?)\"num_comments\":(\d+)(.*?)\"user_username\":\"(.*?)\",(.*?)\"user_score\":(\d+)', str(parsed_rants), re.S)
        
        rants = []
        for parsed_rant in parsed_rants:
            rant = Rant()
            rant.id = parsed_rant[0]
            rant.text = self.__cleanup_rant_text(parsed_rant[2])
            rant.score = parsed_rant[4]
            rant.user = parsed_rant[8]
            rant.num_comments = parsed_rant[6]
            rants.append(rant)
        return rants       
    
    def __cleanup_rant_text(self, text):
        text = text.replace("\\n", "\n")
        text = text.replace("\\r", "\n")
        text = text.replace("\\", "")
        text = text.replace("\\\\", "")
        text = text.replace("ud83dude2c", " :O")
        text = text.replace("ud83dude03", " :D")
        text = text.replace("ud83dude02", " ;D")
        text = text.replace("ud83dudc4d", " <tup>")
        text = text.replace("ud83dudd95", " <finger>")
        text = text.replace("ud83dude4c", " <clap>")
        text = text.replace("ud83cudffc", " ':D")
        text = text.replace("ud83dude05", "")
        text = text.replace("ud83dude12", " :/")
        text = text.replace("ud83dude1c", " :P")
        text = text.replace("ud83dude10", " :|")
        text = text.replace("ud83dudc4f", " <clap>")
        text = text.replace("ud83dude01", " >.<")
        text = text.replace("ud83dudc81", "")
        text = text.replace("ud83cudffd", "")
        text = text.replace("ud83dude44", " <rolleyes>")
        text = text.replace("ud83dude13", " ':(")
        text = text.replace("ud83dude00", " :D")
        text = text.replace("ud83dude48", " <shame>")
        text = text.replace("ud83dude20", " >:(")
        text = text.replace("ud83dude11", " :|")
        text = text.replace("ud83dude23", " >.<")
        text = text.replace("ud83dude27", " :O")
        text = text.replace("ud83dude07", " <halo>")
        text = text.replace("ud83dude0e", " <cool>")
        text = text.replace("ud83dude06", " xD")
        text = text.replace("ud83eudd14", " <thinking>")
        text = text.replace("u263aufe0f", " :)")
        text = text.replace("codeu2026", " ...")
        text = text.replace("ud83dude0a", " ^_^")
        text = text.replace("ud83dudd2b", " <shoot me>")
        text = text.replace("ud83dude41", " :(")
        text = text.replace("ud83dude21", ">:(")
        text = text.replace("ud83dudc4c", "")
        text = text.replace("ud83dudd5b", "")
        return text