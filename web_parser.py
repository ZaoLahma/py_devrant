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
        self.num_comments = 0
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
        #print(encoded_command)
        self.connection.request("GET", encoded_command)
        response = self.connection.getresponse()
        if 200 == response.status:
            raw_rants = response.read()
            return self.__parse_entries(raw_rants)
        else:
            print("Failed to fetch rant entries. Status: " + str(response.status) + ". Go rant about it.")
            return None
        
    def __parse_entries(self, raw_rants):
        #In serious need of refactoring
        rants_text = re.findall('text\":\"(.*?)\",', str(raw_rants), re.S)
        rants_ids = re.findall('\"id\":(.*?),\"text\":', str(raw_rants), re.S)
        rants_users = re.findall('user_username\":\"(.*?)\",\"user_score\"', str(raw_rants), re.S)
        rants_comments = re.findall(',\"comments\"(.*?)}]', str(raw_rants), re.S)
        rants_num_comments = re.findall('num_comments\":(.*?),', str(raw_rants), re.S)
        index = 0
        rants = []
        rant = None
        for rant_id in rants_ids:
            rant = Rant()
            rant.id = rant_id
            rant.text = self.__cleanup_rant_text(rants_text[index])
            rant.user = rants_users[index]
            rant.num_comments = rants_num_comments[index]
            rant.comments = rants_comments
            rants.append(rant)
            index += 1
        
        for rant in rants:
            if None != rant.comments:
                comments = []
                for raw_comment in rant.comments:
                    raw_comment_text = re.findall('body\":\"(.*?)\",', str(raw_comment), re.S)
                    raw_comment_user = re.findall('username\":\"(.*?)\",', str(raw_comment), re.S)
                    index = 0
                    for comment_text in raw_comment_text:
                        #print("Raw comment " + raw_comment_text)
                        comment_text = self.__cleanup_rant_text(comment_text)
                        comment = Comment()
                        comment.text = comment_text
                        comment.user = raw_comment_user[index]
                        comments.append(comment)
                        index += 1
                rant.comments = comments
            
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
        text = text.replace("u263a", " :)")
        text = text.replace("codeu2026", " ...")
        return text