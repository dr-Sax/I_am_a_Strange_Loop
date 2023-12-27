from geometry.geometry import Geometry
from math import sin, cos, pi
import numpy as np

class PolygonGeometry(Geometry):

    def __init__(self, sides = 3, radius = 1, x = 0, y = 0, theta1 = 0, theta2 = 2 * np.pi):
        super().__init__()

        A = 2 * np.pi / sides
        n1 = theta1 / (2 * np.pi) * sides
        n2 = theta2 / (2 * np.pi) * sides
        positionData = []
        colorData = []
        
        uvData = []
        uvCenter = [0.5, 0.5]

        for n in np.arange(n1, n2 + 1):
            #positionData.append([0, 0, 0])
            positionData.append([radius * np.cos(n * A) + x, radius * np.sin(n * A) + y, 0])
            positionData.append([radius * np.cos((n + 1) * A) + x, radius * np.sin((n + 1) * A) + y, 0])
            colorData.append([1, 1, 1])
            colorData.append([1, 0, 0])
            colorData.append([0, 0, 1])

            # texture:
            uvData.append(uvCenter)
            uvData.append(
                [
                    np.cos(n * A) * 0.5 + 0.5,
                    np.sin(n * A) * 0.5 + 0.5,
                ]
            )
            uvData.append(
                [
                    np.cos((n + 1) * A) * 0.5 + 0.5,
                    np.sin((n + 1) * A) * 0.5 + 0.5,
                ]
            )
        
        self.addAttribute('vec3', 'vertexPosition', positionData)
        self.addAttribute('vec3', 'vertexColor', colorData)
        self.addAttribute('vec2', 'vertexUV', uvData)
        self.countVertices()
