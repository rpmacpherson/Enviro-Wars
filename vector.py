###############################VECTOR MATH######################################
class Vector(object):
    def __init__(self,x=0.0,y=0.0):
        self.x=x
        self.y=y
    def __str__(self):
        return "(%s,%s)"%(self.x,self.y)
    @staticmethod
    def from_points(p1,p2):
        return Vector(p2[0]-p1[0],p2[1]-p1[1])
    def get_magnitude(self):
        return math.sqrt(self.x**2+self.y**2)
    def __mul__(self,scalar):
        return Vector(self.x*scalar,self.y*scalar)