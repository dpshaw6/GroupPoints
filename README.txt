---------
File List
---------

The following files are required for this script:
 - grouppoints.py
 - geom.py
 - ga.py

groups.json is one solution that the code generated.  I plotted it and circled the groups (groups.pdf), as an example of one possible optimized solution that this script might generate.


----------------------
Command Line Arguments
----------------------

Example:  ./grouppoints jsonfile

The script takes exactly one command line argument.  That argument is the name of the json file containing the list of points that are to be analyzed.


------------------------------
Design Decisions & Explanation
------------------------------
The grouping of the points is a fairly straightforward optimization problem.  That said, it is certainly not trivial.  The space that needs to be searched is: (number of points)^(number of groups).  For the simple test case provided for this exercise, there are 30 points.  If we were to break them into 4 groups, that makes over a billion billion potential combinations.

The approach this code takes for dealing with this is to do a coarse global optimization based upon the location of the points with respect to the center of all of the points (geometric decomposition).  The code then proceeds to a local optimization using a genetic algorithm-monte carlo hybrid approach.

The global optimization simply calculates the center of mass of the entire group.  It then creates a series of unit vectors, starting at the origin, that are evenly spaced in angle based on the number of groups that are being created.  It then generates a vector for each point from the center of mass to the location of the point.  It is then possible to take the dot product of that vector with the previously created unit vectors to identify which two unit vectors it lies between.  The points are then assigned to their designated area.

The group that each point is located in is represented by an integer ranging from 0 to (number of groups)-1.  These values for each point are the genes for the genetic algorithm and, when they are stored together in a list, become the genome.

In order find the optimal genome, it is necessary to create a scoring, or objective, function.  The goal is the minimize that objective function.  The objective function for this script is relatively simple.  It measures (and tries to minimize), the diameter of each group and also measures (and tries to minimize) the variation in number of points per group.

The actual optimization process involves:
 - 1. Calculating the objective function for the genomes in the popoulation.  It also compares them to the best genome thus far and updates that genome if it finds a better one.
 - 2. Sorting the genomes based on their objective function.
 - 3. The best genomes become parents for the next generation.  The average genomes will be replaced by the mating of the parents.
 - 4. The poor genomes will be replaced by new, randomly generated genomes (Monte Carlo).
 - 5. All the genomes will be given the opporunity to mutate.
 - 6. This process is then repeated with the new generation of the population.

After a set number of iterations, the best genome is considered the solution and is written out to a json file as a list of lists of the same points that were in the original input file.

Due to the pseudo-random nature of this script, it currently will not generate reproducible solutions.  That said, it would merely be a matter of explicitly seeding the pseudo-random number generator to make the solutions duplicatable.
 

----------------------------------------
Genetic Algorithm/Monte Carlo Parameters
----------------------------------------

There are four GA parameters and 1 MC parameter.  All of them are located in the ga.py file.

GA:
    NUM_GA_GENOMES = 1000 - Size of the population subject to generation via mating of fit parents
    NUM_PARENTS = 20 - The best genomes in a population, they are the parents for all genomes produced via mating
    MUTATION_RATE = 0.1 - The chance of an individual gene randomly changing between generations
    NUM_GENERATIONS = 20 - The number of times to iterate through the optimization process
    
MC:
    NUM_MC_GENOMES = 1000 - Number of genomes that will be randomly generated each generation.


----------------------------------
Sperical vs. Cartesian Coordinates
----------------------------------

The code currently only supports Cartesian coordinates.  Extending it to use spherical would be relatively straightforward.  There are only three methods in geom.py where there would need to be different calculations for a different geometry.


