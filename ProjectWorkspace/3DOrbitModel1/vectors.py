import math
class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y 
        self.z = z

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'

    def __str__(self):
        return f'{self.x:.3f}i + {self.y:.3f}j + {self.z:.3f}k'
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        else:
            raise IndexError('Index out of range')

    def __add__(self, other):
        return Vector(
            self.x + other.x, 
            self.y + other.y, 
            self.z + other.z
        ) 
    
    def __sub__(self, other):
        return Vector(
            self.x - other.x, 
            self.y - other.y, 
            self.z - other.z
        )
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                self.x * other, 
                self.y * other, 
                self.z * other
            )
        elif isinstance(other, Vector):
            return Vector(
                self.x * other.x, 
                self.y * other.y, 
                self.z * other.z
            )       
        else:
            raise TypeError('Multiplication not \
                            supported for this type')
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(
                self.x / other, 
                self.y / other, 
                self.z / other
            )
        else:
            raise TypeError('Division not supported for this type')

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm(self):
        magnitude = self.mag()
        if magnitude == 0:
            raise ZeroDivisionError('Cannot normalize the zero vector')
        return self / magnitude
    
