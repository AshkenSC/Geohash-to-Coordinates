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
        self.h = (abs(goal.pos[0] - self.pos[0]) + abs(goal.pos[1] - self.pos[1])) * 10

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
            if i < 0 or j < 0 or i >= len(all_nodes) or j >= len(all_nodes):
                continue
            else:
                # set neighbor nodes' father as current node
                # try:
                #     all_nodes[i][j].father = node
                # except:
                #     print('error')
                # add to neighbor nodes list
                neighbor_nodes.append(all_nodes[i][j])
    return neighbor_nodes

# calculate new g of a node. If smaller, reset its father node and g value.
def calculate_new_g(node, new_father):
    if new_father.pos[0] - node.pos[0] + new_father.pos[1] - node.pos[1] > 1:
        # current node is on the diagonal of father node
        new_g = new_father.g + 14
    else:
        # current node is not on the diagonal of father node
        new_g = new_father.g + 10
    return new_g

# find start and goal in all nodes
def find_start_and_goal(all_nodes):
    for row in all_nodes:
        for node in row:
            if node.status == 'S':
                start = node
                continue
            if node.status == 'G':
                goal = node
                continue
    return start, goal

# load map from file
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


# check if a neighbor node is reachable
def is_reachable(current_node, neighbor_nodes, neighbor_node):
    if neighbor_node.status == 'X':
        return False
    elif current_node.pos[0] != neighbor_node.pos[0] and current_node.pos[1] != neighbor_node.pos[1]:
    # consider neighbor nodes on diagonal
        for node in neighbor_nodes:
            if abs(neighbor_node.pos[0] - node.pos[0]) + abs(neighbor_node.pos[1] - node.pos[1]) == 1:
                if node.status == 'X':
                    return False
        return True
    else:
        return True

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

        # TEST
        # print(current_node.pos)
        # if current_node.pos == (0, 1):
        #     print(current_node.pos)
        # TEST

        # 2(b). move this node to close list
        open_list.remove(current_node)
        close_list.append(current_node)
        # 2(c). check current node's neighbor nodes
        neighbor_nodes = get_neighbor_nodes(all_nodes, current_node)
        for neighbor_node in neighbor_nodes:
            # if the node is unreachable or it's in close list, ignore it
            if is_reachable(current_node, neighbor_nodes, neighbor_node) and neighbor_node not in close_list:
                # if the node is not in open list
                # add it into open list and set current_node of this node's father
                if neighbor_node not in open_list:
                    # add it into open list
                    open_list.append(neighbor_node)
                    # set current_node of this node's father
                    neighbor_node.father = current_node
                    # calculate f, g, h of the node
                    neighbor_node.calculate_g()
                    neighbor_node.calculate_h(goal)
                    neighbor_node.calculate_f()
                # if the node is already in open list
                else:
                    # move it from open list to close list
                    #open_list.remove(neighbor_node)
                    #close_list.append(neighbor_node)
                    # check whether it is a better path

                    new_g = calculate_new_g(neighbor_node, current_node)
                    # if it is a better path, set current_neighbor as its father node
                    if new_g < neighbor_node.g:
                        neighbor_node.father = current_node
                        neighbor_node.calculate_g()
                        neighbor_node.calculate_h(goal)
                        neighbor_node.calculate_f()

    # 3. save the path
    # move from goal to its father, and father's father... reverse it and get the path
    current_node = goal
    path_stack = list()
    while current_node != start:
        try:
            path_stack.append(current_node.pos)
            current_node = current_node.father
        except:
            print('error or NULL')
            break
    if len(path_stack) > 1:
        while len(path_stack) > 0:
            print(path_stack.pop())

if __name__ == '__main__':
    with open('INPUT/input3.txt', 'r', encoding='utf-8') as input_file:
        main(input_file)

