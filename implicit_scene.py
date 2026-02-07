from src.base import BaseScene, Color
from src.shapes import ImplicitFunction

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Implicit Scene")
        self.background = Color(1, 1, 0)
        
        #2.

        def function_naive(x,y):
            return (0.004 + 0.110*x - 0.177*y - 0.174*x**2 + 0.224*x*y - 0.303*y**2 - 0.168*x**3 + 0.327*x**2*y - 0.087*x*y**2 - 0.013*y**3 + 0.235*x**4 - 0.667*x**3*y + 0.745*x**2*y**2 - 0.029*x*y**3 + 0.072*y**4)
        
        def function_horner(x,y):
            #using Horner's Scheme

            p4 = 0.235
            p3 = -0.168 - 0.667 * y
            p2 = -0.174 + y * (0.327 + 0.745 * y)
            p1 = 0.110 + y * (0.224 + y * (-0.087 - 0.029 * y))
            p0 = 0.004 + y * (-0.177 + y * (-0.303 + y * (-0.013 + 0.072 * y)))

            # Regra de Horner para a variável x
            return p0 + x * (p1 + x * (p2 + x * (p3 + x * p4)))

        # Add some triangles to the scene
        self.add(ImplicitFunction(function_naive), Color(0.0, 0.0, 1.0))  # Yellow function
