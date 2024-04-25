from random import choice
from re import match
from os import system

class Tic_Tac_Toe_3D:

    def __init__(self, scores=None, old_players=None):
        # Constructor method for initializing the game
        # Accepts optional parameters for scores, old_players
        
        if scores != None and old_players != None:
            # If scores and old_players are provided, it means the game is being initialized with existing data
            
            # Determine the players based on the old_players dictionary
            player1 = old_players['X']      
            player2 = old_players['O'] 

            # Assign scores to the players based on the wins
            self.scores = {player1: scores[player1], player2: scores[player2]} if scores[player1] > scores[player2] else {player2: scores[player2], player1: scores[player1]}
            
            # Print existing scores
            print(f"\n-------------------------------------------\nScores:") 
            for player, wins in self.scores.items():
                print(f'---> {player}: {wins}')
        else: 
            # If scores and old_players are not provided, prompt for player names and initialize scores to 0
            player1 = input("---> Enter your name player 1: ")
            player2 = input("---> Enter your name player 2: ")
            while player1 == "" or player2 == "" or player1 == player2:
                print("\nPick another\n")
                player1 = input("---> Enter your name player 1: ")
                player2 = input("---> Enter your name player 2: ")
            self.scores = {player1: 0, player2: 0}
        
        # Initialize the players dictionary with 'X' and 'O' symbols
        self.players = {'X':'', 'O':''}
        # Randomly assign the symbols to players
        self.players['X'] = choice([player1,player2])
        self.players['O'] = player1 if self.players['X'] == player2 else player2

        # Initialize the current player to 'X'
        self.current_player = 'X'   
        
        # Initialize the game board as a 3D list
        self.board=[[['1','2','3'],['4','5','6'],['7','8','9']],
                    [['1','2','3'],['4','5','6'],['7','8','9']],
                    [['1','2','3'],['4','5','6'],['7','8','9']]]
        
        # Define the winning combinations for tic-tac-toe
        self.winning_combinations = [
            # Rows
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            # Columns
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            # Diagonals
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
        
        # Start the game
        self.Start()

    # Method to start the game    
    def Start(self):
        
        # Print the game board
        self.printBoards()

        # Check if there is a winner or a tie
        if self.checkWin() or self.checkTie():
            # If there's a winner or a tie, start a new game
            self.new_game()
        else:
            # If the game is ongoing, prompt the current player for their move
            print(f"\n---- It's {self.players[self.current_player]}'s turn ----\n")
            layer, cell = '',''
            invalid=True

            while invalid:
                # Prompt the player to choose a layer and a position
                layer = input("---> Choose a layer (1-3): ")      
                cell = input("---> Choose a cell (1-9): ")
                try:
                    # Convert inputs to integers
                    layer = int(layer)
                    cell = int(cell)
                    invalid = False

                    # Check if the input is valid
                    if not 0 < layer < 4 or not 0 < cell < 10 or self.checkBoard(layer,cell):
                        print("\nInvalid input, Try again\n")
                        invalid = True
                except:
                    print("\nInvalid input, Try again\n")

            # Make the move
            self.move(layer,cell)

    # Method to print the game board in a nice format
    def printBoards(self):
        print("\n[1]----------      [2]----------      [3]----------")
        for row in range(3):
            for layer in range(3):
                print(f'| {self.board[layer][row][0]} | {self.board[layer][row][1]} | {self.board[layer][row][2]} |', end='')
                print("      ", end='')
            print()
            print("-------------      -------------      -------------")
    
    # Method to adjust the move based on the cell
    def adjustMove(self,cell):        
        row = 0
        if 1 <= cell <= 8 and cell%3 != 0: 
            row = cell//3
            if (cell%2 != 0 and cell != 5) or cell == 4: cell = 0
            else: cell = 1   
        else: row = cell//3-1; cell = 2
        return [row,cell]

    # Method to make a move
    def move(self, layer,cell):
        move = self.adjustMove(cell)
        self.board[layer-1][move[0]][move[1]] = self.current_player
        self.changeTurn()
        system('clear')
        self.Start()

    # Method to check if a position on the board is already taken
    def checkBoard(self,layer,cell):
        move = self.adjustMove(cell)
        return match('\\D',self.board[layer-1][move[0]][move[1]])
    
    # Method to change the turn
    def changeTurn(self):
        self.current_player = "X" if self.current_player == "O" else "O"

    # Method to check if there's a winner
    def checkWin(self):
        same_cell = False
        # Changing current player to the previous one to check if he wins
        self.changeTurn()

        # Iterate over each winning combination
        for combo in self.winning_combinations:
            # Initialize a dictionary to track if each cell in the combination matches the current player's symbol
            match_combo = {combo[0]: False, combo[1]: False, combo[2]: False}
            
            # Check each cell in the combination
            for layer in range(3):
                for cell in combo:
                    if self.board[layer][cell[0]][cell[1]] == self.current_player:
                        match_combo[cell] = True
            
            # Check for a win in the same cell in all three layers ([0][0][0] = [1][0][0] = [2][0][0])
            for row in range(3):
                 for col in range(3):
                    if self.board[0][row][col] == self.board[1][row][col] == self.board[2][row][col] == self.current_player:
                        same_cell = True

            # If all cells in the combination match the current player's symbol, or the same symbol in a cell in all layers is found, declare the winner        
            if all(value for value in match_combo.values()) or same_cell:
                print(f"\n---->> {self.players[self.current_player]} won <<----\n")
                # Update scores for the winning player
                self.scores[self.players[self.current_player]] += 1
                return True
        
        # Change turn back to the original player if no winner is found
        self.changeTurn()
        return False
    
    # Method to check if the game is tied
    def checkTie(self):
        return match('^([^0-9]*)$',str(self.board))

    # Method to start a new game
    def new_game(self):     
        ans = input("---> GAME OVER, Do you want to play a new game? (Y/N): ")
        match ans:
            case "Y" | "y" | "yes": Tic_Tac_Toe_3D(self.scores,self.players)
            case "N" | "n" | "no" : print("\n---- Ok Bye ----\n"); exit
            case _: print("invalid input, let's try again"); self.new_game()
        
# Start the game
Tic_Tac_Toe_3D()
