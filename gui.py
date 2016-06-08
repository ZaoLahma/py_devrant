import os

class GUI:
    def __init__(self):
        self.state = "MAIN_MENU"
        
    def show_menu(self, state):
        user_input = None
        if "MAIN_MENU" == state:
            self.print_logo()
            print("top 1-50 - View the top rated rants")
            print("view 1-50 - View most recent rants, printing a maximum of 50 rants")
            print("search <term> 1-50 - Search for rant containing <term> returning a maximum of 50 rants")
            print("get <rant_id> - Get a specific rant and its comments")
            print("exit - Exit program")
            user_input = input("Command: ")
            
        return user_input
    
    def print_rants(self, rants):
        self.print_logo()   
        print("No of rants returned: " + str(len(rants)))
        for rant in rants:
            print("================= RANT: " + rant[0] + " ==================")
            print(rant[1])
            print("\n/" + rant[2])
            if None != rant[3]:
                print("====== Comments ======")
                for comment in rant[3]:
                    print(comment.text + " //" + comment.user)
                    print("-----------------------------------")
            print("================= END ==================")
            
    def print_logo(self):
        print("###   ##### #    #  #####  ####  #    # ####### ######")
        print("#  #  #     #    #  #   #  #  #  ##   #    #    #")
        print("#  #  ####   #  #   ####  ###### # #  #    #    ####")
        print("#  #  #      #  #   #  #  #    # #  # #    #        #")
        print("###   ####    ##    #   # #    # #  # #    #   #####")
        print("========================================================")     