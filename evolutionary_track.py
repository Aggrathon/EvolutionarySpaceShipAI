import track
import numpy as np
import random
import math


def generate_pop(size: int = 10):
	arr = [i for i in range(size)]
	np.random.shuffle(arr)
	return arr

def mutate_pop(pop, percentage: float = 0.2):
	pop = list(pop)
	switches = (len(pop)*percentage)
	if switches < 1: switches = 1
	for _ in range(int(switches)):
		if random.random() < 0.6:
			a = np.random.randint(0, len(pop))
			b = np.random.randint(0, len(pop)-1)
			if a == b: b = len(pop)-1
			temp = pop[a]
			pop[a] = pop[b]
			pop[b] = temp
		else:
			a = np.random.randint(0,len(pop))
			pop = pop[:a]+[i for i in reversed(pop[a:])]
	return pop

def crossover_simple(pop1, pop2):
	splitf = np.random.normal(0.4, 0.1)
	if splitf < 0.1: splitf = 0.1
	elif splitf > 0.7: splitf = 0.7
	split = int(splitf*len(pop1))
	npop1 = pop1[:split]
	for i in range(split,len(pop2)):
		x = pop2[i]
		if not x in npop1:
			npop1.append(x)
	for i in range(split):
		x = pop2[i]
		if not x in npop1:
			npop1.append(x)
		if len(npop1) == len(pop1):
			break
	npop2 = pop2[:split]
	for i in range(split,len(pop1)):
		x = pop1[i]
		if not x in npop2:
			npop2.append(x)
	for i in range(split):
		x = pop1[i]
		if not x in npop2:
			npop2.append(x)
		if len(npop2) == len(pop1):
			break
	return npop1, npop2

def crossover_dmx(pop1, pop2):
	def gen(split, pop1, pop2):
		npop = pop1[:split]
		for i in pop2[split:]:
			if i not in npop:
				npop.append(i)
		for i in pop2[:split]:
			if i not in npop:
				npop.append(i)
		return npop
	
	splitf = np.random.normal(0.4, 0.1)
	if splitf < 0.1: splitf = 0.1
	elif splitf > 0.7: splitf = 0.7
	split = int(splitf*len(pop1))
	return gen(split, pop1, pop2), gen(split, pop2, pop1)

def crossover_erx(pop1, pop2):
	for x in pop1:
		if x not in pop2:
			print("sad")
	def gen(pop1, pop2):
		npop = [random.choice(pop1)]
		for i in range(len(pop1)-1):
			poss = []
			i1 = pop1.index(npop[i])
			i2 = pop2.index(npop[i])
			if pop1[i1-1] not in npop:
				poss.append(pop1[i1-1])
			if pop1[(i1+1)%len(pop1)] not in npop:
				poss.append(pop1[(i1+1)%len(pop1)])
			if pop2[i2-1] not in npop:
				poss.append(pop2[i2-1])
			if pop2[(i2+1)%len(pop2)] not in npop:
				poss.append(pop2[(i2+1)%len(pop2)])
			if len(poss) == 0:
				for i in pop1:
					if i not in npop:
						npop.append(i)
						break
			else:
				npop.append(random.choice(poss))
		return npop
	return gen(pop1, pop2), gen(pop2, pop1)


def generate_pops(num: int = 10, size : int = 20):
	return [generate_pop(size) for _ in range(10)]

def mutate_pops(pops, percentage : float = 0.2):
	return [mutate_pop(pop, percentage) for pop in pops]

def crossover_pops(pops, method, times = 1):
	length = len(pops)-1
	result = []
	for i in range(times):
		np.random.shuffle(pops)
		for i in range(0,length,2):
			p1, p2 = method(pops[i], pops[i+1])
			result.append(p1)
			result.append(p2)
	return result

def get_track(pop, points):
	return [points[i] for i in pop]

def select_pops(pops, points, amount: int = 10, scale : float = 1.0):
	pops.sort(key=lambda p: track.track_length(get_track(p, points), scale))
	return pops[:amount]

def evolutionary_generate(points, scale, generation_size = 40, max_generations=500,
		min_improvment = 0.005, stalled_generations = 15, elitism=True):
	track_length = len(points)
	population = generate_pops(generation_size, track_length)
	best = track.track_length(get_track(population[0], points), scale)
	counter = 0
	for i in range(max_generations):
		parents = population + generate_pops(generation_size, track_length)
		pool = crossover_pops(parents, crossover_simple)
		pool += crossover_pops(parents, crossover_dmx)
		pool += crossover_pops(parents, crossover_erx)
		pool += mutate_pops(pool, 0.2)
		if elitism:
			pool += population[:generation_size//8]
		population = select_pops(pool, points, generation_size, scale)
		nb = track.track_length(get_track(population[0], points), scale)
		if best - min_improvment > nb:
			best = nb
			counter = 0
		print("Generation %d (%.2f)"%(i, nb))
		counter += 1
		if counter > stalled_generations:
			break
	return get_track(population[0], points)

if __name__ == "__main__":
	track_length = 30
	#t = track.Track(1, 0)
	#t.scale = 1
	#t.length = track_length
	#points = t.__generate_points__(track_length)
	t = track.Track(1, track_length)
	solution = evolutionary_generate(t.points, t.scale)
	print("Original Length: %.2f"%track.track_length(t.points, t.scale))
	print("Evolutionary Length: %.2f"%track.track_length(solution, t.scale))
	t.show_track()
	t.set_points(solution, t.scale)
	t.show_track()