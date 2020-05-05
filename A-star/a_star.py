# FIT5047 Assignment 1
# 30989094 Shicheng Ai
# An implementation of A* algorithm

# define node class
class Node:
    def __init__(self, pos, status):
        self.pos = pos
        self.status = status
        self.f = 0
        self.g = 0
        self.h = 0
        self.father = None
        self.children = dict()
        self.OPEN = dict()
        self.CLOSED = dict()

    # check if a node is reachable
    def is_reachable(self):
        if self.status == 'X':
            return False
        else:
            return True

    # calculate g value
    def calculate_g(self):
        if self.father.pos[0] - self.pos[0] + self.father.pos[1] - self.pos[1] > 1:
            # current node is on the diagonal of father node
            self.g = self.father.g + 14
        else:
            # current node is not on the diagonal of father node
            self.g = self.father.g + 10

    # calculate h value
    # use Manhattan method to estimate
    def calculate_h(self, goal):
        self.h = (goal.pos[0] - self.pos[0] + goal.pos[1] - self.pos[1]) * 10

    # calculate f value:
    def calculate_f(self):
        self.f = self.g + self.h

# find the node with minimum F and process it
def find_min_F_node(open_list):
    min_F_node = open_list[0]
    for node in open_list:
        if node.f < min_F_node.f:
            min_F_node = node
        if node.f == min_F_node.f and open_list.index(node) > open_list.index(min_F_node):
        # if f values of 2 nodes are equal, use a newer one (whose index is larger)
            min_F_node = node
    return min_F_node

# get a list of 8 neighbor nodes of current node
def get_neighbor_nodes(all_nodes, node):
    neighbor_nodes = list()
    for i in range(node.pos[0] - 1, node.pos[0] + 2):
        for j in range(node.pos[1] - 1, node.pos[1] + 2):
            if i == node.pos[0] and j == node.pos[1]:
                continue
            if i < 0 or j < 0:
                continue
            else:
                # set neighbor nodes' father as current node
                all_nodes[i][j].father = node
                # add to neighbor nodes list
                neighbor_nodes.append(all_nodes[i][j])
    return neighbor_nodes

# calculate new g of a node. If smaller, reset its father node and g value.
def calculate_new_g(node, new_father):
    if new_father.pos[0] - node.pos[0] + new_father.pos[1] - node.pos[1] > 1:
        # current node is on the diagonal of father node
        new_g = new_father.pos + 14
    else:
        # current node is not on the diagonal of father node
        new_g = new_father.pos + 10
    return new_g

# find start and goal in all nodes
def find_start_and_goal(all_nodes):
    for row in all_nodes:
        for node in row:
            if node.status == 'S':
                start = node
                continue
            if node.status == 'G':
                end = node
                continue
    return start, end

def load_map(input_file):
    all_nodes = list()
    size = int(input_file.readline())
    i = 0
    for line in input_file:
        line = line.strip('\n')
        new_row = list()
        j = 0
        for character in line:
            new_node = Node((i, j), character)
            new_row.append(new_node)
            j += 1
        all_nodes.append(new_row)
        i += 1
    return all_nodes, size

# main function
def main(input_file):
    # load all nodes in a 2d-array
    # their indices are the same as their positions
    all_nodes, size = load_map(input_file)

    # locate start and goal
    start, goal = find_start_and_goal(all_nodes)

    # define open list and close list
    open_list = list()
    close_list = list()

    # 1. add start point into open list
    open_list.append(start)

    # 2. loop until:
    # goal point is added into open list, or
    # goal search fails, and open list is empty
    while goal not in open_list and len(open_list) != 0:
        # 2(a). traverse open list, find the node with minimum F to process it
        current_node = find_min_F_node(open_list)
        # 2(b). move this node to close list
        close_list.append(current_node)
        # 2(c). check current node's neighbor nodes
        neighbor_nodes = get_neighbor_nodes(all_nodes, current_node)
        for neighbor_node in neighbor_nodes:
            # if the node is unreachable or it's in close list, ignore it
            if neighbor_node.is_reachable() and neighbor_node not in close_list:
                # if the node is not in open list
                # and set current_node of this node's father
                if neighbor_node not in open_list:
                    # calculate f, g, h of the node
                    neighbor_node.calculate_g()
                    neighbor_node.calculate_h(goal)
                    neighbor_node.calculate_f()
                    # add it into open list
                    open_list.append(neighbor_node)
                    neighbor_node.father = current_node
                # if the node is in open list
                else:
                    # move it from open list to close list
                    open_list.remove(neighbor_node)
                    close_list.append(neighbor_node)
                    # check neighbor node's neighbors
                    for neighbors_neighbor in get_neighbor_nodes(neighbor_node):
                        if neighbors_neighbor.is_reachable():
                            # check whether it is a better path (use g value to judge)
                            new_g = calculate_new_g(neighbors_neighbor, neighbor_node)
                            # if it is a better path, set current_neighbor as its father node
                            if new_g < neighbors_neighbor.g:
                                neighbors_neighbor.father = neighbor_node
                                neighbors_neighbor.calculate_g()
                                neighbors_neighbor.calculate_h()
                                neighbors_neighbor.calculate_f()

    # 3. save the path
    # move from goal to its father, and father's father... reverse it and get the path
    current_node = goal
    while current_node != start:
        print(current_node.pos)
        current_node = current_node.father
    print(current_node.pos)

if __name__ == '__main__':
    with open('INPUT/input2.txt', 'r', encoding='utf-8') as input_file:
        main(input_file)

