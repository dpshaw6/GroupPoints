from random import randint
from random import random
from geom import center_of_mass
from geom import diameter
from geom import calc_vectors
from geom import dot_product
from collections import Counter
import json

# Scaling Factors
sf_diam = 1.0
sf_count = 1.0

# Initialize simple genetic algorithm parameters
NUM_GA_GENOMES = 1000
NUM_PARENTS = 20
MUTATION_RATE = 0.1
NUM_GENERATIONS = 20
   
# Initialize monte carlo parameters
NUM_MC_GENOMES = 1000
    
NUM_GENOMES = NUM_GA_GENOMES + NUM_MC_GENOMES
    

class Genome:

    def __init__(self, size, groups, points, geometry):
        # Search space is num_groups^num_points, which is enormous
        # We'll set the initial genome to put the points in similar
        # geographic locations and then mutate it slightly to get some
        # variation.
        self.genes = [] * len(points)
        coords = [] * len(points)
        # Translate the points into (x,y) tuples for use by geom.py
        for point in points:
            coords.append((point['lat'],point['lon']))
        com = center_of_mass(coords, geometry)
        vectors = calc_vectors(groups, geometry)
        
        # To do an initial breakout of the points, find a vector from the 
        # center of mass of all of the points to each of the individual points.
        # Next, dot that vector with the init vectors that define n equal spaces.
        # If the dot product is less than 0 for one vector and greater than zero 
        # for the next vector, then that point is located in that subspace
        for coord in coords:
            iVector = (coord[0]-com[0],coord[1]-com[1])
            area = groups - 1
            for iArea in (range(groups-1)):
                if dot_product(iVector,vectors[iArea]) < float(0) and dot_product(iVector,vectors[iArea+1]) > float(0):
                    area = iArea
                    break
            self.genes.append(area)
            
        # All of the points are coarsely divided at this point.  Mutate the 
        # genomes some to get some genetic variation which will allow the 
        # optimization engine to find a local minimum.
        self.mutate(0.5*random(), groups)
        self.obj_func_value = 1000
   
    def minimum_points_per_group(self, min_points, size, groups):
        # Make sure we keep a minimum number of points in each group
        gene_count = Counter(self.genes)
        for key in gene_count:
            while gene_count[key] < min_points:
                self.genes = [randint(0,groups-1) for i in range(size)]
                gene_count = Counter(self.genes)
      
    def get_genes(self):
        return self.genes
    
    def set_genes(self, genes):
        self.genes = list(genes)
        
    def display(self):
        print ''.join(str(self.genes))
        print ('%6.2f ' % self.obj_func_value)
        
    def write(self, groups, points):
        # rearrange original points into groups as per genome then
        # write to file as json
        group_json = []
        for group in range(groups):
            group_list = []
            i = 0
            for gene in self.genes:
                if gene == group:
                    group_list.append(points[i])
                i = i + 1
            group_json.append(group_list)
        with open('groups.json', 'w') as outfile:
            json.dump(group_json, outfile)
    
    def mutate(self, mut_rate, groups):
        # Mutate a genome
        for iGene in range(len(self.genes)):
            if (random() < mut_rate):
                self.genes[iGene] = randint(0,groups-1)
       
    def mate(self, parent1, parent2):
        # Mate to genomes to make a new genome
        for iGene in range(len(self.genes)):
            parent = randint(1,2)
            if parent == 1:
                self.genes[iGene] = parent1.genes[iGene]
            else:
                self.genes[iGene] = parent2.genes[iGene]
    
    # For the objective function, we want to:
    # 1. Minimize the diameter of the groups
    # 2. Minimize the difference in the number of points between groups
    def calc_obj_func(self, groups, points, geometry):
        # Create sub_groups
        sub_groups = []
        for group in range(groups):
            group_row = []
            point = 0
            for gene in self.genes:
                if gene == group:
                    group_row.append((points[point]['lat'], points[point]['lon']))
                point = point + 1
            sub_groups.append(group_row)
            
        diam = sum([diameter(group, geometry) for group in sub_groups])/groups
        
        gene_count = Counter(self.genes)
        count_diff = 0
        for key in gene_count:
            count_diff = count_diff + abs(gene_count[key] - sf_count)
        
        self.obj_func_value = diam/sf_diam + count_diff
     
    def get_obj_func(self):
        return self.obj_func_value
    
    def set_obj_func(self, obj_func_value):
        self.obj_func_value = obj_func_value
    
def set_scaling_factors(random_genome, points, groups, geometry):
    sub_groups = []
    for group in range(groups):
        group_row = []
        point = 0
        for gene in random_genome.genes:
            if gene == group:
                group_row.append((points[point]['lat'], points[point]['lon']))
            point = point + 1
        sub_groups.append(group_row)
               
    global sf_diam
    sf_diam = sum([diameter(group, geometry) for group in sub_groups])
    
    global sf_count
    sf_count = len(points)/groups