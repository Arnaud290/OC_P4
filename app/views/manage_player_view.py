"""manage player view"""
from . import view
from ..controllers import manage_player_control


class ManagePlayerView(view.View):
    """Manage player view class"""
    def __call__(self):
        self.add_player_attributs = {}

    def display_players_table(self, player_list):
        """display record players table"""
        self.clear()
        print("Players List :\n\n")
        for player in player_list:
            print("id : {}, name : {} {}, rank : {}".format(
                                                        player.id,
                                                        player.first_name,
                                                        player.last_name,
                                                        player.rank
                                                        ))
            
    def add_player(self):
        """add player method"""
        print("\n\nNew player :\n\n")
        first_name = input("Enter first name: ").capitalize()
        last_name = input("Enter last name: ").capitalize()
        birth_date = input("Enter birth date (jj/mm//aaaa): ")
        while True:
            sex = input("Enter sex (M or F): ").upper()
            if sex in ('M', 'F'):
                break
            else: 
                print("\nEnter a correct value !\n")
        while True:        
            try:
                rank = abs(int(input("Enter rank: ")))
            except ValueError:
                print("\nEnter a number value !\n")
            else:
                break
        self.add_player_attributs = {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'birth_date': birth_date,
                                    'sex': sex,
                                    'rank': rank
                                    }
        return self.add_player_attributs

    def get_id_modify_player(self):
        player_id = (input("\n\nEnter id player or q for quit : ")).lower()
        return player_id
            
    def modify_player(self, player):
        modify_attribut = {}
        first_name = input("Change first name ? ({}): ".format(player.first_name)).capitalize()
        if first_name:
            modify_attribut = {'first_name': first_name}
        last_name = input("Change last name ? ({}): ".format(player.last_name)).capitalize()
        if last_name:
            modify_attribut = {'last_name': last_name}
        birth_date = input("Change birth date ? ({}): ".format(player.birth_date))
        if birth_date:
            modify_attribut = {'birth_date': birth_date}    
        while True:
            sex = input("change sex (M or F) ({}): ".format(player.sex)).upper()
            if sex:
                if sex in ('M', 'F'):
                    modify_attribut = {'sex': sex}
                    break
                else: 
                    print("\nEnter a correct value !\n")
            else:
                break
        while True:   
            rank = input("Change rank ? ({}): ".format(player.rank))
            if rank:
                try:
                    abs(int(rank))
                except ValueError:
                    print("\nEnter a number value !\n")
                    continue
                else:
                    modify_attribut = {'rank': rank}  
                    break
            else:
                break
        return modify_attribut