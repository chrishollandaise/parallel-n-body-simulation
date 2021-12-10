from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.config import Config
import pickle
import os
from kivy.clock import Clock

class MainCanvas(Widget):
        
    def __init__(self, **kwargs):
        super(MainCanvas, self).__init__(**kwargs)
        self.load()
        # used to iterate through the epochs
        self.inc = 0

        with self.canvas.before:
            # initialize the ellipses to their first positions
            self.particles = [Ellipse(size=(40, 40),pos=(nbody[0], nbody[1])) for nbody in self.epochs[0]]
 
        with self.canvas:
            Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        iter = self.inc % len(self.epochs)

        # update the positions of the ellipses
        for idx, particle in enumerate(self.particles):
            particle.pos = (self.epochs[iter][idx][0], self.epochs[iter][idx][1])
        
        # next epoch
        self.inc += 1    

    def load(self):
        self.epochs = pickle.load(open(os.path.join(os.getcwd(), 'profiles/1000steps_2_particles_2500spe.pkl'), 'rb')) 
        

class MainApp(App):
    def build(self):
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'width', '720')
        Config.set('graphics', 'height', '480')
        self.title = 'N-Body Simulator'

def main():
    app = MainApp()
    app.run()

if __name__ == '__main__':
    main()