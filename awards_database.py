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

    def change_score(self, award, nominee, new_score):

        b = self.all_awards.get(award)

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

            print ("The winner of " + each_award + " was " + current_winner)
 
#TEST SECTION

golden_globes = awards_database("Best Picture", ["Moonlight", "Hell or High Water", "Lion", "Manchester by the Sea", "Hacksaw Ridge"])

golden_globes.change_score("Best Picture", "Moonlight", 0.5)

golden_globes.add_category("Best Director", ["Damien Chazelle", "Tom Ford", "Mel Gibson", "Barry Jenkins", "Kenneth Lonergan"])

golden_globes.change_score("Best Director", "Damien Chazelle", 0.21)

golden_globes.find_winners()
