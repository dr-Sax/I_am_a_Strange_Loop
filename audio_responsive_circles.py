from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh

from geometry.polygonGeometry import PolygonGeometry

from material.surfaceMaterial import SurfaceMaterial

from audio.audio_stream_rt import AudioBuffer

from OpenGL.GL import *
import numpy as np
from scipy.fft import fft, fftfreq

Z = 20  # Sets camera distance away from xy plane
R_MAX = 10
EXPANSION_FACTOR = 50

# render a basic scene
class Test(Base):

    def initialize(self):

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 1)
        self.camera.setPosition([0, 0, Z])
        self.audio_buffer = AudioBuffer(chunks=10)
        self.audio_buffer.start()

        vsCode = '''
            in vec3 vertexPosition;
            out vec3 position;
            uniform mat4 modelMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 projectionMatrix;
            void main()
            {
                vec4 pos = vec4(vertexPosition, 1.0);
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
                position = vertexPosition;
            }
        '''

        self.geometry = PolygonGeometry(sides = 100, radius = 1)
        self.material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': GL_LINE_STRIP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [1.0, 1.0, 1.0]
        )


        self.circle_mesh = []
        self.circle_freq = []
        self.circle_iter = []

        self.renderer.render(self.scene, self.camera) 

        
    def get_max_freq(self):
        data = self.audio_buffer()
        yf = fft(data)
        xf = fftfreq(len(data), 1 / self.audio_buffer.RATE)
        peak_index = np.argmax(yf)
        read_freq = xf[peak_index]
        return read_freq
    
    def in_range(self, freq, min, max):
        if freq >= min and freq <= max:
            return True
        else:
            return False


    def update(self):  
        removal_index = []
        peak_freq = self.get_max_freq()

        if self.in_range(peak_freq, 100, 660): # to add a new_circle to the list
            temp_mesh = Mesh(self.geometry, self.material)
            self.circle_mesh.append(temp_mesh)
            self.circle_freq.append(peak_freq)
            self.circle_iter.append(0)
            self.scene.add(temp_mesh)

        for circ_n in range(0, len(self.circle_mesh)): # advance existing circles based on their pitch, and remove those off screen

            freq = self.circle_freq[circ_n]
            iter = self.circle_iter[circ_n]
            mesh = self.circle_mesh[circ_n]

            new_radius = iter * (1 / freq) * EXPANSION_FACTOR

            try:
                self.scene.remove(mesh)
            except:
                pass

            if new_radius >= R_MAX:  # circle is off-screen
                removal_index.append(circ_n)

            else:
                new_iter = iter + 1
                new_mesh = Mesh(PolygonGeometry(sides = 100, radius = new_radius), self.material)

                self.circle_iter[circ_n] = new_iter
                self.circle_mesh[circ_n] = new_mesh
                self.scene.add(new_mesh)

        for i in removal_index:
            del self.circle_mesh[i]
            del self.circle_freq[i]
            del self.circle_iter[i]

        self.renderer.render(self.scene, self.camera) 
            
# instantiate this class and run the program
Test(screenSize = [1300, 1300]).run()
