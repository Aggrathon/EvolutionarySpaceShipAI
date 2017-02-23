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
		self.color = (128, 0, 255)

	def evaluate(self, goal, goal2):
		dir = vector.normalize(vector.from_to(self.position, goal))
		stop = vector.normalize(self.velocity)
		stop = vector.mult(stop, vector.dot(stop, dir))
		return vector.normalize(vector.sub(dir, stop))


if __name__ == "__main__":
	r = Race.Race()
	r.add_racer(EasyAI())
	r.add_racer(FasterAI())
	r.start_pygame_race()


