import Race
import vector

class EasyAI(Race.BaseAI):

	def __init__(self):
		super().__init__()
		self.color = (0, 128, 255)

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.normalize(self.velocity)
		return vector.normalize(vector.sub(dir, stop))


class FasterAI(Race.BaseAI):

	def __init__(self):
		super().__init__()
		self.color = (255, 0, 128)

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.limit(self.velocity, 1.0)
		return vector.normalize(vector.sub(dir, stop))


class TweakedAI(Race.BaseAI):

	def __init__(self, scale: float = 1.0):
		super().__init__()
		self.color = (40*scale, 0, 255)
		self.scale = scale

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.normalize(self.velocity)
		stop = vector.mult(stop, vector.dot(stop, dir)*self.scale)
		return vector.normalize(vector.sub(dir, stop))


if __name__ == "__main__":
	r = Race.Race()
	r.add_racer(EasyAI())
	r.add_racer(FasterAI())
	r.add_racer(TweakedAI(2))
	r.add_racer(TweakedAI(1))
	r.start_pygame_race()


