"""
A text-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

from typing import Tuple, Optional, Dict, List

from main_support import *

# Author: Abdullah Shafqat

class Entity:
    """
    Entity is an abstract class that is used to represent
    anything that can appear on the game’s grid

    For example, the game grid will always have a player,
    so a player is considered a type of entity.
    """
    
    def step(self, position: "Position", game: "Game") -> None:
        """
        Returns nothing
        
        The step method is called on every entity in the game grid
        after each move made by the player, it controls what actions
        an entity will perform during the step event.
        
        The abstract Entity class will not perform any action
        during the step event. Therefore, this method should do nothing.

        Parameters:
            position: The position of this entity when the step event
                        is triggered.
            game: The current game being played. 
        """
        return None
    
    def display(self) -> str:
        """
        Return the character used to represent this entity in a
        text-based grid.

        An instance of the abstract Entity class should never be
        placed in the grid, so this method should only be implemented
        by subclasses of Entity.

        The abstract Entity class should raise a NotImplementedError for
        this method.
        """
        raise NotImplementedError
    
    def __repr__(self) -> str:
        """
        Return a representation of this entity.

        By convention, the repr string of a class should look
        as close as possible to how the class is constructed.
        Since entities do not take constructor parameters,
        the repr string will be the class name followed by parentheses, ().

        Examples:
            >>> repr(Entity())
            'Entity()'
            >>> Entity().__repr__()
            'Entity()'
        """
        #return "Entity()"
        return self.__class__.__name__ + "()"

    
class Player(Entity):
    """
    Inherits from Entity abstract class

    A player is a subclass of the entity class that represents
    the player that the user controls on the game grid.

    Examples:
        >>> player = Player()
        >>> player
        Player()
    """
    
    def display(self) -> str:
        """
        Return the character used to represent the
        player entity in a text-based grid.
        
        A player should be represented by the ‘P’ character.

        Examples:
            >>> player = Player()
            >>> player.display()
            'P'
        """
        return PLAYER
    
    def __repr__(self) -> str:
        """
        Return a representation of this entity.

        Examples:
            >>> repr(Player())
            'Player()'
            >>> Player().__repr__()
            'Player()'
        """
        return "Player()"


# the hospital class inherits from entity
class Hospital(Entity):
    """
    Inherits from Entity abstract class

    The hospital is the entity that the player has to
    reach in order to win the game.

    Examples:
        >>> hospital = Hospital()
        >>> hospital
        Hospital()
    """
    
    def display(self) -> str:
        """
        Return the character used to represent the
        hospital entity in a text-based grid.
        
        A hospital should be represented by the ‘H’ character.

        Examples:
            >>> player = Player()
            >>> player.display()
            'H'
        """
        return HOSPITAL
    
##    def __repr__(self) -> str:
##        """
##        insert docstring
##        """
##        return "Hospital()"


class Grid:
    """
    The Grid class is used to represent the 2D grid of entities.
    
    The grid can vary in size but it is always a square.
    Each (x, y) position in the grid can only contain one entity at a time.

    Examples:
        >>> grid = Grid(5)
        >>> grid.get_size()
        5
        >>> grid.in_bounds(Position(2, 2))
        True
        >>> grid.in_bounds(Position(0, 6))
        False >>> grid.get_entities()
        []
        >>> grid.add_entity(Position(2, 2), Hospital())
        >>> grid.get_entity(Position(2, 2)) Hospital()
        >>> grid.get_entities()
        [Hospital()]
        >>> grid.serialize()
        {(2, 2): 'H'}

    """

    # the size of the grid
    size:int = None
    # the list of current entities in the grid
    entities:List[Entity] = None
    # the dictionary of entities along with their locations in the grid
    EntityLocations:Dict[Tuple[int, int], Entity] = None
    
    def __init__(self, size: int):
        """
        A grid is constructed with a size that dictates
        the length and width of the grid.
        Initially a grid does not contain any entities.

        Parameters:
            size: The length and width of the grid
        """
        # initializing all the class variables
        self.size = size
        self.EntityLocations = {}
        self.entities = []
        
    def get_size(self) -> int:
        """
        Returns the size of the grid. 
        """
        return self.size
    
    def in_bounds(self, position: "Position") -> bool:
        """
        Return True if the given position is within the bounds of the grid.
        
        For a position to be within the bounds of the grid,
        both the x and y coordinates have to be greater than
        or equal to zero but less than the size of the grid.

        Parameters:
            position: An (x, y) position that we want to check
                        is within the bounds of the grid.

        Examples:
            >>> grid5 = Grid(5)
            >>> grid5.in_bounds(Position(0, 10))
            False
            >>> grid5.in_bounds(Position(0, 4))
            True 
        """
        if(0 <= position.get_x() < self.size and
           0 <= position.get_y() < self.size):
            return True
        else:
            return False
        
    def add_entity(self, position: "Position", entity: "Entity") -> None:
        """
        Place a given entity at a given position of the grid.

        If there is already an entity at the given position,
        the given entity will replace the existing entity.

        If the given position is outside the bounds of the grid,
        the entity will not be added.

        Parameters:
            position:  An (x, y) position in the grid to place the entity. 
            entity: The entity to place on the grid.

        Examples:
            >>> grid = Grid(4)
            >>> grid.add_entity(Position(0, 0), Player()) 
        """
        # if position out of bounds return
        if self.in_bounds(position) == False:
            return None

        # removing the entity if any at the position where new
        # entity is to be added
        # using method 'pop' with optional parameter default equal to 'None'
        entity_removed = self.EntityLocations.pop((position.get_x(), position.get_y()), None)

        if entity_removed != None:
            # removing the entity previously at postion
            # if any from the entities list
            self.entities.remove(entity_removed)

        # adding the entity to the dictionary of locations
        # as well as to the list of entities
        self.EntityLocations.update({(position.get_x(), position.get_y()):entity})
        self.entities.append(entity)
        
    def remove_entity(self, position: "Position") -> None:
        """
        Remove the entity, if any, at the given position.

        Parameters:
            position: An (x, y) position in the grid from which
                        the entity is removed.

        Examples:
            >>> grid = Grid(4)
            >>> grid.add_entity(Position(0, 0), Player())
            >>> grid.remove_entity(Position(0, 0))
        """
        # if position is out of bounds return

        if self.in_bounds(position) == False:
            return None

        # removing the entity if any at the position if any
        # using method 'pop' with optional parameter default equal to 'None'
        entity_at_position = self.EntityLocations.pop((position.get_x(), position.get_y()), None)

        if entity_at_position != None:
            # removing the entity previously at postion
            # if any from the entities list
            self.entities.remove(entity_at_position)

    def get_entity(self, position: "Position") -> Optional[Entity]:
        """
        Return the entity that is at the given position in the grid.

        If there is no entity at the given position, returns None.
        If the given position is out of bounds, returns None.

        Parameters:
            position: An (x, y) position in the grid from which
                        the entity is removed.

        Examples:
            >>> grid = Grid(4)
            >>> grid.add_entity(Position(0, 0), Player())
            >>> grid.get_entity(Position(0, 0))
            Player()
            >>> grid.get_entity(Position(1, 1)) 
        """
        if self.in_bounds(position) == False:
            return None

        # getting the entity at defined position
        # using method 'get' with optional parameter default equal to 'None'
        return self.EntityLocations.get((position.get_x(), position.get_y()), None)
         
    def get_mapping(self) -> Dict[Position, Entity]:
        """
        Return a dictionary with position instances as the keys
        and entity instances as the values.

        For every position in the grid that has an entity,
        the returned dictionary contains an entry with
        the position instance mapped to the entity instance.

        Examples:
            >>> grid = Grid(4)
            >>> grid.add_entity(Position(0, 0), Player())
            >>> grid.add_entity(Position(3, 3), Hospital())
            >>> grid.get_mapping()
            {Position(0, 0): Player(), Position(3, 3): Hospital()}
        """
        return_dictionary = {}

        for key, value in self.EntityLocations.items():
            # creating a Postion instance using the values
            # from the key tuple
            return_dictionary.update({Position(key[0], key[1]):value})
            
        return return_dictionary
    
    def get_entities(self) -> List[Entity]:
        """
        Return a list of all the entities in the grid.

        Examples:
            >>> grid = Grid(5)
            >>> grid.add_entity(Position(0, 0), Hospital())
            >>> grid.add_entity(Position(0, 1), Player())
            >>> grid.get_entities()
            [Hospital(), Player()]
        """
        return self.entities
    
    def move_entity(self, start: "Position", end: "Position") -> None:
        """
        Moves an entity from the given start position
        to the given end position.

        Do not attempt to move if:
            the end position or start position is out of the grid bounds.
            there is no entity at the given start position.

        If there is an entity at the given end position,
        replace that entity with the entity from the start position.

        The start position should not have an entity after moving.

        Parameters:
            start: The position the entity is in initially.
            end:  The position to which the entity will be moved.

        Examples:
            >>> grid = Grid(10)
            >>> grid.add_entity(Position(1, 2), Player())
            >>> grid.move_entity(Position(1, 2), Position(3, 5))
            >>> grid.get_entity(Position(1, 2))
            >>> grid.get_entity(Position(3, 5))
            Player()
        """
        # checking for out of bounds
        if self.in_bounds(start) == False or self.in_bounds(end) == False:
            return None

        # removing the entity from the start position if any
        # if no entity exists this variable will hold None
        entity_at_start = self.EntityLocations.pop((start.get_x(), start.get_y()),
                                                   None)

        if entity_at_start != None:

            # using the remove_entity method to remove entity at end position
            self.remove_entity(end)
                
            self.EntityLocations.update({(end.get_x(), end.get_y()):
                                         entity_at_start})
        return None
    
    def find_player(self) -> Optional[Position]:
        """
        Return the position of the player within the grid.

        Return None if there is no player in the grid.

        Examples:
            >>> grid = Grid(10)
            >>> grid.add_entity(Position(4, 6), Player())
            >>> grid.find_player()
            Position(4, 6)
        """
        for key, value in self.EntityLocations.items():

            # if the value a instance of class Player
            if isinstance(value, Player):
                return Position(key[0], key[1])
            
        return None
        
    def serialize(self) -> Dict[Tuple[int, int], str]:
        """
        Serialize the grid into a dictionary that maps tuples to characters.

        The tuples have two values,
        the x and y coordinate representing a postion.
        The characters are the display representation of
        the entity at that position. i.e. ‘P’ for player, ‘H’ for hospital.

        Examples:
            >>> grid = Grid(50)
            >>> grid.add_entity(Position(3, 8), Player())
            >>> grid.add_entity(Position(3, 20), Hospital())
            >>> grid.serialize()
            {(3, 8): 'P’, (3, 20): ’H'}
        """
        return_dictionary = {}
        
        for key, value in self.EntityLocations.items():
            
            # calling the display function for the entities
            # to get their character representation
            return_dictionary.update({key:value.display()})

        return return_dictionary


class MapLoader:
    """
    The MapLoader class is an abstract class
    to allow for extensible map deﬁnitions.
    
    The MapLoader class is used to read a map ﬁle
    and create an appropriate Grid instance which
    stores all the map ﬁle entities.
    """
    
    def load(self, filename: str) -> Grid:
        """
        Load a new Grid instance from a map ﬁle.

        Opens the map ﬁle and reads each line to ﬁnd all
        the entities in the grid and add them to the new Grid instance.

        Parameters:
            filename:  Path where the map ﬁle should be found.

        Returns:
            A grid instance made from the map in file

        Examples:
            >>> bml = BasicMapLoader()
            >>> grid = bml.load("maps/basic.txt")
        """
        # reading the mapfile into a Tuple[EntityLocations, int]
        loadedMap = load_map(filename)

        # creating a new grid with size read from the
        # second value in tuple pair
        grid = Grid(loadedMap[1])

        # managing all the entities found in map file
        for key, value in loadedMap[0].items():

            # creating a new entity 
            entity = self.create_entity(value)
            # adding the entity to the grid instance
            grid.add_entity(Position(key[0], key[1]), entity)
            
        return grid
    
    def create_entity(self, token: str) -> Entity:
        """
        Raises NotImplementedError
        
        Create and return a new instance of the
        Entity class based on the provided token.

        Parameters:
            token:  Character representing the Entity subtype.
        """
        raise NotImplementedError

class BasicMapLoader(MapLoader):
    """
    Inherits from MapLoader

    BasicMapLoader is a subclass of MapLoader which can handle
    loading map ﬁles which include the following entities:
        Player
        Hospital 
    """
    
    def create_entity(self, token: str) -> Entity:
        """
        Create and return a new instance of the
        Entity class based on the provided token.
        
        The BasicMapLoader class only supports
        the Player and Hospital entities.

        Raise ValueError if a token not representing Hospital
        or Player is recieved
        """
        if token not in [PLAYER, HOSPITAL]:
            raise ValueError

        elif token == PLAYER:
            return Player()

        elif token == HOSPITAL:
            return Hospital()


class Game:
    """
    The Game handles some of the logic for controlling
    the actions of the player within the grid.

    The Game class stores an instance of the Grid
    and keeps track of the player within the grid
    so that the player can be controlled.
    """
    
    grid:Grid = None
    no_steps:int = None
    
    def __init__(self, grid: "Grid"):
        """
        The construction of a Game instance takes the grid
        upon which the game is being played.

        Parameters:
            grid: The game's grid
            
        Precondition:
            The grid has a player
        """
        self.grid = grid
        self.no_steps = 0

    def get_grid(self) -> Grid:
        """
        Return the grid on which this game is being played.
        """
        return self.grid

    def get_player(self) -> Optional[Player]:
        """
        Return the instance of the Player class in the grid.
        
        If there is no player in the grid, return None. 
        """
        # finding the position of player on map using Grid
        # class method find_player()
        player_position = self.grid.find_player()

        # if the position for a player exists
        if player_position != None:

            # return the entity at the player_position
            return self.grid.get_entity(player_position)
        
        return None

    def step(self) -> None:
        """
        The step method of the game will be called after
        every action performed by the player.

        This method triggers the step event by calling the
        step method of every entity in the grid.
        When the entity‘s step method is called,
        it should pass the entity’s current position
        and this game as parameters.
        """
        # updating the number of steps that have occured in game
        self.no_steps += 1

        # calling step for all entities in grid
        for key, value in self.grid.get_mapping().items():
            value.step(key, self)

    def get_steps(self) -> int:
        """
        Return the amount of steps made in the game
        """
        return self.no_steps

    def move_player(self, offset: "Position") -> None:
        """
        Move the player entity in the grid by a given oﬀset.

        Add the oﬀset to the current position of the player,
        move the player entity within the grid to the new position.

        If the new position is outside the bounds of the grid,
        or there is no player in the grid,
        the method does nothing.

        Parameters:
            offset:  A position to add to the player’s current position
                    to produce the player’s new desired position.
        """
        # the starting position is the current position of player
        start_position = self.grid.find_player()

        # the ending position is the current position of player
        # plus the offset
        end_position = start_position.add(offset)

        self.grid.move_entity(start_position, end_position)

    def direction_to_offset(self, direction: str) -> Optional[Position]:
        """
        Convert a direction, as a string, to a oﬀset position.
        
        The oﬀset position can be added to a position
        to move in the given direction.

        If the given direction is not valid, this method should return None.

        Parameters:
            direction: Character representing the direction in
                        which the player should be moved.

        Examples:
            >>> game = Game(Grid(5))
            >>> game.direction_to_offset("W")
            Position(0, -1)
            >>> game.direction_to_offset("N") 
        """
        if direction == UP:
            return Position(0, -1)

        elif direction == DOWN:
            return Position(0, 1)

        elif direction == LEFT:
            return Position(-1, 0)

        elif direction == RIGHT:
            return Position(1, 0)

        else:
            return None

    def has_won(self) -> bool:
        """
        Return true if the player has won the game.

        The player wins the game by stepping onto the hospital.
        When the player steps on the hospital,
        there will be no hospital entity in the grid. 
        """
        # checking if a hospital entity exists in the entities list
        # if it does player has not won the game yet
        for entity in self.grid.entities:

            if(repr(entity) == "Hospital()"):
                return False

        return True

    def has_lost(self) -> bool:
        """
        Return true if the player has lost the game.

        Game does not handle player losing so this method always
        return False
        """
        return False

class TextInterface(GameInterface):
    """
    Inherits from GameInterface

    A text-based interface between the user and the game instance.

    This class handles all input collection from the user
    and printing to the console. 
    """
    
    size:int = None
    
    def __init__(self, size: int):
        """
        The text-interface is constructed knowing the size
        of the game to be played, this allows the
        draw method to correctly print the right sized grid.

        Parameters:
            size: The size of the game to be displayed and played. 
        """
        self.size = size

    def draw(self, game: "Game") -> None:
        """
        The draw method prints out the given game
        surrounded by ‘#’ characters representing the border of the game.

        Parameters:
            game: An instance of the game class that is to
                    be displayed to the user by printing the grid.

        Examples:
            >>> grid = Grid(4)
            >>> grid.add_entity(Position(2, 2), Player())
            >>> game = Game(grid)
            >>> interface = TextInterface(4)
            >>> interface.draw(game)
            ######
            #    #
            #    #
            #  P #
            #    #
            ######
        """
        grid = game.get_grid()

        # printing the top border
        print(BORDER * (self.size + 2))

        for j in range(self.size):
            # printing the left border
            print(BORDER, end = '')

            # printing the game grid
            for i in range(self.size):
                # getting the value from serialized grid
                # with default parameter set to a empty space lietral
                print(grid.serialize().get((i,j), ' '), end = '')

            # printing the right border
            print(BORDER)

        # printing the bottom border  
        print(BORDER * (self.size + 2))

    def play(self, game: "Game") -> None:
        """
        The play method implements the game loop,
        constantly prompting the user for their action,
        performing the action and printing the game until the game is over.

        Parameters:
            game: The game to start playing.
        """
        # the input loop for game
        while True:
            
            # drawing each loop
            self.draw(game)
            # taking input from player each loop
            action = input(ACTION_PROMPT)
            # handling the action 
            self.handle_action(game, action)

            # checking for win or lose conditions
            # if either one is true break from game loop
            if game.has_won() == True:
                print(WIN_MESSAGE)
                break
            
            elif game.has_lost() == True:
                print(LOSE_MESSAGE)
                break
            
    def handle_action(self, game: "Game", action: str) -> None:
        """
        The handle_action method is used to process the actions
        entered by the user during the game loop in the play method.
        
        The handle_action method should be able to handle
        all movement actions, i.e. ‘W’, ’A’, ’S’, ’D’.

        If the given action is not a direction, this method should do nothing.

        Parameters:
            game: The game that is currently being played. 
            action: An action entered by the player during the game loop.

        """
        # converting string input into a position instance
        offset_position = game.direction_to_offset(action)

        # if the string input was valid
        if offset_position != None:
            # move the player
            game.move_player(offset_position)

        # call the step function of game regardless
        game.step()


class VulnerablePlayer(Player):
    """
    Inherits from Player

    The VulnerablePlayer class is a subclass of the Player,
    this class extends the player by allowing them to become infected.

    Now a Player entity has a way to lose by becoming infected

    Examples:
        >>> player = VulnerablePlayer()
        >>> player.is_infected()
        False
        >>> player.infect()
        >>> player.is_infected()
        True
    """
    
    infected: bool = None
    
    def __init__(self):
        """
        When an object of the VulnerablePlayer class is constructed,
        the player is not be infected
        """
        self.infected = False

    def infect(self):
        """
        When the infect method is called,
        the player becomes infected. 
        """
        self.infected = True

    def is_infected(self) -> bool:
        """
        Return the current infected state of the player.
        """
        return self.infected

class Zombie(Entity):
    """
    Inherits from Entity

    The Zombie entity will wander the grid at random.
    
    The movement of a zombie is triggered by the player performing an action,
    i.e. the zombie moves during each step event. 
    """
    
    def step(self, position: "Position", game: "Game") -> None:
        """
        Move the zombie in a random direction

        If no positions are available, do not move the zombie.

        To be available, a position must be in the bounds of the grid
        and not already contain an entity.

        If the position the zombie is going to move to contains the player,
        the zombie should infect the player but not move to that position.

        Parameters:
            position: The position of this zombie when the
                        step event is triggered.
            game: The current game being played.
        """
        # getting a list of random directions
        rnd_directions = random_directions()
        grid = game.get_grid()
        
        for i in range(len(rnd_directions)):
            
            direction = rnd_directions[i]

            # the final position to be moved to is the zombies' current position
            # plus the offset from the random directions
            final_position = position.add(Position(direction[0],direction[1]))

            # if final position out of bounds try the next random direction
            if grid.in_bounds(final_position) == False:
                continue

            # if there is no entity at final position, move the zombie
            if grid.get_entity(final_position) == None:
                grid.move_entity(position, final_position)
                return None

            # if there is a Player entity at final position
            # do not move the zombie but infect the player
            if isinstance(grid.get_entity(final_position), Player):
                game.get_player().infect()   
                return None

        return None

    def display(self) -> str:
        """
        Return the character used to represent the
        zombie entity in a text-based grid.
        
        A zombie should be represented by the ‘Z’ character.

        Examples:
            >>> zombie = Zombie()
            >>> zombie.display()
            'Z'
        """
        return ZOMBIE

    
class IntermediateGame(Game):
    """
    Inherits from Game

    An intermediate game extends some of the functionality of the basic game.
    
    The intermediate game includes the ability for the player
    to lose the game when they become infected. 
    """
    
    def has_lost(self) -> bool:
        """
        Return true if the player has lost the game.

        The player loses the game if they become infected by a zombie.
        """
        player = self.get_player()

        return player.is_infected()

class IntermediateMapLoader(BasicMapLoader):
    """
    Inherits from BasicMapLoader

    The IntermediateMapLoader class extends BasicMapLoader
    to add support for new entities.

    When a player token, ‘P’, is found, a VulnerablePlayer
    instance should be created instead of a Player.

    In addition to the entities handled by the BasicMapLoader,
    the IntermediateMapLoader should be able to load the following entities:
        Zombie
    """
    
    def create_entity(self, token: str) -> Entity:
        """
        Create and return a new instance of the
        Entity class based on the provided token.
        
        The IntermediateMapLoader class only supports
        the Player, Hospital and Zombie entities.

        Raise ValueError if a token not representing Hospital, Player
        or Zombie is recieved
        """
        if token not in [PLAYER, ZOMBIE]:
            # calling the super class function to handle entities
            # other than zombie and player
            # becaues they are same as before
            return super().create_entity(token)

        elif token == PLAYER:
            # create a instance of vulnerable player instead of simple player
            return VulnerablePlayer()

        elif token == ZOMBIE:
            return Zombie()


class TrackingZombie(Zombie):
    """
    Inherits from Zombie
    
    The TrackingZombie is a more intelligent type of zombie which
    is able to see the player and move towards them. 
    """
    
    def step(self, position: "Position", game: "Game") -> None:
        """
        Moves the tracking zombie in the best possible direction
        to move closer to the player.

        Chooses from a list of sorted possible directiona that
        minimize the distance between the resultant position and the player

        In case of multiple directions that result in being the
        same distance from the player,
        the direction should be picked in preference order
        picking ‘W’ ﬁrst followed by ‘S’, ‘N’, and ﬁnally ‘E’.

        Checks each of the possible directions in order,
        and moves the zombie to the ﬁrst available position.

        To be available, a position must be in the bounds of the grid
        and not already contain an entity.
        
        If none of the resultant positions are available,
        do not move the zombie.

        If the position the zombie is going to move to contains the player,
        the zombie should infect the player but not move to that position.

        Parameters:
            position: The position of this zombie when
                        the step event is triggered. 
            game: The current game being played. 
            
        Examples:
            if zombie is at (1, 1), and the player is at (2, 4)

            In this situation ‘S’ and ‘E’ compete for best direction
            with a distance of 3 from the player so ‘S’ is picked,
            ‘W’ and ‘N’ are also equidistant so ‘W’ is picked,
            causing an order of ‘S’, ‘E’, ‘W’, ‘N’ to be chosen.

        """
        player_position = game.get_grid().find_player()

        offsets_list:List[Position] = [Position(0, 1), Position(0, -1),
                      Position(1, 0), Position(-1, 0)]

        # list of direction of possible offsets
        # corresponds directly to the order of offsets_list
        directions_list:List[str] = ['S','N','E','W']

        # list of distance of player when the zombie
        # moves the corresponding offset in the offsets_list
        distances_list:List[int] = []
        
        for offset in offsets_list:

            # calculating the distance using the method in Position
            distances_list.append(player_position.distance(offset.add(position)))

        # combining all the three lists together to get a single 3D list
        compressed_list: List[Position, int, str] = [list(a) for a in
                     zip(offsets_list, distances_list, directions_list)]

        # sorting the 3D list first on basic of
        # decreasing distance the second element
        # and in case of equal distance on basis of
        # increasing direction character
        compressed_list = sorted(compressed_list,key=lambda x: (-x[1], x[2]))

        # reversing the list to obtains a properly sorted list per our needs
        compressed_list.reverse()
        
        grid = game.get_grid()
        
        for i in range(len(compressed_list)):
            
            final_position = position.add(compressed_list[i][0])

            # if the final position is out of bounds try the next direction
            if grid.in_bounds(final_position) == False:
                continue

            # if no entity at final postion move the zombie
            if grid.get_entity(final_position) == None:
                grid.move_entity(position, final_position)
                return None

            # if the entity at final position is a Player
            # infect the player but do not move the zombie
            if isinstance(grid.get_entity(final_position), Player):
                game.get_player().infect()
                return None
            
        return None
    
    def display(self) -> str:
        """
        Return the character used to represent the
        tracking zombie entity in a text-based grid.
        
        A tracking zombie should be represented by the ‘T’ character.

        Examples:
            >>> tracking_zombie = TrackingZombie()
            >>> tracking_zombie.display()
            'T'
        """
        return TRACKING_ZOMBIE


class Pickup(Entity):
    """
    Inherits from Entity

    Pickup class is an abstract class.
    
    A Pickup is a special type of entity that the player is able
    to pickup and hold in their inventory.
    """
    
    remaining_steps: int = None
    
    def __init__(self):
        """
        A pickup entity initializes the lifetime of the entity
        to be equal to the maximum lifetime of that entity
        """
        if(isinstance(self, Garlic) == True):
            self.remaining_steps = LIFETIMES.get(GARLIC)

        elif(isinstance(self, Crossbow) == True):
            self.remaining_steps = LIFETIMES.get(CROSSBOW)

    def get_durability(self) -> int:
        """
        Raises NotImplementedError
        
        Return the maximum amount of steps the player is able to take
        while holding this item. After the player takes this many steps,
        the item disappears.

        The abstract Pickup class should never be placed in the grid,
        so this method should be implemented by the subclasses of Pickup only. 
        """
        raise NotImplementedError

    def get_lifetime(self) -> int:
        """
        Return the remaining steps a player can take with this instance
        of the item before the item disappears from the player’s inventory. 
        """
        return self.remaining_steps

    def hold(self) -> None:
        """
        The hold method is called on every pickup entity that the player
        is holding each time the player takes a step.

        Remaining lifetime of the pickup entity is decreased by one.
        """
        self.remaining_steps -= 1

    def __repr__(self) -> str:
        """
        Return a string that represents the entity,
        the representation contains the type of the pickup entity
        and the amount of remaining steps.

        Examples:
            >>> repr(Garlic())
            'Garlic(10)'
            >>> Crossbow().__repr__()
            'Crossbow(5)'
        """
        return self.__class__.__name__ + "(" + str(self.remaining_steps) + ")"


class Garlic(Pickup):
    """
    Inherits from Pickup

    Garlic is an entity which the player can pickup.
    
    While the player is holding a garlic entity they cannot
    be infected by a zombie.
    If they collide with a zombie while holding a garlic,
    the zombie will perish.
    """
    
    def get_durability(self) -> int:
        """
        Return the durability of a garlic.
        
        A player can only hold a garlic entity for 10 steps.

        Returns:
            10
        """
        return LIFETIMES.get(GARLIC)

    def display(self) -> str:
        """
        Return the character used to represent the
        garlic entity in a text-based grid.
        
        A garlic should be represented by the ‘G’ character.

        Examples:
            >>> garlic = Garlic()
            >>> garlic.display()
            'G'
        """
        return GARLIC

class Crossbow(Pickup):
    """
    Inherits from Pickup

    Crossbow is an entity which the player can pickup.

    While the player is holding a crossbow entity they are able
    to use the ﬁre action to launch a protectile in a given direction,
    removing the ﬁrst zombie in that direction. 
    """
    
    def get_durability(self) -> int:
        """
        Return the durability of a crossbow.
        
        A player can only hold a crossbow entity for 5 steps.

        Returns:
            5
        """
        return LIFETIMES.get(CROSSBOW)

    def display(self) -> str:
        """
        Return the character used to represent the
        crossbow entity in a text-based grid.
        
        A crossbow should be represented by the ‘C’ character.

        Examples:
            >>> crossbow = Crossbow()
            >>> crossbow.display()
            'C'
        """
        return CROSSBOW


class Inventory:
    """
    An inventory holds a collection of entities which the player can pickup,
    i.e. Pickup subclasses.

    The player is only able to hold any given item for a limited duration,
    this is the lifetime of the item.
    Once the lifetime is exceeded the item will be destroyed
    by being removed from the inventory.
    """

    # the list of items in the inventory
    items: List[Pickup] = None
    
    def __init__(self):
        """
        Initialize the inventory to contain no items
        """
        self.items = []

    def step(self) -> None:
        """
        The step method is be called every time the player steps
        as a part of the player’s step method.

        When this method is called, the lifetime of every item
        stored within the inventory decreases by one.
        Any items in the inventory that have exceeded their lifetime
        are removed.

        Examples:
            >>> inventory = Inventory()
            >>> inventory.add_item(Garlic())
            >>> inventory.add_item(Crossbow())
            >>> inventory.get_items() 
            [Garlic(10), Crossbow(5)] 
            >>> inventory.step()
            >>> inventory.get_items() 
            [Garlic(9), Crossbow(4)] 
        """
        for item in self.items:

            # holding the item for one play round
            item.hold()

            # if lifetime is over remove it from inventory
            if item.get_lifetime() <= 0:
                self.items.remove(item)
        
    def add_item(self, item: "Pickup") -> None:
        """
        This method takes a pickup entity and adds it to the inventory.

        Parameters:
            item: The pickup entity to add to the inventory. 
        """
        self.items.append(item)

    def get_items(self) -> List[Pickup]:
        """
        Return the pickup entity instances currently stored in the inventory.

        Examples:
            >>> inventory = Inventory()
            >>> inventory.get_items()
            []
            >>> inventory.add_item(Garlic())
            >>> inventory.add_item(Crossbow())
            >>> inventory.get_items()
            [Garlic(10), Crossbow(5)] 
        """
        return self.items

    def contains(self, pickup_id: str) -> bool:
        """
        Return true if the inventory contains any entities which return
        the given pickup_id from the entity’s display method.

        Examples:
            >>> inventory = Inventory()
            >>> inventory.add_item(Garlic())
            >>> inventory.contains("C")
            False
            >>> inventory.contains("G")
            True
        """
        for item in self.items:
            if pickup_id == item.display():
                return True
        return False

class HoldingPlayer(VulnerablePlayer):
    """
    Inherits from VulnerablePlayer

    The HoldingPlayer is a subclass of VulnerablePlayer
    that extends the existing functionality of the player.

    In particular, a holding player will now keep an inventory. 
    """

    inventory:Inventory = None

    def __init__(self):
        """
        Initializing the inventory to a new instance
        """
        super().__init__()
        self.inventory = Inventory()
        
    def get_inventory(self) -> Inventory:
        """
        Return the instance of the Inventory class that represents
        the player’s inventory. 
        """
        return self.inventory

    def infect(self) -> None:
        """
        Extends the existing infect method so that the player
        is immune to becoming infected if they are holding garlic. 
        """
        if(self.inventory.contains(GARLIC)):
            return None

        # calling the super class infect method
        super().infect()


    def step(self, position: "Position", game: "Game") -> None:
        """
        The step method for a holding player will notify its inventory
        that a step event has occurred.

        Parameters:
            position: The position of this entity when the step event
                        is triggered.
            game: The current game being played.

        """
        self.inventory.step()


class AdvancedGame(IntermediateGame):
    """
    Inherits from IntermediateGame

    The AdvancedGame class extends IntermediateGame to add support
    for the player picking up a Pickup item when they come into contact with it. 
    """
    
    def move_player(self, offset: "Position") -> None:
        """
        Move the player entity in the grid by a given oﬀset.

        If the player moves onto a Pickup item,
        it should be added to the player’s inventory
        and removed from the grid.

        Parameters:
            offset: A position to add to the player’s current position
                    to produce the player’s new desired position.

        """
        start_position = self.grid.find_player()
        end_position = start_position.add(offset)

        entity_endpos = self.grid.get_entity(end_position)

        # if the entity at the ending position is pickable
        if isinstance(entity_endpos, Pickup) == True:

            # add it to the inventory of player
            self.get_player().get_inventory().add_item(entity_endpos)

        self.grid.move_entity(start_position, end_position)


class AdvancedMapLoader(IntermediateMapLoader):
    """
    Inherits from IntermediateMapLoader

    The AdvancedMapLoader class extends IntermediateMapLoader
    to add support for new entities

    When a player token, ‘P’, is found, a HoldingPlayer
    instance should be created instead of a Player or a VulnerablePlayer.

    In addition to the entities handled by the IntermediateMapLoader,
    the AdvancedMapLoader should be able to load the following entities:
        TrackingZombie
        Garlic
        Crossbow

    """
    
    def create_entity(self, token: str) -> Entity:
        """
        Create and return a new instance of the
        Entity class based on the provided token.
        
        The AdvancedMapLoader class supports all the entity types.

        Raise ValueError if a token not representing Hospital, Player,
        Zombie, TrackingZombie, Garlic or Crossbow is recieved
        """
        if token not in [PLAYER, TRACKING_ZOMBIE, GARLIC, CROSSBOW]:
            # call the superclass create_entity method
            return super().create_entity(token)

        elif token == PLAYER:
            return HoldingPlayer()

        elif token == TRACKING_ZOMBIE:
            return TrackingZombie()

        elif token == GARLIC:
            return Garlic()

        elif token == CROSSBOW:
            return Crossbow()


class AdvancedTextInterface(TextInterface):
    """
    Inherits from TextInterface

    A text-based interface between the user and the game instance.

    This class extends the existing functionality of TextInterface
    to include displaying the state of the player’s inventory
    and a firing action. 
    """
    
    def draw(self, game: "Game") -> None:
        """
        The draw method should print out the given game
        surrounded by ‘#’ characters representing the border of the game.

        This method should behave in the same way as the super class
        except if a player is currently holding items in their inventory.

        If the player is holding items in their inventory,
        ‘The player is currently holding:’ should be printed
        after the grid, followed by the representation of
        each item in the inventory on separate lines.
        
        Examples:
            >>> grid = Grid(4)
            >>> grid.add_entity(Position(2, 2), HoldingPlayer())
            >>> game = Game(grid)
            >>> interface = AdvancedTextInterface(4)
            >>> game.get_player().get_inventory().add_item(Garlic())
            >>> game.get_player().get_inventory().add_item(Crossbow())
            >>> interface.draw(game)
            ######
            #    #
            #    #
            #  P #
            #    #
            ######
            The player is currently holding:
            Garlic(10)
            Crossbow(5)
        """
        # calling the super class draw method for basic map drawing
        super().draw(game)

        # getting the items in the players inventory
        inventory_items = game.get_player().get_inventory().get_items()

        if len(inventory_items) != 0:

            print(HOLDING_MESSAGE)

            for item in inventory_items:
                # printing the representation of items
                print(repr(item))

    def handle_action(self, game: "Game", action: str) -> None:
        """
        The handle_action method for AdvancedTextInterface extends
        the interface to be able to handle the ﬁre action for a crossbow.

        If the user enters, ‘F’ for fire method takes the following actions:
            1. Checks that the user has something to ﬁre,
            if they do not hold a crossbow,
            prints ‘You are not holding anything to ﬁre!’

            2. Prompts the user to enter a direction in which to ﬁre,
            with ‘Direction to ﬁre: ’

            3. If the direction is not one of ‘W’, ‘A’, ‘S’ or ‘D’,
            prints ‘Invalid ﬁring direction entered!’

            4. Find the ﬁrst entity, starting from the player’s position
            in the direction speciﬁed.

            5. If there are no entities in that direction,
            or if the ﬁrst entity is not a zombie,
            (zombies include tracking zombies), then prints
            ‘No zombie in that direction!’

            6. If the ﬁrst entity in that direction is a zombie,
            removes the zombie.

            7. Triggers the step event.

        If 'F' is not the action i.e. the action is not fire, this method
        behaves the same as superclass handle_action method

        Parameters:
            game: The game that is currently being played.
            action: An action entered by the player during the game loop.
        """

        # the game grid
        grid = game.get_grid()
        # the position at which currently checking for an entity
        current_position = grid.find_player()
        # the game player
        player = game.get_player()
        # the player inventory
        inventory = player.get_inventory()

        
        if action == FIRE:
            
            if inventory.contains(CROSSBOW) == True:

                # getting the user input for the direction to fire
                fire_direction = input(FIRE_PROMPT)

                # If the direction is not one of ‘W’, ‘A’, ‘S’ or ‘D’
                if fire_direction not in DIRECTIONS:
                    print(INVALID_FIRING_MESSAGE)

                # If the firing direction is valid
                else:

                    # finding the first entity starting from the player position
                    # in the fire direction
                    while True:
                        
                        offset = game.direction_to_offset(fire_direction)

                        # updating the current position by adding to it the offset
                        current_position = current_position.add(offset)

                        # if the current position has gotten out of bounds
                        # print the ‘No zombie in that direction!’ message
                        # and break out of loop
                        if grid.in_bounds(current_position) == False:
                            print(NO_ZOMBIE_MESSAGE)
                            break

                        # the entity at the current position
                        entity = grid.get_entity(current_position)

                        # if the entity is either a Zombie or a Tracking Zombie
                        # remove the zombie from the grid
                        # and break out of loop
                        if isinstance(entity, Zombie) or isinstance(entity, TrackingZombie):
                            grid.remove_entity(current_position)
                            break

                        # if the entity is not a Zombie neither a Tracking Zombie
                        # but is also not None means the first entity in the
                        # firing direction is not a Zombie
                        # print the ‘No zombie in that direction!’ message
                        # and break out of loop
                        elif entity != None:
                            print(NO_ZOMBIE_MESSAGE)
                            break

            # if the player does not have crossbow in inventory
            else:
                print(NO_WEAPON_MESSAGE)

            # informing game that a step has occured
            game.step()

        # if the action is not fire
        else:
            # calling the superclass handle_action method
            super().handle_action(game, action)
            
def main():
    """Entry point to gameplay."""
    print("Zombie Survival Game")

    # taking user input for map choice
    mapFile = input("Map: ")

    # creating a new grid with advanced map loader and inputted mapfile path
    grid = AdvancedMapLoader().load(mapFile)

    # validating the precondition for the Game constructor
    # that a player must exist in the grid
    if grid.find_player() == None:
        raise ValueError

    #  creating a new game from grid instance  
    game = AdvancedGame(grid)

    # creating a new AdvancedTextInterface with the size of the grid
    interface = AdvancedTextInterface(grid.get_size())

    # playing the game
    interface.play(game)
    
if __name__ == "__main__":
    main()
