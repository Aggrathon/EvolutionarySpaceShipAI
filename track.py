import random
import itertools
import math
import pygame
import vector

def circle_permutations(coll):
	for perm in itertools.permutations(coll[1:]):
		yield perm+(coll[0],)

def track_length(track, angle_weight : float):
	nlen = 0.0
	for i in range(len(track)):
		dx1 = track[i][0]-track[i-1][0]
		dy1 = track[i][1]-track[i-1][1]
		dx2 = track[i][0]-track[(i+1)%len(track)][0]
		dy2 = track[i][1]-track[(i+1)%len(track)][1]
		len1 = math.sqrt(dx1*dx1+dy1*dy1)
		len2 = math.sqrt(dx2*dx2+dy2*dy2)
		multlen = len1*len2
		if multlen == 0: multlen = 1
		try:
			angle = 1.0-math.acos((dx1*dx2+dy1*dy2)/multlen)/math.pi
		except ValueError:
			angle = 1.0
		nlen += len1 + (angle*0.55-0.05)*(angle*0.55-0.05)*4*angle_weight
	return nlen

def search_shorter_track(track, angle_weight : float):
	if len(track) < 10:
		return tsp_exact(track, angle_weight)
	else:
		return tsp_2opt(track, angle_weight)

def tsp_exact(track, angle_weight: float):
	points = track
	shortest = float("inf")
	for perm in circle_permutations(track):
		nlen = track_length(perm, angle_weight)
		if nlen < shortest:
			shortest = nlen
			points = perm
	return points

def tsp_2opt(track, angle_weight: float):
	points = track
	shortest = track_length(track, angle_weight)
	for its in range(int(math.sqrt(len(points))*3)):
		print("Search step %d"%its)
		track, nlen = __tsp_2opt__(track, angle_weight, 2)
		if nlen < shortest:
			points = track
		else:
			break
	return points

def __tsp_2opt__(track, angle_weight : float, depth : int = 2):
	if depth == 0:
		return track, track_length(track, angle_weight)
	length = len(track)
	strack = track
	shortest = track_length(track, angle_weight)
	for i in range(0,length):
		for j in range(i+1,length+1):
			ntrack = track[:i]+[x for x in reversed(track[i:j])]+track[j:]
			nlen = track_length(ntrack, angle_weight)
			if nlen < shortest + 0.5*angle_weight:
				ntrack, nlen = __tsp_2opt__(ntrack, angle_weight, depth -1)
				if nlen < shortest:
					shortest = nlen
					strack = ntrack
	return strack, shortest


class Track(object):
	points = []
	scale = 1.0
	length = 0

	def __init__(self, scale : float = 1.0, points : int = 10, track_optimizer=search_shorter_track):
		self.scale = scale*points/10
		self.length = points
		if points == 0:
			self.points = []
		else:
			if track_optimizer is None:
				self.points = self.__generate_points__(points)
			else:
				self.points = track_optimizer(self.__generate_points__(points), self.scale)

	def set_points(self, points, scale: float = 0.0):
		if scale == 0.0:
			for p in points:
				if p[0] > scale: scale = p[0]
				if -p[0] > scale: scale = -p[0]
				if p[1] > scale: scale = p[1]
				if -p[1] > scale: scale = -p[1]
		self.scale = scale
		self.length = len(points)
		self.points = points

	def __generate_points__(self, num : int = 8, arr = []):
		if num == 0:
			return arr
		point = (random.random()*self.scale, random.random()*self.scale)
		limit = (self.scale / self.length)*(self.scale / self.length)
		for p in arr:
			if vector.sqr_distance(point, p) < limit:
				return self.__generate_points__(num, arr)
		arr.append(point)
		return self.__generate_points__(num-1, arr)

	def draw_track(self, screen, size):
		screen.fill((255,255,255))
		oldp = (int(self.points[-1][0]*size), int(self.points[-1][1]*size))
		for p in self.points:
			newp = (int(p[0]*size), int(p[1]*size))
			pygame.draw.circle(screen, (0,255,0), newp, 8, 4)
			pygame.draw.line(screen, (64,64,64), newp, oldp, 2)
			oldp = newp

	def show_track(self):
		pygame.init()
		screen = pygame.display.set_mode((600,600))
		self.draw_track(screen, 600//self.scale)
		pygame.display.update()
		while (True):
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					pygame.quit()
					return


if __name__ == "__main__":
	t = Track(1.0,30)
	print("Track generated")
	t.show_track()