from .base import Shape

class Circle(Shape):
    def __init__(self, center, radius):
        super().__init__("circle")
        self.center = center
        self.radius = radius

    def in_out(self, point):
        dx = point[0] - self.center[0]
        dy = point[1] - self.center[1]
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

class Triangle(Shape):
    def __init__(self, vertex1, vertex2, vertex3):
        super().__init__("triangle")
        self.v1 = vertex1
        self.v2 = vertex2
        self.v3 = vertex3

    def in_out(self, point):

        #1.1.
        '''
        #half plane algorithm 


        def sign (p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        def PointInTriangle (pt, v1, v2, v3):
            d1 = sign(pt, v1, v2)
            d2 = sign(pt, v2, v3)
            d3 = sign(pt, v3, v1)

            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

            return not (has_neg and has_pos)
        return PointInTriangle(point, self.v1, self.v2, self.v3)
        '''
        #using barycentric coordinates s and t
        #source : https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle

        triangle_area = (-self.v2[1] * self.v3[0] + self.v1[1] * (-self.v2[0] + self.v3[0]) + 
                    self.v1[0] * (self.v2[1] - self.v3[1]) + self.v2[0] * self.v3[1])
    
        s = (1 / triangle_area) * (self.v1[1] * self.v3[0] - self.v1[0] * self.v3[1] + 
                                (self.v3[1] - self.v1[1]) * point[0] + 
                                (self.v1[0] - self.v3[0]) * point[1])
        
        t = (1 / triangle_area) * (self.v1[0] * self.v2[1] - self.v1[1] * self.v2[0] + 
                                (self.v1[1] - self.v2[1]) * point[0] + 
                                (self.v2[0] - self.v1[0]) * point[1])

        return s >= 0 and t >= 0 and (s + t) <= 1
        

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point[0],point[1]) <= 0