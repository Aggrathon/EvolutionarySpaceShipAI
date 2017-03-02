import race
import vector

class EasyAI(race.BaseAI):

	def __init__(self):
		super().__init__()
		self.color = (0, 128, 255)

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.normalize(self.velocity)
		return vector.normalize(vector.sub(dir, stop))


class DragAI(race.BaseAI):

	def __init__(self, scale : float = 1.0):
		super().__init__()
		self.color = (255, 0, 128 + (scale-1)*40)
		self.scale = scale

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.mult(self.velocity, self.scale)
		return vector.normalize(vector.sub(dir, stop))

	def __repr__(self):
		return "DragAI (%.1f)" % self.scale
	
class PerpAI(race.BaseAI):

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.mult(vector.sub(self.velocity, vector.along(self.velocity, dir)), vector.length(self.velocity)*2)
		return vector.normalize(vector.sub(dir, stop))


class CombinedAI(race.BaseAI):

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.sub(self.velocity, vector.mult(vector.along(self.velocity, dir), 0.25))
		return vector.normalize(vector.sub(dir, stop))


class StoppingAI(race.BaseAI):

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.sub(self.velocity, vector.mult(vector.along(self.velocity, dir), 0.25))
		if vector.sqr_distance(self.position, goal) < 0.2:
			return vector.normalize(vector.sub(vector.sub(dir, stop), self.velocity))
		return vector.normalize(vector.sub(dir, stop))


class TweakedAI(race.BaseAI):

	def __init__(self, scale: float = 1.0):
		super().__init__()
		self.color = (40*scale, 0, 255)
		self.scale = scale

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.normalize(self.velocity)
		stop = vector.mult(stop, vector.dot(stop, dir)*self.scale)
		return vector.normalize(vector.sub(dir, stop))
	
	def __repr__(self):
		return "TweakedAI (%.1f)" % self.scale


if __name__ == "__main__":
	r = race.Race(time = 40)
	r.add_racer(EasyAI())
	r.add_racer(DragAI(1))
	r.add_racer(DragAI(2))
	r.add_racer(PerpAI())
	r.add_racer(CombinedAI())
	r.add_racer(StoppingAI())
	r.add_racer(TweakedAI(1))
	r.start_pygame_race()


