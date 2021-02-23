import webbrowser
from os import system, name
from random import shuffle, randint, choice
import sys
import copy

class Player:
    """ Parent class for all players in the game. """
    def __init__(self, name):
        self.name = name
        self.status = "active"
        self.hand = []
        self.table = []
        self.table_sum = 0
        self.tokens = 0

    def draw(self, deck):
        """ Draw a card from the deck. """
        self.hand.append(deck.draw())

    def play(self, card_name):
        """ Play a card from a player's hand onto their table. """
        for item in self.hand:
            if item.name == card_name:
                print(f"{self.name} played {card_name}.")
                self.hand.remove(item)
                self.table.append(item)
                self.table_sum += item.value
                return item

    def discard(self, card):
        """ Discard card from hand. """
        for item in self.hand:
            if item.name == card.name:
                self.hand.remove(item)
                return

    def reset(self):
        """ Resets attributes to beginning of round values. """
        self.status = "active"
        self.hand = []
        self.table = []
        self.table_sum = 0

    def __repr__(self):
        """ Displays hand and player name when player called. """
        hand_table = f"Player: {self.name}\nHand: "
        for item in self.hand:
            hand_table = hand_table + item.name +" "
        hand_table += "\nOn Table: "
        for item in self.table:
            hand_table = hand_table + item.name +" "
        hand_table +=f"\nStatus: {self.status}\n"
        hand_table +=f"Tokens: {self.tokens}\n"
        return hand_table

class User(Player):
    """ Class for human user. """
    def __init__(self, name):
        super().__init__(name)

    def cont_play():
        """
        Prompt user to continue.
        Opens website for help and allows user to quit program or return to
        start screen.
        """
        cont = input(
                     "Press Enter to continue, q for quit, or h for help. "
                     ).strip()
        if cont.lower() == 'h':
            print("Opening game manual in browser.")
            webbrowser.open(
            "https://loveletteremulator.weebly.com/game-rules-and-story.html")
            User.cont_play()
        elif cont.lower() == "q":
            stat = input("Press Enter to restart and q to exit the program. ")
            if stat.lower() == 'q':
                print("Thanks for playing.")
                sys.exit()
            GameEngine.home()
        return

    def play_user(self, game_players, player_dict, deck):
        """
        User turn management.
        Ensures that user follows rules and collect user input.
        """
        #Get from user which card to play.
        while True:
            play_card = input(
                              "Which card would you like to play? "
                              ).capitalize().strip()
            cards_in_hand = [card.name for card in self.hand]
            #Check to make sure card is in hand. And player is following rules.
            if play_card not in [card.name for card in self.hand]:
                print("You don't have that card!")
            elif (
                   "Countess" in cards_in_hand
                   and ("Prince" in cards_in_hand or "King" in cards_in_hand)
                   and play_card != "Countess"
            ):
                print("Countess in hand with Prince or King.",
                      "You must play the Countess.")
                User.cont_play()
                card = self.play("Countess")
                break
            else:
                card = self.play(play_card)
                break
        #Manage play actions of different cards.
        #Check there are unprotected active players.
        #If there are no unprotected players put card on table take no actions.
        playable_players = [player for player in game_players
                            if player.status == "active"]
        if len(playable_players) == 0:
                print("You can't play a card against any player.",
                      "Your card is played directly to table.")
                User.cont_play()
                return
        if len(playable_players) ==1 and playable_players[0]==self:
            if play_card == "Prince":
                pass
            else:
                print("You can't play a card against any player.",
                      "Your card is played directly to table.")
                User.cont_play()
                return
        elif card.name in ["Princess", "Handmaid", "Countess"]:
            card.action(self)
        else:
            #Get from user who they would like to use card against.
            while True:
                player2 = input(
                                "Who do you want to play this card against? "
                                ).capitalize().strip()
                try:
                    player2 = player_dict[player2]
                    #Check valid player selected.
                    if player2 == self and card.name!="Prince":
                        print(f"You can't play {card.name} on yourself.",
                              "Choose another player:")
                        for player in playable_players:
                            if player.name != self.name:
                                print(player.name)
                        print()
                        continue
                    elif player2.status in ["protected", "eliminated"]:
                        if card.name != "Prince":
                            print(f"{player2.name} is {player2.status}.",
                                  "Choose another player from:")
                            for player in playable_players:
                                if player.name != self.name:
                                    print(player.name)
                            print()
                        else:
                            print(f"{player2.name} is {player2.status}.",
                                  "Choose another player:")
                            for player in playable_players:
                                print(player.name)
                            print()
                    else:
                        break
                except:
                    print("Not a valid player. Choose from:")
                    for player in playable_players:
                        print(player.name)
                    User.cont_play()
            print()
            #Perform the card's action.
            if card.name in ["Prince"]:
                card.action(player2, deck)
            elif card.name in ["Priest","Baron", "King"]:
                card.action(self,player2)
            elif card.name == "Guard":
                while True:
                    guess = input(
                                   "Which card would you like to guess?"\
                                   " (Enter h for help.) "
                                   ).capitalize().strip()
                    if guess in ["Priest", "Baron", "Handmaid", "Prince",
                                 "King", "Countess", "Princess"]:
                        break
                    if guess.lower() == "h":
                        print("In the deck there are 5 Guards, 2 Priests,",
                              " 2 Barons , 2 Handmaids, 2 Prince,",
                                "1 King, 1 Countess, and 1 Princess.",
                                "\nYou can not guess Guard.\n")
                    else:
                        print("Not a valid guess.",
                        "Remember you can't guess Guard!")
                        print("You can guess Priest, Baron, Handmaid, Prince,",
                                "King, Countess, or Princess.\n")
                card.action(player2,guess)
            return

    def __repr__(self):
        """ Displays hand and player name when player called."""
        hand_table = f"Player: {self.name}\n"
        hand_table += "On Table: "
        for item in self.table:
            hand_table = hand_table + item.name +" "
        hand_table +=f"\nStatus: {self.status}\n"
        hand_table +=f"Tokens: {self.tokens}\n"
        hand_table += "Your Hand:\n"
        for item in self.hand:
            hand_table = hand_table +"\t"+ item.name +": " +item.card_text+"\n"
        return hand_table

class NPC(Player):
    """ Class for computer controlled players. """
    def __init__(self, name, level="easy"):
        super().__init__(name)
        self.knowledge = ["Guard"]*5+["Priest","Baron","Handmaid","Prince"]*2+\
                         ["King", "Countess", "Princess"]
        self.level = level

    def reset(self):
        """ Reset NPC attributes to beginning of round values."""
        super().reset()

    def play_level(self,game_players,deck):
        """ Controls autoplay actions for NPCs. """
        cards_in_hand = [card.name for card in self.hand]
        guess_names = ["Priest", "Baron", "Handmaid", "Prince", "King",
                   "Countess", "Princess"]
        #If Countess in hand and Prince or King must discard Countess.
        if(
            "Countess" in cards_in_hand
            and ("Prince" in cards_in_hand or "King" in cards_in_hand)
        ):
            if self.hand[0].name =="Countess":
                play_card = self.hand[0]
            else:
                play_card = self.hand[1]
            self.play(play_card.name)
            play_card.action(self)
        else:
            #Picks card at random if level is easy.
            #Keeps highest card if level is medium or hard.
            if self.level == "easy":
                play_card = choice(self.hand)
            else:
                play_card = self.smart_card()
            self.play(play_card.name)
            #Check that card can be played against anyone.
            playable_players = [player for player in game_players
                                if player.status == "active"]
            if len(playable_players) == 0:
                print(f"{self.name} can't play a card against any player.",
                "Card played directly to table.")
                return
            if len(playable_players) ==1 and playable_players[0]==self:
                if play_card.name == "Prince":
                    pass
                else:
                    print(f"{self.name} can't play a card against any player.",
                    "Card played directly to table.")
                    return
            #Play card.
            if play_card.name in ["Princess", "Handmaid", "Countess"]:
                play_card.action(self)
            else:
                #Choose player to play card against. Validate player choice.
                while True:
                    player2 = choice(playable_players)
                    if player2.status == "active":
                        break
                while play_card.name != "Prince" and player2 == self:
                    player2 = choice(playable_players)
                #Play card with correct arguments
                if play_card.name == "Prince":
                    play_card.action(player2, deck)
                elif play_card.name in ["Priest","Baron", "King"]:
                    play_card.action(self,player2)
                elif play_card.name == "Guard":
                    #Random guess if level is not hard.
                    #If level is hard guesses only from remaining cards.
                    if self.level in ["easy", "medium"]:
                        guess = choice(guess_names)
                    else:
                        #Look at all played cards
                        potential_guesses = copy.deepcopy(self.knowledge)
                        for player in game_players:
                            for item in player.table:
                                potential_guesses.remove(item.name)
                        #Include card in hand.
                        potential_guesses.remove(self.hand[0].name)
                        #Remove any left over guards.
                        while True:
                            try:
                                potential_guesses.remove("Guard")
                            except:
                                break
                        guess = choice(potential_guesses)
                    play_card.action(player2,guess)
        return

    def smart_card(self):
        """Finds lowest value card in hand and returns that card object."""
        if self.hand[0].value<self.hand[1].value:
            play_card = self.hand[0]
        else:
            play_card = self.hand[1]
        return play_card

    def __repr__(self):
        """" Displays table and player name when player called. """
        hand_table = f"Player: {self.name}"
        hand_table += "\nOn Table: "
        for item in self.table:
            hand_table = hand_table + item.name +" "
        hand_table +=f"\nStatus: {self.status}\n"
        hand_table +=f"Tokens: {self.tokens}\n"
        return hand_table

class Card:
    """ Parent class for cards. """
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Guard(Card):
    """Creates the Guard card and controls its action in game play."""
    def __init__(self, name = "Guard", value = 1 ):
        super().__init__(name, value)
        self.card_text = "Name a non-Guard card and choose another player. "\
                          "If that player has that card, he or she is out of "\
                          "the round"

    def action(self, player2, guess):
        """ Implements card's specific action. Narrates action to user. """
        guess = guess.capitalize()
        print(f"Guessing {player2.name}'s hand is {guess}.")
        if guess == player2.hand[0].name:
            print(f"{player2.name} had a {guess}!",
                  f"\n{player2.name} is eliminated")
            player2.status = "eliminated"
        else:
            print(f"{player2.name} did not have a {guess}.")

class Priest(Card):
    """Creates the Priest card and controls its action in game play."""
    def __init__(self, name = "Priest", value = 2 ):
        super().__init__(name, value)
        self.card_text = "Look at another player's hand."

    def action(self,player1, player2):
        """ Implements card's specific action. Narrates action to user. """
        print(f"{player1.name} looks at {player2.name}'s hand.")
        if isinstance(player1,NPC):
            pass
        else:
            print(f"{player2.name} shows you their hand.")
            for item in player2.hand:
                print(f"{item.name}: {item.card_text}")

class Baron(Card):
    """Creates the Baron card and controls its action in game play."""
    def __init__(self, name = "Baron", value = 3 ):
        super().__init__(name, value)
        self.card_text = "You and another player secretly compare hands. The "\
                         "player with the lower value is out of the round."

    def action(self, player1, player2):
        """ Implements card's specific action. Narrates action to user. """
        print(f"{player1.name} comparing hands with {player2.name}.")
        if player1.hand[0].value > player2.hand[0].value:
            print(f"{player2.name} had the lower card and was eliminated.")
            print(f"{player2.name} had a {player2.hand[0].name}.")
            player2.status = "eliminated"
        elif player1.hand[0].value < player2.hand[0].value:
            print(f"{player1.name} had the lower card and was eliminated.")
            print(f"{player1.name} had a {player1.hand[0].name}.")
            player1.status = "eliminated"
        else:
            print(f"No one eliminated!")
        return player2.hand[0].name

class Handmaid(Card):
    """Creates the Handmaid card and controls its action in game play."""
    def __init__(self, name = "Handmaid", value = 4 ):
        super().__init__(name, value)
        self.card_text = "Until your next turn, ignore all effects from "\
                            "other players' cards."

    def action(self, player):
        """ Implements card's specific action. Narrates action to user. """
        print(f"{player.name} is now protected till their next turn.")
        player.status = "protected"

class Prince(Card):
    """Creates the Prince card and controls its action in game play."""
    def __init__(self, name = "Prince", value = 5 ):
        super().__init__(name, value)
        self.card_text = "Choose any player (including yourself) to discard "\
                          "his or her hand and draw a new card."

    def action(self, player2,deck):
        """ Implements card's specific action. Narrates action to user. """
        print(f"{player2.name} must discard their hand.")
        if player2.hand[0].name == "Princess":
            print(f"{player2.name} had the Princess and is eliminated.")
            player2.status = "eliminated"
        else:
            print(f"{player2.name} discarded and drew a new card.")
            player2.discard(player2.hand[0])
            if len(deck.deck)==0:
                print("No cards left!\n\n")
                player2.status = "eliminated"
            else:
                player2.draw(deck)

class King(Card):
    """Creates the King card and controls its action in game play."""
    def __init__(self, name = "King", value = 6 ):
        super().__init__(name, value)
        self.card_text = "Trade hands with another player of your choice."

    def action(self,player1, player2):
        """ Implements card's specific action. Narrates action to user. """
        print(f"{player1.name} and {player2.name} switched hands.")
        player1.hand, player2.hand = player2.hand, player1.hand

class Countess(Card):
    """Creates the Countess card and controls its action in game play."""
    def __init__(self, name = "Countess", value = 7 ):
        super().__init__(name, value)
        self.card_text = "If you have this card and the King or Prince in "\
                            "your hand, you must discard this card."
    def action(self,player):
        """ Implements card's specific action. """
        pass

class Princess(Card):
    """Creates the Princess card and controls its action in game play."""
    def __init__(self, name = "Princess", value = 8 ):
        super().__init__(name, value)
        self.card_text = "If you discard this card you are out of the round."

    def action(self, player):
        """ Implements card's specific action. Narrates action to user. """
        print(f"{player.name} discarded the princess and is eliminated.")
        player.status = "eliminated"

class Deck():
    """ Love Letter deck. Build, shuffle, and draw from deck. """
    def __init__(self):
        self.deck = []
        self.build_deck()

    def build_deck(self):
        """ Builds Love Letter deck with card objects. """
        for i in range(5):
            self.deck.append(Guard())
        for i in range(2):
            x = [Priest(), Baron(), Handmaid(), Prince()]
            self.deck.extend(x)
        for y in [King(), Countess(), Princess()]:
            self.deck.append(y)

    def shuffle(self):
        """ Shuffles deck. """
        shuffle(self.deck)

    def draw(self):
        """ Draw a single card from the deck. """
        return self.deck.pop()

    def __str__(self):
        deck_str = ""
        for item in self.deck:
            deck_str = deck_str + item.name +", "
        return deck_str

class GameEngine():
    """ Main control class. Manages full game play. """
    def __init__(self, name, num_players, level):
        self.players = [User(name)]
        self.level = level
        NPC_names = ["Guido", "Ewa", "Kevin"]
        for i in range(num_players-1):
            self.players.append(NPC(NPC_names[i],self.level))
        self.player_dict = {player.name:player for player in self.players}
        self.game_deck = Deck()
        self.game_deck.shuffle()
        self.removed_cards = []
        self.start()

    def reset(self):
        """ Resets game deck and removed_cards. Shuffles new deck."""
        self.game_deck = Deck()
        self.game_deck.shuffle()
        self.removed_cards = []

    def deal(self):
        """
        Deals inital player hands and removes cards for the round based
        on the number of players.
        """
        for item in self.players:
            item.draw(self.game_deck)
        if len(self.players) == 2:
            for i in range(2):
                self.removed_cards.append(self.game_deck.draw())
        else:
            self.removed_cards.append(self.game_deck.draw())

    def clear():
        """ Clears the screen. """
        #Handles Windows OS.
        if name == 'nt':
            clear = system('cls')
        #Handles mac and linux OS.
        else:
            clear = system('clear')

    def game_round(self):
        """
        Runs one round of Love Letter. Runs until one player remains or deck
        is exhausted. Returns index of winner to use to reorder in next round.
        """
        #Reset game and players for beginning of round.
        self.reset()
        for player in self.players:
            player.reset()
        #Deal out opening hands.
        self.deal()
        #Reset number of eliminated players to 0.
        num_eliminated_players = 0
        #Main round loop.
        while num_eliminated_players != len(self.players)-1:
            #Iterate through players around the table.
            for player in self.players:
                #Determine number of remaining players.
                #clear screen
                GameEngine.clear()
                num_eliminated_players = sum(
                                             [1 for player in self.players
                                             if player.status == "eliminated"]
                                             )
                #Break out of loop if all but one eliminated or deck exhausted.
                if (
                    num_eliminated_players == len(self.players)-1
                    or len(self.game_deck.deck)==0
                ):
                    GameEngine.clear()
                    break
                #Skip player if they have been eliminated
                if player.status == "eliminated":
                    print(f"{player.name} is eliminated, skipping them.\n")
                    User.cont_play()
                    continue
                else:
                    player.status = "active"
                #Draw a card. Check length of deck.
                player.draw(self.game_deck)
                #Turn management based on user or NPC
                if isinstance(player, User):
                    #Print game information for user.
                    print("Your Turn!\nHere's what the board looks like",
                          f"\n\n{player}")
                    for x in self.players:
                        if x !=player:
                            print(x)
                    player.play_user(self.players, self.player_dict,
                                     self.game_deck)
                else:#NPC turns
                    print(f"{player.name}'s turn.")
                    player.play_level(self.players, self.game_deck)
                print(f"{player.name} finished their turn.\n")
                print()
                User.cont_play()
            #Determine number of remaining players at the end of the round.
            num_eliminated_players = sum(
                                         [1 for player in self.players
                                         if player.status == "eliminated"]
                                         )
            #End round if conditions met.
            if (
                num_eliminated_players == len(self.players)-1
                or len(self.game_deck.deck)==0
            ):
                GameEngine.clear()
                if len(self.game_deck.deck)==0:
                    print("No cards left! Round ends.\n\n")
                else:
                    print("Only one player left!\n\n")
                break
        #Award points.
        winner = self.award(num_eliminated_players)
        return winner

    #how to give players awards at end of the round
    def award(self,num_eliminated_players):
        """
        Identify the winning player at the end of a round
        and award a token (point).
        """
        #Splash text. ASCII art.
        print(open("ASCII\\roundend.txt").read())
        #Number of tokens needed to win the game.
        token_win = {2:2, 3:5, 4:4}
        tokens_needed = token_win[len(self.players)]
        if num_eliminated_players == len(self.players)-1:
            for player in self.players:
                if player.status != "eliminated":
                    player.tokens +=1
                    if isinstance(player,User):
                        print("You are the only player left!.",
                              "You won the round!",
                              f"You get a token! You have {player.tokens}.",
                              f"They need {tokens_needed} total tokens to win.")
                    else:
                        print(f"{player.name} was the only player left.",
                              "They won the round! They are awarded a token.",
                              f"They have {player.tokens}.",
                              f"They need {tokens_needed} total tokens to win.")
                    return player
        else:
            remaining_players = [player for player in self.players
                                 if player.status != "eliminated"]
            card_values = [player.hand[0].value for player in remaining_players]
            high_card = max(card_values)
            if card_values.count(high_card) ==1:
                player_index = card_values.index(high_card)
                winner = remaining_players[player_index]
                winner.tokens +=1
                if isinstance(winner,User):
                    print("You have the highest card. You won the round!",
                          f"You get a token! You have {winner.tokens}.",
                          f"You need {tokens_needed} total tokens to win.")
                else:
                    print(f"{winner.name} had the highest card.",
                          "They won the round! They are awarded a token.",
                          f"They have {winner.tokens}.",
                          f"They need {tokens_needed} total tokens to win.")
                return winner
            else:
                max_table = 0
                winner_index = 0
                player_index = 0
                #Look at table sums to determine winner.
                for i in range(card_values.count(high_card)):
                    table_sum = 0
                    player_index = card_values[player_index:].index(high_card)
                    for item in remaining_players[player_index].table:
                        table_sum += item.value
                    if table_sum >max_table:
                        max_table = table_sum
                        winner_index = player_index
                winner = remaining_players[winner_index]
                winner.tokens+=1
                if isinstance(winner,User):
                    print("Your table had the most points on your table.",
                          "You won the round! You get a token!",
                          f"You have {winner.tokens}",
                          f"You need {tokens_needed} total tokens to win.")
                else:
                    print(f"{winner.name} had the ",
                          "most points on their table. They won the round!",
                          f"They are awarded a token. They have {winner.tokens}.",
                          f"They need {tokens_needed} total tokens to win.")
                return winner

    def start(self):
        """
        Runs the full gameplay and program.
        """
        #Pick inital ordering of players randomly.
        start_player = randint(0,len(self.players))
        #Reorder players so start player is first in list.
        self.players = self.players[start_player:]+self.players[:start_player]
        while True:
            while True:
                #Check number of tokens.
                token_counts = [player.tokens for player in self.players]
                #Winning tokens numbers based on number of players.
                token_win = {2:2, 3:5, 4:4}
                #Check end game criteria.
                if token_win[len(self.players)] == max(token_counts):
                    GameEngine.clear()
                    print(open("ASCII\gameover.txt").read())
                    cont = input("Press Enter to see who won!")
                    GameEngine.clear()
                    winner = self.players[
                                          token_counts.index(max(token_counts))
                                         ]
                    if isinstance(winner, User):
                        print(open("ASCII\win.txt").read())
                    else:
                        print(open("ASCII\lose.txt").read())
                    print(f"{winner.name} won the game with",
                          f"{token_win[len(self.players)]} tokens!")
                    break
                #Play a full round and get winner_index of round.
                winner = self.game_round()
                winner_index = self.players.index(winner)
                #Reorder players so winner of round starts.
                self.players = self.players[winner_index:] + \
                               self.players[:winner_index]
                cont = input("Press Enter to begin the next round.")

            cont = input(
                         "Press Enter to play another game or q to quit. "
                         ).strip()
            if cont.lower() == 'q':
                print("Thanks for playing!")
                return
            else:
                GameEngine.home()

    def home():
        """ Bring the user back to the opening screen to start a new game. """
        GameEngine.clear()
        print(open("ASCII\LLText.txt").read())
        print("Welcome to the Love Letter test emulator!")
        print("New to Love Letter or the text emulator?\nPress i for more",
              "information about the emulator and to learn to play Love Letter!")
        cont = input("If you already know how to play press Enter or q to quit.")
        if cont == "i":
            print("Opening Love Letter emulator website in the browser.")
            webbrowser.open("https://loveletteremulator.weebly.com")
        elif cont == "q":
            print("Thanks for playing.")
            sys.exit()
        print("\nLet's play some Love Letter!")
        name = input("Enter your name: ").capitalize().strip()
        level = input(
                      "Select a difficulty: Easy, Medium, or Hard. "
                      ).lower().strip()
        while level not in ["easy", "medium", "hard"]:
            level = input(
                "Invalid difficulty. Select a difficulty: Easy, Medium, or Hard. "
                ).lower().strip()
        while True:
            num_players = input(
                            "Select a number of players: 2, 3, or 4. "
                            ).strip()
            try:
                num_players = int(num_players)
                if num_players in [2,3,4]:
                    break
                else:
                    print("Invalid number of players.",
                          "Must be 2, 3 or 4.")
            except:
                print("Invalid number of players."
                      "Must be 2, 3 or 4.")
        game = GameEngine(name, num_players, level)

#Scripting to begin the game.
print(open("ASCII\LLText.txt").read())
print("Welcome to the Love Letter test emulator!")
print("New to Love Letter or the text emulator?\nPress i for more",
      "information about the emulator and to learn to play Love Letter!")
cont = input("If you already know how to play press Enter.")
if cont == "i":
    print("Opening Love Letter emulator website in the browser.")
    webbrowser.open("https://loveletteremulator.weebly.com")
print("\nLet's play some Love Letter!")
name = input("Enter your name: ").capitalize().strip()
level = input(
              "Select a difficulty: Easy, Medium, or Hard. "
              ).lower().strip()
while level not in ["easy", "medium", "hard"]:
    level = input(
        "Invalid difficulty. Select a difficulty: Easy, Medium, or Hard. "
        ).lower().strip()
while True:
    num_players = input(
                    "Select a number of players: 2, 3, or 4. "
                    ).strip()
    try:
        num_players = int(num_players)
        if num_players in [2,3,4]:
            break
        else:
            print("Invalid number of players.",
                  "Must be 2, 3 or 4.")
    except:
        print("Invalid number of players."
              "Must be 2, 3 or 4.")
#Start game with user input.
game = GameEngine(name, num_players, level)
