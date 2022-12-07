"""
AoC 2022 Day 7 script
"""


# simple node structure
class Node:
    def __init__(self, dir_name=None, parent=None, children=[], files=[]):
        self.parent = parent
        self.dir_name = dir_name
        self.children = []
        self.files = []

    def print_tree(self, level=0, just_dirs=False):
        print("  " * level + self.dir_name + " " + str(self.get_size()))
        if len(self.children) > 0:
            for child in self.children:
                child.print_tree(level + 1, just_dirs)
        if not just_dirs and len(self.files) > 0:
            for file in self.files:
                print("  " * (level + 1) + str(file[0]) + " " + str(file[1]))

    # calculate the size of directory by summing the size of all files and directories
    def get_size(self):
        size = 0
        if len(self.files) > 0:
            for file in self.files:
                size += int(file[0])
        if len(self.children) > 0:
            for child in self.children:
                size += child.get_size()
        return size

    # find the total size of all directories that are under 100000 size
    def get_small_dirs(self):
        size = 0
        if len(self.children) > 0:
            for child in self.children:
                if child.get_size() < 100000:
                    size += child.get_size()
                    size += child.get_small_dirs()
                else:
                    size += child.get_small_dirs()
        return size

    # find the child that is closest to target size without going under
    def find_closest_child(self, target_size):
        # this finds the closest child in the current level
        closest_child = None
        for child in self.children:
            if child.get_size() < target_size:
                continue
            if closest_child is None:
                closest_child = child
            elif child.get_size() < closest_child.get_size():
                closest_child = child
        return closest_child

    def find_global_closest_child(self, size: int):
        canidates = []
        cand = self.find_closest_child(size)
        if cand is not None:
            canidates.append(cand)
        for child in self.children:
            canidates += child.find_global_closest_child(size)
        return canidates



# start by building a node structure from the input
# each line that starts with $ is a command controlling the node were on
# The results of the command are stored in the node
# files are contents; dirs are nodes; just going to use a dict for this
def parse_directory_struct(commands: list):
    root = Node(dir_name="/")
    # current node, we know root node is /
    cur_node = root
    # iterate over the commands
    i = 1
    while i < len(commands):
        command = commands[i]
        # check if the command is a node
        if command[0] == "$":
            # get the node name
            cmd = command[1:].strip().split(" ")
            if cmd[0] == "cd":
                # change the current node
                new_dir = cmd[1]
                # handle special case
                if new_dir == "..":
                    # go up a level
                    cur_node = cur_node.parent
                else:
                    # check if the node exists
                    if new_dir not in [child.dir_name for child in cur_node.children]:
                        # create a new node
                        new_node = Node(dir_name=new_dir, parent=cur_node)
                        cur_node.children.append(new_node)
                        cur_node = new_node
                    else:
                        # get the node
                        cur_node = [child for child in cur_node.children if child.dir_name == new_dir][0]
            elif cmd[0] == "ls":
                # go through the contents and create/add contents
                i += 1
                while i < len(commands):
                    command = commands[i]
                    if command[0] == "$":
                        i -= 1
                        break
                    else:
                        # determine if file or dir
                        eles = command.strip().split(" ")
                        if eles[0] == "dir":
                            # add new child dir node
                            if eles[1] not in [child.dir_name for child in cur_node.children]:
                                new_node = Node(dir_name=eles[1], parent=cur_node)
                                cur_node.children.append(new_node)
                        else:
                            # add new file; format (size, name)
                            if eles[1] not in [file[1] for file in cur_node.files]:
                                cur_node.files.append((eles[0], eles[1]))
                        i += 1
        i += 1

    return root


if __name__ == '__main__':
    print("Running AoC 2022 day 7")
    with open("../data/day7.txt", "r") as f:
        root_dir = parse_directory_struct(f.readlines())
        root_dir.print_tree(just_dirs=True)
        print(f"Size of small dirs: {root_dir.get_small_dirs()}")
        # now need to find the smallest directory that is over large enough to free up enough space
        space_needed = 30000000 - (70000000 - root_dir.get_size())
        print(f"Space needed: {space_needed}")
        # now need to find the smallest directory that is over large enough to free up enough space
        # find the closest child at each level
        canidates = root_dir.find_global_closest_child(space_needed)
        print(f"The smallest directory that is over {space_needed} is {min([cand.get_size() for cand in canidates])}")

