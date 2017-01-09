class GUI:
    def __init__(self):
        self.print_logo()
    def show_menu(self, state):
        print("This is a completely unofficial devRant (www.devrant.io) reader.")
        print("== COMMANDS ===========================================================================")
        print("sort <recent/algo> - Set algorithm for view command. Default is recent.")
        print("view               - View rants based on current sort setting")
        print("view <no_of_rants> - View rants, returning a maximum of 50 rants")            
        print("top <no_of_rants>  - View the top rated rants, returning at most 50 rants")
        print("surprise           - Get a random rant")
        print("search <term>      - Search for rant containing <term> returning a maximum of 20 rants")
        print("get <rant_id>      - Get a specific rant and its comments")
        print("n                  - Next page (where applicable)")
        print("b                  - Back (where applicable)")
        print("r                  - Refresh/Repeat previous command")
        print("exit               - Exit program")
        user_input = input("Command: ")
            
        return user_input
    
    def print_rants(self, rants, page):
        #self.print_logo()
        for rant in rants:
            print("--------------------------------------------------")
            print("Rant ID: " + rant.id)
            print("Score: " + rant.score)
            print("Comments: " + rant.num_comments + "\n")
            toPrint = []
            lineLength = 0
            for word in rant.text.split(' '):
                if lineLength + len(word) + 1 < 100:
                    toPrint.append(word + " ")
                    lineLength += len(word) + 1
                else:
                    print(''.join(toPrint))
                    toPrint = []
                    toPrint.append(word + " ")
                    lineLength = len(word) + 1
            print(''.join(toPrint))
            toPrint = []
            print("\n/" + rant.user)
            if [] != rant.comments:
                print("\n------ Comments ------")
                for comment in rant.comments:
                    print(comment.text + " //" + comment.user)
                    print("-----------------------------------")          
        print("--------------------------------------------------")
        print("Current page: " + str(page) + "\n")   
            
    def print_logo(self):
        print("==================================================") 
        print("###   ##### #    # #####  ####  #    # #######")
        print("#  #  #     #    # #   #  #  #  ##   #    #")
        print("#   # ####   #  #  ####  ###### # #  #    #")
        print("#  #  #      #  #  #  #  #    # #  # #    #")
        print("###   #####   ##   #   # #    # #    #    #")
        print("==================================================")    
