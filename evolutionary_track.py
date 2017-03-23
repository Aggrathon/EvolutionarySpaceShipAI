import track
import numpy as np
import random
import math
from timeit import default_timer as timer


def random_curve_limit(min_val, max_val):
    delta = max_val - min_val
    r1 = random.random()*delta+min_val
    r2 = np.random.triangular(min_val, min_val+delta/2, max_val)
    return (r1+r2)/2


class Chromosome(object):

	def __init__(self, size: int=10, genes=None, other=None):
		if other is None:
			self.size = size
			self.__fitness__ = -1
			if genes is None:
				self.genes = list(range(size))
				np.random.shuffle(self.genes)
			else:
				self.genes = genes
		else:
			self.size = other.size
			self.genes = list(other.genes)
			self.__fitness__ = other.__fitness__

	def copy(self):
		return Chromosome(other=self)

	def get_track(self, points):
		return [points[i] for i in self.genes]

	def get_fitness(self, points, scale):
		if self.__fitness__ != -1:
			return self.__fitness__
		return track.track_length(self.get_track(points), scale)

	def mutate(self, mutate_chance: float = 0.02, reverse_chance=0.5):
		mutated = self.copy()
		for i in range(self.size):
			if random.random() < mutate_chance:
				o = random.randint(0, self.size-2)
				if o == i:
					o = self.size-1
				if random.random() < reverse_chance:
					if o < i:
						mutated.genes = mutated.genes[:o+1]+mutated.genes[i-1:o:-1]+mutated.genes[i:]
					else:
						mutated.genes = mutated.genes[:i+1]+mutated.genes[o-1:i:-1]+mutated.genes[o:]
				else:
					tmp = mutated.genes[o]
					mutated.genes[o] = mutated.genes[i]
					mutated.genes[i] = tmp
		return mutated

	def crossover_simple(self, other):
		split = int(random_curve_limit(0.2, 0.8) * self.size)
		def combine(pop1, pop2):
			npop = pop1[:split]
			for i in range(split, len(pop2)):
				x = pop2[i]
				if not x in npop:
					npop.append(x)
			for i in range(split):
				x = pop2[i]
				if not x in npop:
					npop.append(x)
				if len(npop) == len(pop1):
					break
			return Chromosome(self.size, npop)
		return combine(self.genes, other.genes), combine(other.genes, self.genes)

	def crossover_dmx(self, other):
		def gen(split, pop1, pop2):
			npop = pop1[:split]
			for i in pop2[split:]:
				if i not in npop:
					npop.append(i)
			for i in pop2[:split]:
				if i not in npop:
					npop.append(i)
			return Chromosome(self.size, npop)
		split = int(random_curve_limit(0.2, 0.8) * self.size)
		return gen(split, self.genes, other.genes), gen(split, other.genes, self.genes)

	def crossover_erx(self, other):
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
			return Chromosome(self.size, npop)
		return gen(self.genes, other.genes), gen(other.genes, self.genes)


def generate_pops(num: int = 10, size : int = 20):
	return [Chromosome(size) for _ in range(10)]

def mutate_pops(pops, percentage : float = 0.02):
	return [pop.mutate(percentage) for pop in pops]

def crossover_pops(pops):
	result = []
	np.random.shuffle(pops)
	for i in range(0, len(pops)-1, 2):
		p1, p2 = pops[i].crossover_simple(pops[i+1])
		result.append(p1)
		result.append(p2)
	np.random.shuffle(pops)
	for i in range(0, len(pops)-1, 2):
		p1, p2 = pops[i].crossover_erx(pops[i+1])
		result.append(p1)
		result.append(p2)
	np.random.shuffle(pops)
	for i in range(0, len(pops)-1, 2):
		p1, p2 = pops[i].crossover_dmx(pops[i+1])
		result.append(p1)
		result.append(p2)
	return result

def select_pops(pops, points, amount: int = 10, scale : float = 1.0, roulette: bool=False):
	if roulette:
		norm_len = [p.get_fitness(points, scale) for p in pops]
		norm_max = np.max(norm_len)+1
		inv_len = [1-l/norm_max for l in norm_len]
		inv_sum = np.sum(inv_len)
		fitness = np.multiply(inv_len, 1/inv_sum)
		selection = np.random.choice(np.arange(len(pops)), size=amount, p=fitness)
		selection.sort(reverse=True, key=lambda s: fitness[s])
		return [pops[i] for i in selection]
	else:
		pops.sort(key=lambda p: p.get_fitness(points, scale))
		return pops[:amount]

def evolutionary_generate(points, scale, generation_size = 40, max_generations=250,
		min_improvment = 0.005, stalled_generations = 20, elitism=True):
	track_length = len(points)
	population = generate_pops(generation_size, track_length)
	best = population[0].get_fitness(points, scale)
	counter = 0
	for i in range(max_generations):
		pool = generate_pops(generation_size//4, track_length)
		pool += crossover_pops(population + pool)
		pool += mutate_pops(pool, (1-i/max_generations)*0.05+0.01)
		if elitism:
			sel_pop = select_pops(pool, points, generation_size-(generation_size//8), scale)
			elit_pop = population[:generation_size//8]
			if sel_pop[0].get_fitness(points, scale) > elit_pop[0].get_fitness(points, scale):
				population = elit_pop+sel_pop
			else:
				population = sel_pop+elit_pop
		else:
			population = select_pops(pool, points, generation_size, scale)
		nb = population[0].get_fitness(points, scale)
		if best - min_improvment > nb:
			best = nb
			counter = 0
		#if i%10 == 0:
		#	print("Generation %d (%.2f)"%(i, nb))
		counter += 1
		if counter > stalled_generations:
			print("Final Generation %d (%.2f)"%(i, nb))
			break
	return population[0].get_track(points)

def __compare_method__(track_length=30):
	time1 = timer()
	t = track.Track(1, track_length)
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
