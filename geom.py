from math import sqrt, cos, sin, pi

CARTESIAN = 1
SPHERICAL = 2

# At this point, the code only handles Cartesian coordinates.  To impllement
# sperical coordinates, changes only need to be made to the center_of_mass,
# distance, and diameter methods.

def center_of_mass(points, geometry):
    # Computes the center of mass of a group of points, returning
    # a tuple of (x, y) or (lat, lon)
    if geometry == CARTESIAN:
        sum_x = 0
        sum_y = 0
        for point in points:
            sum_x = sum_x + point[0]
            sum_y = sum_y + point[1]
        if len(points) == 0:
            return None
        return (sum_x/len(points), sum_y/len(points))
    elif geometry == SPHERICAL:
        return (0, 0)
    else:
        return None # Add error message
    
    
def distance(point_a, point_b, geometry):
    # Returns the distance between two points
    if geometry == CARTESIAN:
        # sqrt(x^2 + y^2)
        return sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)
    elif geometry == SPHERICAL:
        return 1
    else:
        return None # Add error message
    
def calc_vectors(groups, geometry):
    # Creates a list of unit vectors, evenly divided around an origin
    # where the angle between them is determined by the number of groups
    vectors = []
    if geometry == CARTESIAN:
        vectors.append((0,1))
        angle_diff = (2*pi)/float(groups)
        for group in range(1, groups):
            angle = group * angle_diff
            vectors.append((sin(angle),cos(angle)))
        return vectors
    else:
        return [(0,0)]
    
def dot_product(vector1, vector2):
    # Dot product of two vectors
    return sum(p*q for p,q in zip(vector1, vector2))
    
def diameter(point_group, geometry):
    # In the interest of keeping this relatively simple, the diameter will be
    # the maximum distance from the center of mass of the group to the
    # points in the group.  This value will be scaled for the objective function
    # anyway, so it should suit our needs well enough.
    if geometry == CARTESIAN:
        diam = 0
        for point in point_group:
            diam = max(diam, distance(point, center_of_mass(point_group, CARTESIAN), CARTESIAN))
        if len(point_group) == 0:
            return 0
        return diam
    elif geometry == SPHERICAL:
        return 1
    else:
        return None