"""
AoC 2022 Day 18 script
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('Qt5Agg')


# Each point in the input represents a 1x1x1 cube's coordinates on a 3d grid
# we want to find the number of exposed faces of all cubes
# if cubes are adjacent to each other, then one of the cube's face is hidden
# my first thought is to calculate the distance between each point and all other points
# if the distance is 1, then the points are adjacent and 1 face is hidden

def parse_cube_coordinates(input: list[str]) -> list[tuple[int, int, int]]:
    return [(int(line.split(",")[0]), int(line.split(",")[1]), int(line.split(",")[2])) for line in input]


def get_distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def get_exposed_faces(cube_coordinates: list[tuple[int, int, int]]) -> int:
    exposed_faces = 0
    for i in range(len(cube_coordinates)):
        cube = 6
        for j in range(len(cube_coordinates)):
            if i != j and get_distance(cube_coordinates[i], cube_coordinates[j]) == 1:
                cube -= 1
        exposed_faces += cube
    return exposed_faces


# this didnt work, I think it might be missing cases where there are channels from the outside into voids
def find_voids(cubes):
    # get the min and max coordinates
    min_x = min([cube[0] for cube in cubes])
    max_x = max([cube[0] for cube in cubes])
    min_y = min([cube[1] for cube in cubes])
    max_y = max([cube[1] for cube in cubes])
    min_z = min([cube[2] for cube in cubes])
    max_z = max([cube[2] for cube in cubes])
    # loop over each point and if it is not in the list of cubes, test it
    # we test it by checking if all 6 sides are hidden by a cube
    voids = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in cubes:
                    # test if all 6 sides are hidden by checking if that side coord is contained in the list of cubes
                    # fix y,z and test in x direction
                    # find all cubes that have y,z
                    cubes_in_x_plane = [cube for cube in cubes if cube[1] == y and cube[2] == z]
                    if len(cubes_in_x_plane) == 0:
                        continue
                    elif min(cubes_in_x_plane)[0] > x or max(cubes_in_x_plane)[0] < x:
                        continue
                    # fix x,z and test in y direction
                    # find all cubes that have x,z
                    cubes_in_y_plane = [cube for cube in cubes if cube[0] == x and cube[2] == z]
                    if len(cubes_in_y_plane) == 0:
                        continue
                    elif min(cubes_in_y_plane)[1] > y or max(cubes_in_y_plane)[1] < y:
                        continue
                    # fix x,y and test in z direction
                    # find all cubes that have x,y
                    cubes_in_z_plane = [cube for cube in cubes if cube[0] == x and cube[1] == y]
                    if len(cubes_in_z_plane) == 0:
                        continue
                    elif min(cubes_in_z_plane)[2] > z or max(cubes_in_z_plane)[2] < z:
                        continue
                    voids.append((x, y, z))
    return voids


# could have put this in the function above, but I wanted to see the voids before/after
def check_voids(voids, cubes):
    # need to remove any voids that are touching the outside
    clean = False
    while not clean:
        for void in voids:
            # get the coordinates of all adjacent cubes
            adjacent_cubes = [(void[0] + 1, void[1], void[2]), (void[0] - 1, void[1], void[2]),
                              (void[0], void[1] + 1, void[2]), (void[0], void[1] - 1, void[2]),
                              (void[0], void[1], void[2] + 1), (void[0], void[1], void[2] - 1)]
            # check if any of the adjacent cubes are in the list of cubes or voids
            if not all([cube in cubes or cube in voids for cube in adjacent_cubes]):
                print(f"void {void} is not connected to anything")
                voids.remove(void)
                break
        clean = True
    return voids


if __name__ == '__main__':
    print("Running AoC 2022 Day 18 script")
    with open("../data/day18.txt", "r") as f:
        input = f.readlines()
        cubes = parse_cube_coordinates(input)
        print(cubes)
        exposed_faces = get_exposed_faces(cubes)
        print(f"exposed_faces: {exposed_faces}")
        # for part two we also need to eliminate any faces that do no touch the outside
        # we need to loop through the bounds of the graph and find any points that are hidden in all directions
        voids = find_voids(cubes)
        print(f"voids: {voids}")
        # want to check that every void is adjacent to either another void or a cube, if not then it is not a real void
        # there has to be a slick was to do this; probably would just be easier to dfs the 'steam' from the outside, but im curious
        voids = check_voids(voids, cubes)
        # find how many faces are exposed in the voids
        void_faces = get_exposed_faces(voids)
        print(f"void_faces: {void_faces}")
        # the new total should be the old total minus the void faces
        new_total = exposed_faces - void_faces
        print(f"new_total: {new_total}")
        # plt.figure()
        # ax = plt.axes(projection='3d')
        # ax.scatter([cube[0] for cube in cubes], [cube[1] for cube in cubes], [cube[2] for cube in cubes], c='r')
        # ax.scatter([void[0] for void in voids], [void[1] for void in voids], [void[2] for void in voids], c='b')
        # plt.show()
