from ga import Genome
from ga import set_scaling_factors
from ga import NUM_GA_GENOMES, NUM_PARENTS, MUTATION_RATE
from ga import NUM_GENERATIONS, NUM_GENOMES
from geom import CARTESIAN
from operator import attrgetter
from random import randint
import json
import sys

def main(infile):
    # Get the number of groups (n) to divide the points into
    n = input("Enter the number of groups into which to divide your delivery points: ")
    if n < 2:
        print "Error.  Invalid number of groups.  Must be greater than 1.  Exiting..."
        exit()
        
    # Load points.json
    try:
        with open(infile) as points_file:    
            points = json.load(points_file)
    except IOError:
        print "Error reading input file.  Exiting..."
        exit()
            
    # Count points
    NUM_GENES = len(points)
    if n > NUM_GENES:
        print "Error.  Invalid number of groups.  Must be less then the number of points.  Exiting..."
        exit()
    
    # Group points (minimum)
    MIN_PTS_PER_GRP = 2

    # Randomly create initial population
    population = [] * NUM_GENOMES
    for iGenome in range(NUM_GENOMES):
        genome = Genome(NUM_GENES, n, points, CARTESIAN)
        genome.minimum_points_per_group(MIN_PTS_PER_GRP, NUM_GENES, n)
        population.append(genome)

    # Initialize best objective function to the default value
    set_scaling_factors(population[0], points, n, CARTESIAN)
    best_obj_func = population[0].get_obj_func()
    best_genome = Genome(NUM_GENES, n, points, CARTESIAN)
    for generation in range(NUM_GENERATIONS):
        print 'Generation: ' + str(generation)
        # For each generation:
        # 1. Calculate the objective functions of the population
        # 2. Sort the population based on those objective function values
        # 3. Mate the parents to create a new generation of genomes
        # 4. Allow genomes to mutate
        # 5. Replace poorest scoring genomes with random genomes (Monte Carlo)
        # 6. Repeat with new population until NUM_GENERATIONS is met
        for genome in population:
            genome.calc_obj_func(n, points, CARTESIAN)
            if genome.get_obj_func() < best_obj_func:
                best_genome.set_genes(genome.get_genes())
                best_obj_func = genome.get_obj_func()
                best_genome.set_obj_func(best_obj_func)
                print "New best objective function value: " + str(best_obj_func)
        
        # Move the best genomes to the front of the list
        sorted_population = sorted(population, key=attrgetter('obj_func_value'))
       
        # Mate best genomes to create new generation
        for iGenome in range(NUM_PARENTS, NUM_GA_GENOMES):
            parent1 = sorted_population[randint(0,NUM_PARENTS)]
            parent2 = sorted_population[randint(0,NUM_PARENTS)]
            while parent2 == parent1:
                parent2 = sorted_population[randint(0,NUM_PARENTS)]
            sorted_population[iGenome].mate(parent1,parent2)
            sorted_population[iGenome].minimum_points_per_group(MIN_PTS_PER_GRP, NUM_GENES, n)
            
        # Allow for mutation
        for genome in sorted_population:
            genome.mutate(MUTATION_RATE, n)
            genome.minimum_points_per_group(MIN_PTS_PER_GRP, NUM_GENES, n)
            
        # Additional MC genomes:
        for iGenome in range(NUM_GA_GENOMES, NUM_GENOMES):
            sorted_population[iGenome] = Genome(NUM_GENES, n, points, CARTESIAN)
            sorted_population[iGenome].minimum_points_per_group(MIN_PTS_PER_GRP, NUM_GENES, n)
        
        population = sorted_population
        
    best_genome.write(n, points)

if __name__ == "__main__":
   main(str(sys.argv[1]))