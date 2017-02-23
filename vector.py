import math

def length(vec):
	return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

def sqr_distance(vector1, vector2):
	dx = vector1[0]-vector2[0]
	dy = vector1[1]-vector2[1]
	return dx*dx+dy*dy

def from_to(vec_from, vec_to):
	return sub(vec_to, vec_from)

def normalize(vec):
	vlen = length(vec)
	if vlen == 0:
		return vec
	return (vec[0]/vlen, vec[1]/vlen)

def limit(vec, limit: float):
	vlen = length(vec)
	if vlen > limit:
		scale = limit/vlen
		return (vec[0]*scale, vec[1]*scale)
	return vec

def add(vec1, vec2):
	return (vec1[0]+vec2[0], vec1[1]+vec2[1])

def sub(vec1, vec2):
	return (vec1[0]-vec2[0], vec1[1]-vec2[1])

def mult(vec, scalar):
	return (vec[0]*scalar, vec[1]*scalar)

def dot(vec1, vec2):
	return vec1[0]*vec2[0] + vec1[1]*vec2[1]
