import random
import itertools
import math
import pygame

def circle_permutations(coll):
	for perm in itertools.permutations(coll[1:]):
		yield perm+(coll[0],)

def track_length(track, angle_weight):
	nlen = 0.0
	for i in range(len(track)):
		dx1 = track[i][0]-track[i-1][0]
		dy1 = track[i][1]-track[i-1][1]
		dx2 = track[i][0]-track[(i+1)%len(track)][0]
		dy2 = track[i][1]-track[(i+1)%len(track)][1]
		len1 = math.sqrt(dx1*dx1+dy1*dy1)
		len2 = math.sqrt(dx2*dx2+dy2*dy2)
		angle = 1.0-math.acos((dx1*dx2+dy1*dy2)/(len2*len1))/math.pi
		nlen += len1 + (angle*0.55-0.05)*(angle*0.55-0.05)*4*angle_weight
	return nlen


class Track(object):
	points = []
	scale = 1.0

	def __init__(self, scale : float = 1.0, points : int = 10, later_points : int = 3):
		self.scale = scale
		point_list = [(random.random()*scale, random.random()*scale) for i in range(points)]
		length = 99999999.0
		for perm in circle_permutations(point_list[:-later_points]):
			nlen = track_length(perm, scale)
			if nlen < length:
				length = nlen
				self.points = perm
		for i in range(later_points):
			point = point_list[i-later_points]
			new_points = self.points
			length = 99999999.0
			for i in range(len(self.points)):
				track = self.points[:i]+(point,)+self.points[i:]
				nlen = track_length(track, scale*2)
				if nlen < length:
					new_points = track
					length = nlen
			self.points = new_points

	def draw_track(self, screen, size):
		screen.fill((255,255,255))
		oldp = (int(self.points[-1][0]*size), int(self.points[-1][1]*size))
		for p in self.points:
			newp = (int(p[0]*size), int(p[1]*size))
			pygame.draw.circle(screen, (0,255,0), newp, 8, 4)
			pygame.draw.line(screen, (255,0,0), newp, oldp, 2)
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
	t = Track(1.0,10,3)
	print("Track generated")
	t.show_track()