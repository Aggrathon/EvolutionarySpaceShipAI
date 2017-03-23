import track
import numpy as np
import random
import math
from timeit import default_timer as timer


class Chromosome(object):

	def __init__(self, size: int=10, gene=None):
		self.size = size
		if gene is not None:
			pass

def generate_pop(size: int = 10):
	arr = [i for i in range(size)]
	np.random.shuffle(arr)
	return arr

def mutate_pop(population, mutate_chance: float = 0.02, reverse_chance=0.5):
	pop = list(population)
	length = len(population)
	for i in range(length):
		if random.random() < mutate_chance:
			o = random.randint(0,length-2)
			if o == i:
				o = length-1
			if random.random() < reverse_chance:
				if len(pop) != length:
					print("error", i, o, ' ',len(pop), length)
				if o < i:
					pop = pop[:o+1]+pop[i-1:o:-1]+pop[i:]
				else:
					pop = pop[:i+1]+pop[o-1:i:-1]+pop[o:]
				if len(pop) != length:
					print("error", i, o, ' ',len(pop), length)
			else:
				tmp = pop[o]
				pop[o] = pop[i]
				pop[i] = tmp
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

def mutate_pops(pops, percentage : float = 0.02):
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

def get_fitness(pop, points, scale):
	return track.track_length(get_track(pop, points), scale)

def select_pops(pops, points, amount: int = 10, scale : float = 1.0, roulette: bool=False):
	if roulette:
		norm_len = [get_fitness(p, points, scale) for p in pops]
		norm_max = np.max(norm_len)+1
		inv_len = [1-l/norm_max for l in norm_len]
		inv_sum = np.sum(inv_len)
		fitness = np.multiply(inv_len, 1/inv_sum)
		selection = np.random.choice(np.arange(len(pops)), size=amount, p=fitness)
		return [pops[i] for i in sorted(selection, reverse=True, key=lambda s: fitness[s])]
	else:
		pops.sort(key=lambda p: get_fitness(p, points, scale))
		return pops[:amount]

def evolutionary_generate(points, scale, generation_size = 40, max_generations=200,
		min_improvment = 0.005, stalled_generations = 15, elitism=True):
	track_length = len(points)
	population = generate_pops(generation_size, track_length)
	best = track.track_length(get_track(population[0], points), scale)
	counter = 0
	for i in range(max_generations):
		pool = generate_pops(generation_size//4, track_length)
		parents = population + pool
		pool += crossover_pops(parents, crossover_simple)
		pool += crossover_pops(parents, crossover_dmx)
		pool += crossover_pops(parents, crossover_erx)
		pool += mutate_pops(pool, (1-i/max_generations)*0.04+0.01)
		if elitism:
			sel_pop = select_pops(pool, points, generation_size-(generation_size//8), scale)
			elit_pop = population[:generation_size//8]
			if get_fitness(sel_pop[0], points, scale) > get_fitness(elit_pop[0], points, scale):
				population = elit_pop+sel_pop
			else:
				population = sel_pop+elit_pop
		else:
			population = select_pops(pool, points, generation_size, scale)
		nb = get_fitness(population[0], points, scale)
		if best - min_improvment > nb:
			best = nb
			counter = 0
		if i%5 == 0:
			print("Generation %d (%.2f)"%(i, nb))
		counter += 1
		if counter > stalled_generations:
			print("Final Generation %d (%.2f)"%(i, nb))
			break
	return get_track(population[0], points)

def __compare_method__(track_length=30):
	time1 = timer()
	t = track.Track(1, track_length, None)
	time2 = timer()
	solution = evolutionary_generate(t.points, t.scale)
	time3 = timer()
	timeOrig = time2-time1
	timerEvo = time3-time2
	return (track.track_length(t.points, t.scale), timeOrig, 
			track.track_length(solution, t.scale), timerEvo)

def compare_methods(track_size=30, track_count=20, threads=4):
	from multiprocessing import Pool
	results = Pool(threads).map(__compare_method__, [track_size]*track_count)
	orig_len, orig_time, evo_len, evo_time = (0, 0, 0, 0)
	for olen, otime, elen, etime in results:
		orig_time += otime
		orig_len += olen
		evo_len += elen
		evo_time += etime
	print()
	print("Original Length: %.2f (%.2f s)"%(orig_len/track_count, orig_time/track_count))
	print("Evolutionary Length: %.2f (%.2f s)"%(evo_len/track_count, evo_time/track_count))

if __name__ == "__main__":
	compare_methods(30, 20, 4)
