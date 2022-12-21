"""
AoC 2022 Day 20 script
"""


PART_1 = False
dkey = 811589153

# I think I want to make a circular doubly linked list
class Node:
    def __init__(self, data, id):
        self.data = data
        self.id = id
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"Node({self.data})"

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        # I think theres a better way to do this, but I'm not sure what it is
        self.elements = []

    def __repr__(self):
        return f"CircularDoublyLinkedList({self.head})"

    def __len__(self):
        return self.size

    def close(self):
        self.head.prev = self.tail
        self.tail.next = self.head

    def append(self, data):
        new_node = data
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.close()
        self.size += 1
        self.elements.append(new_node)

    # move an existing data element to the new index
    def move(self, data, index):
        # unhook the element
        data.prev.next = data.next
        data.next.prev = data.prev
        # get references to those elements
        p = data.prev
        n = data.next
        # calculate how far to move
        move = data.data % (self.size - 1)
        # move to new index
        for _ in range(move):
            p = p.next
            n = n.next
        # hook it back in
        p.next = data
        data.prev = p
        n.prev = data
        data.next = n



if __name__ == "__main__":
    print("Running AoC 2022 Day 20 script")
    with open("../data/day20.txt", "r") as f:
        data = f.readlines()
        # parse each line as an int, turn it into a node, and add it to the list
        encrypted = CircularDoublyLinkedList()
        for i, line in enumerate(data):
            line = line.strip()
            # print(line)
            # parse the line
            node = Node(int(line) if PART_1 else int(line) * dkey, i)
            # add the node to the list
            encrypted.append(node)
            # move the node to the correct position

        # now loop over every element and move it to its new index defined by its value and its current index
        for _ in range(1 if PART_1 else 10):
            for node in encrypted.elements:
                encrypted.move(node, node.data)
        # find the sum of the chosen
        elements_to_find = [1000, 2000, 3000]
        # find the index of the node with value 0
        zero_index = 0
        current = encrypted.head
        while current:
            if current.data == 0:
                break
            current = current.next
            zero_index += 1
        coor = 0
        # TODO the head and tail are broken here, you should try fixing it
        for ele in elements_to_find:
            current = encrypted.head
            target = (zero_index + ele) % len(encrypted)
            for i in range(target):
                current = current.next
            coor += current.data
        print(f"Value of coordinate: {coor}")
