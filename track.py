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
		if len1 == 0: len1 = 1
		if len2 == 0: len2 = 1
		angle = 1.0-math.acos((dx1*dx2+dy1*dy2)/(len2*len1))/math.pi
		nlen += len1 + (angle*0.55-0.05)*(angle*0.55-0.05)*4*angle_weight
	return nlen

def search_shorter_track(track, angle_weight : float, depth : int = 2):
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
				ntrack, nlen = search_shorter_track(ntrack, angle_weight, depth -1)
				if nlen < shortest:
					shortest = nlen
					strack = ntrack
	return strack, shortest


class Track(object):
	points = []
	scale = 1.0
	length = 0

	def __init__(self, scale : float = 1.0, points : int = 10):
		self.scale = scale*points/10
		self.length = points
		if points < 10:
			length = self.__generate_short_track__(points)
		elif points < 16:
			flen = points - points//3
			slen = points//3
			self.__generate_short_track__(flen)
			self.__generate_additional_track__(slen)
		else:
			self.__generate_long_track_fast__(points)
	
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
	
	def __generate_short_track__(self, length : int = 8):
		point_list = self.__generate_points__(length)
		shortest = 5*self.scale*length
		for perm in circle_permutations(point_list):
			nlen = track_length(perm, self.scale)
			if nlen < shortest:
				shortest = nlen
				self.points = perm
	
	def __generate_additional_track__(self, num : int = 3):
		point_list = self.__generate_points__(num, [p for p in self.points])[len(self.points):]
		for point in point_list:
			new_points = (point,)+self.points
			length = track_length(new_points, self.scale*2)
			for i in range(1, len(self.points)):
				track = self.points[:i]+(point,)+self.points[i:]
				nlen = track_length(track, self.scale*2)
				if nlen < length:
					new_points = track
					length = nlen
			self.points = new_points
	
	def __generate_long_track_bad__(self, length : int = 20):
		points = self.__generate_points__(length)
		track = points
		shortest = track_length(points, self.scale)*2
		for its in range(length):
			index = 0
			for i in range(0,length):
				for j in range(i,length):
					ntrack = points[:i]+points[j:j+1]+points[i+1:j]+points[i:i+1]+points[j+1:]
					nlen = track_length(ntrack, self.scale)
					if nlen < shortest:
						shortest = nlen
						index = i
						track = ntrack
			if index != 0:
				points = track
			else:
				break
		self.points = track
				
	def __generate_long_track_fast__(self, length : int = 20):
		points = self.__generate_points__(length)
		shortest = track_length(points, self.scale)
		for its in range(length//2):
			print("Search step %d"%its)
			track, nlen = search_shorter_track(points, self.scale, 2)
			if nlen < shortest:
				points = track
			else:
				print(its)
				break
		self.points = points


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