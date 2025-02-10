class Ball():
    def __init__(self, radius, color, player_pos : pygame.Vector2):
        self._radius = radius
        self._color = color
        # center of the ball
        self._player_pos = player_pos
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color

    @property
    def player_pos(self):
        return self._player_pos
    
    @player_pos.setter
    def player_pos(self, player_pos):
        self._player_pos = player_pos
