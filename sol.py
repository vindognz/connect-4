from colours import Colours as C
import json, random, time

#region Constants
MIN_BOARD_SIZE: tuple[int,int] = (3,3)
MAX_BOARD_SIZE: tuple[int,int] = (9,9)

settings: dict = None
DEFAULT_SETTINGS = {
    'display_mode': ('preset','coloured_text',('coloured_text','coloured_background','no_colour')),
    'board_columns': ('custom',7,(MIN_BOARD_SIZE[0],MAX_BOARD_SIZE[0])),
    'board_rows': ('custom',6,(MIN_BOARD_SIZE[1],MAX_BOARD_SIZE[1])),
    'connect_count': ('custom',4),
}
#endregion Constants

#region Input Funcs
def await_enter():
    input()

def get_int_input(prompt: str, min: int|None = None, max: int|None = None) -> int:
    '''Get an integer from the user, with optional `min` / `max`.'''
    while True:
        clear()
        try:
            inp = input(str(prompt)).strip()

            #region Validate input
            if not inp.isdecimal():
                raise ValueError(f'Input must be an integer.')
            inp = int(inp)
            if min != None and inp < min:
                raise ValueError(f'Input must be at least {min}.')
            if max != None and inp > max:
                raise ValueError(f'Input must be at most {max}.')
            #endregion Validate input

            return inp
        except ValueError as e: # Retry
            print(e)
            print('Press ENTER to retry.')
            await_enter()

def menu_choice(prompt: str, options: tuple[str]) -> str:
    '''Provides an input for the user to select an option from `options`.'''
    clear()
    prompt = [prompt]
    i = 0
    for title in options:
        i += 1
        prompt.append(f'{i}. {title}')
    choice = get_int_input('\n'.join(prompt)+'\n> ',1,i)
    clear()
    return options[choice-1]
#endregion Input Funcs

#region Display Funcs
def clear():
    print(end='\033[2J\033[1;1H',flush=True)

def display_tile(tile: int, win: bool = False) -> str:
    #region Ensure Arguments
    if type(tile) != int: raise TypeError(tile)
    if type(win) != bool: raise TypeError(win)
    if tile not in range(3): raise ValueError(f'Argument \'tile\' ({tile}) must be within range 0-2.')
    #endregion Ensure Arguments

    if settings['display_mode'] == 'coloured_text':
        if tile == 1:
            return f'{C.BOLD}{C.LIGHT_GREEN}R{C.END}' if win else f'{C.BOLD}{C.RED}R{C.END}'
        elif tile == 2:
            return f'{C.BOLD}{C.LIGHT_GREEN}Y{C.END}' if win else f'{C.BOLD}{C.YELLOW}Y{C.END}'
        else:
            return f'{C.BOLD}{C.DARK_GRAY}O{C.END}'
        
    elif settings['display_mode'] == 'coloured_background':
        if tile == 1:
            return f'{C.BG_LIGHT_GREEN}{C.BOLD}R{C.END}' if win else f'{C.BG_RED} {C.END}'
        elif tile == 2:
            return f'{C.BG_LIGHT_GREEN}{C.BOLD}Y{C.END}' if win else f'{C.BG_LIGHT_YELLOW} {C.END}'
        else:
            return f'{C.BG_DARK_GRAY} {C.END}'

    elif settings['display_mode'] == 'no_colour':
        if tile == 1:
            return 'R' if win else 'r'
        elif tile == 2:
            return 'Y' if win else 'y'
        else:
            return ' '
    
    else:
        raise Exception('Unknown display mode!')
#endregion Display Funcs

class Board():
    def __init__(self, size_x: int = 7, size_y: int = 6, connect_count: int = 4):
        #region Ensure Arguments
        if type(size_x) != int: raise TypeError(size_x)
        if type(size_y) != int: raise TypeError(size_y)
        if type(connect_count) != int: raise TypeError(connect_count)
        if size_x not in range(MIN_BOARD_SIZE[0],MAX_BOARD_SIZE[0]+1): raise ValueError(f'Argument \'size_x\' ({size_x}) must be within range {MIN_BOARD_SIZE[0]}-{MAX_BOARD_SIZE[0]}.')
        if size_y not in range(MIN_BOARD_SIZE[1],MAX_BOARD_SIZE[1]+1): raise ValueError(f'Argument \'size_y\' ({size_y}) must be within range {MIN_BOARD_SIZE[1]}-{MAX_BOARD_SIZE[1]}.')
        if connect_count not in range(3,min(size_x,size_y)+1): raise ValueError(f'Argument \'connect_count\' ({connect_count}) must be within range {3}-{min(size_x,size_y)}.')
        #endregion Ensure Arguments

        self.size_x = size_x
        self.size_y = size_y
        self.connect_count = connect_count
        self._board: list[list[int]] = [[0 for y in range(size_y)] for x in range(size_x)]
        self.history: list[tuple[int,int,int]] = []

    def copy(self):
        out = Board(self.size_x,self.size_y,self.connect_count)
        for x in range(self.size_x):
            for y in range(self.size_y):
                out.set_tile(x,y,self.get_tile(x,y))
        return out
    
    def reset(self) -> None:
        '''Clear the board and it's history.'''
        self._board = [[0] * self.size_y for _ in range(self.size_x)]
        self.history.clear()
    
    def get_tile(self, x: int, y: int) -> int:
        '''
        Return the tile at x,y of the board. \n
        0: Empty,
        1: Player 1,
        2: Player 2.
        '''
        #region Ensure Arguments
        if type(x) != int: raise TypeError(x)
        if type(y) != int: raise TypeError(y)
        if x not in range(self.size_x): raise ValueError(f'Argument \'x\' ({x}) must be within range 0-{self.size_x-1}.')
        if y not in range(self.size_y): raise ValueError(f'Argument \'y\' ({y}) must be within range 0-{self.size_y-1}.')
        #endregion Ensure Arguments

        return self._board[x][y]
    
    def set_tile(self, x: int, y: int, tile: int) -> None:
        '''
        Set the tile at x,y of the board. \n
        `tile`:
        0 -> Empty,
        1 -> Player 1,
        2 -> Player 2.
        '''
        #region Ensure Arguments
        if type(x) != int: raise TypeError(x)
        if type(y) != int: raise TypeError(y)
        if type(tile) != int: raise TypeError(tile)
        if x not in range(self.size_x): raise ValueError(f'Argument \'x\' ({x}) must be within range 0-{self.size_x-1}.')
        if y not in range(self.size_y): raise ValueError(f'Argument \'y\' ({y}) must be within range 0-{self.size_y-1}.')
        if tile not in range(3): raise ValueError(f'Argument \'tile\' ({tile}) must be within range 0-2.')
        #endregion Ensure Arguments

        self._board[x][y] = tile
        self.history.append((x,y,tile))

    def top_in_column(self, x: int) -> int|None:
        '''Returns the y value of the first empty cell in a column (`x`), or None.'''
        #region Ensure Arguments
        if type(x) != int: raise TypeError(x)
        if x not in range(self.size_x): raise ValueError(f'Argument \'x\' ({x}) must be within range 0-{self.size_x-1}.')
        #endregion Ensure Arguments

        column = self._board[x]

        try:
            return column.index(0)
        except ValueError:
            return None
    
    def is_full(self) -> bool:
        '''Returns whether or not the board is full.'''
        return not any(self.top_in_column(x) != None for x in range(len(self._board)))
    
    def display(self, win_tiles: list[tuple[int,int]] = []) -> None:
        '''
        Returns a string of the board, ready to print out. \n
        `win_tiles` is a list of tiles to highlight in the win colour.
        '''
        out = []

        base_row: str = f'+{'+'.join(['---' for x in range(self.size_x)])}+'

        out.append(f'CONNECT {self.connect_count}'.center(len(base_row)))
        out.append(base_row)

        for y in range(self.size_y).__reversed__():
            out.append(f'|{'|'.join([f' {display_tile(self.get_tile(x,y), any([(x,y) == tile for tile in win_tiles]))} ' for x in range(self.size_x)])}|')

        out.append(base_row)
        out.append(f' {' '.join([f' {x+1} ' for x in range(self.size_x)])} ')

        return('\n'.join(out))
    
    def history_log(self, show_y: bool = False) -> str:
        '''
        Returns a log of the tiles set, ready to print out. \n
        `show_y` determines whether or not columns or the whole position is displayed.
        '''
        #region Ensure Arguments
        if type(show_y) != bool: raise TypeError(show_y)
        #endregion Ensure Arguments

        out = []

        for i,action in enumerate(self.history):
            x,y,tile = action
            out.append(f'{i}. {('Reset',display_tile(1),display_tile(2))[tile]} at {x}{f',{y}' if show_y else ''}')
        
        return '\n'.join(out)

    def check_win(self, player: int):
        '''If the given player (`player`) has won, returns a list of the tiles that gave them the won, otherwise None.'''
        #region Ensure Arguments
        if type(player) != int: raise TypeError(player)
        if player not in range(1,3): raise ValueError(f'Argument \'player\' ({player}) must be within range 1-2.')
        #endregion Ensure Arguments

        for row in range(self.size_y):
            for col in range(self.size_x - self.connect_count + 1):
                if all(self.get_tile(col + i, row) == player for i in range(self.connect_count)):
                    return [(col + i, row) for i in range(self.connect_count)]
        for col in range(self.size_x):
            for row in range(self.size_y - self.connect_count + 1):
                if all(self.get_tile(col, row + i) == player for i in range(self.connect_count)):
                    return [(col, row + i) for i in range(self.connect_count)]
        for col in range(self.size_x - self.connect_count + 1):
            for row in range(self.size_y - self.connect_count + 1):
                if all(self.get_tile(col + i, row + i) == player for i in range(self.connect_count)):
                    return [(col + i, row + i) for i in range(self.connect_count)]
        for col in range(self.size_x - self.connect_count + 1):
            for row in range(self.connect_count - 1, self.size_y):
                if all(self.get_tile(col + i, row - i) == player for i in range(self.connect_count)):
                    return [(col + i, row - i) for i in range(self.connect_count)]

class Game():
    def __init__(self, player1_move_provider, player2_move_provider, board_size: tuple[int,int] = (7,6), connect_count: int = 4):
        self.board = Board(board_size[0],board_size[1],connect_count) # We have this before the next Ensure Arguments block to make board_size related argument errors take priority

        #region Ensure Arguments
        if not callable(player1_move_provider): return ValueError(player1_move_provider)
        if not callable(player2_move_provider): return ValueError(player2_move_provider)
        #endregion Ensure Arguments
        
        self.connect_count = connect_count
        self.player1_move_provider = player1_move_provider
        self.player2_move_provider = player2_move_provider

    def play(self, starting_player: int = 1) -> int:
        '''Starts the game.'''
        #region Ensure Arguments
        if type(starting_player) != int: raise TypeError(starting_player)
        if starting_player not in range(1,3): raise ValueError(f'Argument \'starting_player\' ({starting_player}) must be within range 1-2.')
        #endregion Ensure Arguments
        player = starting_player

        while True:
            # Display the board
            clear()
            print(self.board.display())

            # Get the column from the current player
            try:
                if player == 1:
                    x = self.player1_move_provider(player, self.board)
                else:
                    x = self.player2_move_provider(player, self.board)
            except KeyboardInterrupt:
                clear()
                print('Match ended early.')
                print('Press ENTER to return to the menu.')
                await_enter()
                return None
            # Check if the column is valid and get the y to claim, otherwise ask them again
            try:
                y = self.board.top_in_column(x)
                if y == None:
                    continue
            except ValueError:
                continue

            # Claim the tile
            self.board.set_tile(x,y,player)

            # Check if the player has won, and exit the game loop if they have
            win_tiles = self.board.check_win(player)
            if win_tiles != None:
                clear()
                print(self.board.display(win_tiles))
                print(f'{display_tile(player)} won!')
                print('Press ENTER to return to the menu.')
                await_enter()
                return player
            
            if self.board.is_full():
                clear()
                print(self.board.display())
                print('Draw!')
                print('Press ENTER to return to the menu.')
                await_enter()
                return player

            # Swap player for next turn
            player = 2 if player == 1 else 1
        
#region Move Providers
def local_move_provider(player: int, board: Board) -> int:
    clear()
    return get_int_input(f'{board.display()}\n {display_tile(player)} > ',1,board.size_x)-1

def cpu_move_provider(player: int, board: Board) -> int:
    time.sleep(0.125+random.random()*0.25)
    return random.randint(1,board.size_x)
#endregion Move Providers

game_modes = {
    'Local PVP': (local_move_provider,local_move_provider),
    'Player VS CPU': (local_move_provider,cpu_move_provider),
    'CPU VS CPU': (cpu_move_provider,cpu_move_provider),
    'LAN (Host)': 'LAN (Host) is currently under maintenance due to exploits!', # TODO
    'LAN (Client)': 'LAN (Client) is currently under maintenance due to exploits!' # TODO
}

def load_settings():
    '''Loads settings from `settings.json`'''
    global settings
    settings = {}
    for k,v in DEFAULT_SETTINGS.items():
        settings[k] = v[1]
    try:
        with open('settings.json', 'r') as f: json_settings: dict = json.load(f)
        for k,v in json_settings.items():
            if k in DEFAULT_SETTINGS: settings[k] = v
    except (FileNotFoundError, json.JSONDecodeError): pass
load_settings()

#region Main Menu
while True:
    try:
        choice = menu_choice(
        '=== Main Menu ===\nHow do you want to play?',(
            *[title for title in game_modes.keys()], # Game modes
            'Edit settings',
            'Quit',
        ))
    except KeyboardInterrupt: choice = 'Quit' # Allows for fast, clean exit

    if choice == 'Quit': clear(); break
        
    elif choice == 'Edit settings':
        while True:
            try:
                choice = menu_choice(
                '=== Settings Menu ===\nChoose a setting to edit, or save and return to the menu:',(
                    *[f'{title} ({value})' for title,value in settings.items()], # Settings
                    'Save and return to main menu'
                ))
            except KeyboardInterrupt: # Allows for fast, clean save and exit
                with open('settings.json', 'w') as f: json.dump(settings, f, indent=4);
                break

            if choice == 'Save and return to main menu':
                with open('settings.json', 'w') as f: json.dump(settings, f, indent=4)
                print('Settings saved.')
                print('Press ENTER to return to the menu.')
                await_enter()
                break
            
            else: # Edit a setting
                setting_name = choice.split(' (')[0]
                setting_data = DEFAULT_SETTINGS[setting_name]
                default_val = setting_data[1]
                setting_type = setting_data[0]

                def setting_type_preset(options):
                    '''Prompt for a setting value from `options`.'''
                    try:
                        choice = menu_choice(f'Set value for {setting_name}:\n(Or press Ctrl+C to set to default value: {default_val})', options)
                    except KeyboardInterrupt: choice = default_val
                    settings[setting_name] = choice

                def setting_type_int(min_val,max_val):
                    '''Prompt for a setting value of type int with optional `min` / `max`.'''
                    try:
                        choice = get_int_input(f'Set value for {setting_name}{f' (from {min_val}-{max_val})' if min_val != None and max_val != None else ''}:\n(Or press Ctrl+C to set to default value: {default_val})\n> ', min_val, max_val)
                    except KeyboardInterrupt: choice = default_val
                    settings[setting_name] = choice

                if setting_type == 'preset': setting_type_preset(setting_data[2])
                elif setting_type == 'int': setting_type_int(*setting_data[2])
                # TODO MORE VALUE TYPES
                elif setting_type == 'custom':
                    
                    #region Make sure connect_count is always a legal value
                    if setting_name == 'board_columns':
                        setting_type_int(*setting_data[2])
                        if settings['connect_count'] > min(settings['board_columns'],settings['board_rows']): settings['connect_count'] = min(settings['board_columns'],settings['board_rows'])

                    if setting_name == 'board_rows':
                        setting_type_int(*setting_data[2])
                        if settings['connect_count'] > min(settings['board_columns'],settings['board_rows']): settings['connect_count'] = min(settings['board_columns'],settings['board_rows'])

                    if setting_name == 'connect_count':
                        setting_type_int(3, min(settings['board_columns'],settings['board_rows']))
                    #endregion Make sure connect_count is always a legal value
    
    else: # Play a game
        game_mode = game_modes[choice]

        if type(game_mode) == str:
            print(game_mode) # Prints out a reason as to why this game mode is currently unavaliable
            print('Press ENTER to return to the menu.')
            await_enter()

        elif callable(game_mode): # Allows for setup, i.e socket starting before the game
            game: Game = game_mode() # This function should return a Game object, and can optionally use settings
            game.play()

        elif type(game_mode) == tuple: # Allows for a simple game mode with 2 player providers
            game = Game(game_mode[0],game_mode[1],(settings['board_columns'],settings['board_rows']),settings['connect_count'])
            game.play()
#endregion Main Menu