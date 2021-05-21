from math import sqrt

class Coordinates:
    def __init__(self, x = None, y = None, z = None):
        self.x, self.y, self.z = None, None, None
        self.update(x, y, z)

    def update(self, x = None, y = None, z = None):
        if x is not None:
            self.x = self.parse_value(x)

        if y is not None:
            self.y = self.parse_value(y)
        
        if z is not None:
            self.z = self.parse_value(z)

    def is_relative(self, c):
        if type(c) is Coordinates:
            return self.is_relative(c.x) or self.is_relative(c.y) or self.is_relative(c.z)
        else:
            return (type(c) is str) or (c is None)
    
    def has_absolute(self):
        return (not self.is_relative(self.x)) or (not self.is_relative(self.y)) or (not self.is_relative(self.z))

    def parse_value(self, x):
        if x is None:
            return 0

        try:
            num = float(x)

            if num.is_integer():
                return int(num)
            else:
                return num
        except:
            return x
            
    def parse_relative(self, x):
        if x is None:
            return 0

        if type(x) is not str:
            return x

        snum = x[1:]
        if snum:
            return self.parse_value(snum)
        else:
            return 0

    def merge(self, other):
        ## You can't merge onto relative coordinates
        if self.is_relative(self):
            return False
        
        ## If the other coordinates are undefined
        if other is None:
            return self

        new_x = self.x
        new_y = self.y
        new_z = self.z

        if self.is_relative(other.x):
            new_x += self.parse_relative(other.x)
        else:
            new_x = other.x

        if self.is_relative(other.y):
            new_y += self.parse_relative(other.y)
        else:
            new_y = other.y

        if self.is_relative(other.z):
            new_z += self.parse_relative(other.z)
        else:
            new_z = other.z

        return Coordinates(new_x, new_y, new_z)
    
    def round(self):
        return Coordinates(int(self.x), int(self.y), int(self.z))
    
    def tuple(self):
        return (self.x, self.y, self.z)

    def distance(self, other):
        d = (self.x - other.x) ** 2
        d += (self.y - other.y) ** 2
        d += (self.z - other.z) ** 2
        return sqrt(d)

    def between(self, x1, x2, x):
        return min(x1, x2) <= x <= max(x1, x2)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.tuple())
    
    def __str__(self):
        return str(self.tuple())