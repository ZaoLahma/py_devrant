import os

class GUI:
    def __init__(self):
        self.state = "MAIN_MENU"
        
    def show_menu(self, state):
        user_input = None
        if "MAIN_MENU" == state:
            #self.print_logo()
            print("====== MENU ======")
            print("top 1-50 - View the top rated rants")
            print("surprise - Get a random rant")
            print("view 1-50 - View most recent rants, printing a maximum of 50 rants")
            print("search <term> 1-50 - Search for rant containing <term> returning a maximum of 50 rants")
            print("get <rant_id> - Get a specific rant and its comments")
            print("r - Refresh/Repeat previous command")
            print("exit - Exit program")
            user_input = input("Command: ")
            
        return user_input
    
    def print_rants(self, rants):
        self.print_logo()   
        for rant in rants:
            print("Rant ID: " + rant.id)
            print("Comments: " + rant.num_comments + "\n")
            print(rant.text)
            print("\n/" + rant.user)
            if [] != rant.comments:
                print("====== Comments ======")
                for comment in rant.comments:
                    print(comment.text + " //" + comment.user)
                    print("-----------------------------------")
            print("===================================")
            
    def print_logo(self):
        print("==================================================") 
        print("###   ##### #    #  #####  ####  #    # #######")
        print("#  #  #     #    #  #   #  #  #  ##   #    #")
        print("#  #  ####   #  #   ####  ###### # #  #    #")
        print("#  #  #      #  #   #  #  #    # #  # #    #")
        print("###   ####    ##    #   # #    # #  # #    #")
        print("==================================================")     