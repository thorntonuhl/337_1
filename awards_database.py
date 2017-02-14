class awards_database(object):


    #Each award nominee is initialized with a 20% chance of winning

    def __init__ (self, award, nominees):

        inner_dict = {}
        outer_dict = {}

        for movie in nominees:

            inner_dict.update({movie: 0.2})

        outer_dict.update({award: inner_dict})

        self.all_awards = outer_dict
        
    #Add a new award category

    def add_category(self, award, nominees):

        new_add = {}

        for movie in nominees:

            new_add.update({movie: 0.2})

        self.all_awards.update({award: new_add})


    #Change the winning percentage of a given nominee within a given category

    def add_score(self, award, nominee, new_score):

        b = self.all_awards.get(award)
        if nominee in b:
            oldScore = b[nominee]
            b.update({nominee: oldScore + new_score})
        else:
            b.update({nominee: new_score})
        


    #Calculate the winner of each award based on 

    def find_winners(self):

        for each_award in self.all_awards:

            current_best = 0

            find_dict = self.all_awards.get(each_award)

            current_winner = ""

            for each_nominee in find_dict:

                nominee_score = find_dict.get(each_nominee)

                if (nominee_score > current_best):

                    current_best = nominee_score

                    current_winner = each_nominee
                    
            if (each_award != ""):

                print ("The winner of " + each_award + " was " + current_winner)

    def find_presenters(self):

        for each_award in self.all_awards:

            current_best = 0

            find_dict = self.all_awards.get(each_award)

            current_winner = ""

            for each_nominee in find_dict:

                nominee_score = find_dict.get(each_nominee)

                if (nominee_score > current_best):

                    current_best = nominee_score

                    current_winner = each_nominee

            if (current_winner != "") and (each_award != ""):

                print ("Presenter(s) of \"" + each_award + "\": " + current_winner)
