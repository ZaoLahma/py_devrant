class GUI:
    def show_menu(self, state):
        user_input = None
        if "MAIN_MENU" == state:
            self.print_logo()
            print("This is a completely unofficial Devrant (www.devrant.io) reader.")
            print("== COMMANDS ===========================================================================")
            print("view               - View most recent rants")
            print("view <no_of_rants> - View most recent rants, printing a maximum of 50 rants")            
            print("top <no_of_rants>  - View the top rated rants, returning at most 50 rants")
            print("surprise           - Get a random rant")
            print("search <term>      - Search for rant containing <term> returning a maximum of 20 rants")
            print("get <rant_id>      - Get a specific rant and its comments")
            print("r                  - Refresh/Repeat previous command")
            print("exit               - Exit program")
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
                print("\n------ Comments ------")
                for comment in rant.comments:
                    print(comment.text + " //" + comment.user)
                    print("-----------------------------------")
            print("--------------------------------------------------")
            
    def print_logo(self):
        print("==================================================") 
        print("###   ##### #    # #####  ####  #    # #######")
        print("#  #  #     #    # #   #  #  #  ##   #    #")
        print("#   # ####   #  #  ####  ###### # #  #    #")
        print("#  #  #      #  #  #  #  #    # #  # #    #")
        print("###   #####   ##   #   # #    # #    #    #")
        print("==================================================")    