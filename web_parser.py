from http.client import HTTPSConnection
import urllib.parse
import re

class Comment:
    def __init__(self):
        self.text = ""
        self.user = ""

class WebParser():
    def __init__(self, address):
        self.connection = HTTPSConnection(address)
        
    def execute_command(self, address, command):
        encoded_command = address
        if None != command: 
            encoded_command = encoded_command + "?" + urllib.parse.urlencode(command)
        print(encoded_command)
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
        rants_comments = re.findall('comments\"(.*?)}]', str(raw_rants), re.S)
        
        index = 0
        rants = []
        for rant_id in rants_ids:
            rants.append([rant_id, rants_text[index], rants_users[index], rants_comments])
            index += 1
        
        for rant in rants:
            rant[1] = rant[1].replace("\\n", "\n")
            rant[1] = rant[1].replace("\\r", "\n")
            rant[1] = rant[1].replace("\\", "")
        
            if None != rant[3]:
                print("processing comments")
                comments = []
                for raw_comment in rant[3]:
                    raw_comment_text = re.findall('body\":\"(.*?)\",', str(raw_comment), re.S)
                    raw_comment_user = re.findall('username\":\"(.*?)\",', str(raw_comment), re.S)
                    index = 1
                    for comment_text in raw_comment_text:
                        #print("Raw comment " + raw_comment_text)
                        comment_text = comment_text.replace("\\n", "\n")
                        comment_text = comment_text.replace("\\r", "\n")
                        comment_text = comment_text.replace("\\", "")
                        comment_text = comment_text.replace("\\\\", "")
                        comment = Comment()
                        comment.text = comment_text
                        comment.user = raw_comment_user[index]
                        print("Processed comment: " + comment.text + " user: " + comment.user)
                        comments.append(comment)
                        index += 1
                rant[3] = comments
            
        return rants