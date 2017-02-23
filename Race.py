from Track import Track
import pygame
import random

def sqr_distance(vector1, vector2):
	dx = vector1[0]-vector2[0]
	dy = vector1[1]-vector2[1]
	return dx*dx+dy*dy

class BaseAI(object):
	position = (0.0, 0.0)
	velocity = (0.0, 0.0)
	color = (0,0,255)

	def evaluate(goalx, goaly):
		return (random.random()*2-1, random.random()*2-1)
	
	def add_score(score : float):
		pass
	
	def draw(self, screen, size):
		startpos = (int(self.position[0]*size), int(self.position[1]*size))
		endpos = (int((self.position[0]+self.velocity[0])*size), int((self.position[1]+self.velocity[1])*size))
		pygame.draw.circle(screen, self.color, startpos, 4, 2)
		pygame.draw.line(screen, self.color, startpos, endpos, 2)

class Race(object):

	def __init__(self, scale : float = 10.0, steps : int = 10, time : float = 10.0, racers = []):
		self.racers = racers
		self.track = Track(scale)
		self.time_steps = steps
		self.time_limit = time
		self.goals = []
	
	def add_racer(self, racer):
		self.racers.append(racer)
	
	def add_racers(self, racers):
		self.racers += racers
	
	def start_race(self):
		self.__init_race__()
		for i in range(0, self.time_limit, self.delta_time):
			self.__race_step__()
	
	def start_pygame_race(self):
		self.__init_race__()
		pygame.init()
		screen = pygame.display.set_mode((600,600))
		size = 600 / self.track.scale
		clock = pygame.time.Clock()
		for i in range(int(self.time_limit*self.time_steps)):
			self.__race_step__()
			self.track.draw_track(screen, size)
			for r in self.racers:
				r.draw(screen, size)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					return
			clock.tick(self.time_steps)
		pygame.quit()
	
	def __init_race__(self):
		self.goals = [0]*len(self.racers)
		for i in range(len(self.racers)):
			self.racers[i].position = self.track.points[0]
			self.racers[i].velocity = (0.0, 0.0)
	
	def __race_step__(self):
		dt = 1.0/self.time_steps
		for i, r in enumerate(self.racers):
			if sqr_distance(r.position, self.track.points[self.goals[i]]) < 0.1:
				self.goals[i] = (self.goals[i]+1)%len(self.track.points)
			dx, dy = r.evaluate(self.track.points[self.goals[i]])
			r.velocity = (r.velocity[0]+dx*dt, r.velocity[1]+dy*dt)
			r.position = (r.position[0] +r.velocity[0]*dt, r.position[1]+r.velocity[1]*dt)
			

if __name__ == "__main__":
	race = Race()
	race.add_racers([BaseAI(),BaseAI(),BaseAI(),BaseAI(),BaseAI()])
	race.start_pygame_race()