from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.config import Config
import pickle
import os
from kivy.clock import Clock
from kivy.graphics.transformation import Matrix

class Simulation(Scatter):
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.scale = self.scale * 1.1
            elif touch.button == 'scrollup':
                self.scale = self.scale * 0.9
        else:
            super(Simulation, self).on_touch_down(touch)
    
    def __init__(self, **kwargs):
        super(Simulation, self).__init__(**kwargs)
        self.load()
        # used to iterate through the epochs
        self.inc = 0
        self.PARTICLE_SIZE = 10

        with self.canvas.before:
            # initialize the ellipses to their first positions
            self.particles = [Ellipse(size=(self.PARTICLE_SIZE, self.PARTICLE_SIZE),pos=(nbody[0], nbody[1])) for nbody in self.epochs[0]]

        with self.canvas:
            Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        iter = self.inc % len(self.epochs)

        # update the positions of the ellipses
        for idx, particle in enumerate(self.particles):
            particle.size = (self.PARTICLE_SIZE / self.scale, self.PARTICLE_SIZE / self.scale)
            particle.pos = (self.epochs[iter][idx][0], self.epochs[iter][idx][1])
        
        # next epoch
        self.inc += 1    

    def load(self):
        self.epochs = pickle.load(open(os.path.join(os.getcwd(), r'C:\Users\Chris\code\parallel-n-body-simulation\profiles\1000steps_10_particles_2500spe.pkl'), 'rb')) 

class MainApp(App):
    def build(self):
        # Configure the window
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', '1920')
        Config.set('graphics', 'height', '1080')

        self.title = 'N-Body Simulator'

        # Designate design file
        # Builder.load_file('scripts/gui.kv')
        
        return Simulation()

if __name__ == '__main__':
    MainApp().run()