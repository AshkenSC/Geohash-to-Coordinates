import argparse as ap

import re

import platform


######## RUNNING THE CODE ####################################################

#   You can run this code from terminal by executing the following command

#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>

#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0

#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA

###############################################################################


################## YOUR CODE GOES HERE ########################################

# define node class
class Node:
    def __init__(self, pos, status):
        self.pos = pos
        self.status = status
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None
        self.children = list()
        # the following are used for console output
        self.id = -1
        self.operator = ''
        self.path = ''

    # calculate g value
    def calculate_g(self):
        if abs(self.parent.pos[0] - self.pos[0]) + abs(self.parent.pos[1] - self.pos[1]) > 1:
            # current node is on the diagonal of parent node
            self.g = self.parent.g + 1
        else:
            # current node is not on the diagonal of parent node
            self.g = self.parent.g + 2

    # calculate h value
    # use Manhattan method to estimate
    def calculate_h(self, goal):
        dx = abs(goal.pos[0] - self.pos[0])
        dy = abs(goal.pos[1] - self.pos[1])
        # self.h = (abs(goal.pos[0] - self.pos[0]) + abs(goal.pos[1] - self.pos[1])) * 2
        # 对角线走比走两条边更短。因此可看作：
        # 在min(dx, dy)边长的正方形上斜着走：代价abs(dx - dy)
        # dx和dy更长者，其剩下的部分只能直走，代价为(max(dx, dy) - abs(dx - dy)) * 2
        self.h = abs(dx - dy) + (max(dx, dy) - abs(dx - dy)) * 2

    # calculate f value:
    def calculate_f(self):
        self.f = self.g + self.h

    # calculate path from start to current node
    def calculate_path(self, start):
        action_list = 'S'
        if self == start:
            return action_list
        # get path node
        node = self
        path_nodes = list()
        while node != start:
            path_nodes.insert(0, node)
            node = node.parent
        path_nodes.insert(0, start)
        # transfer node to action list string
        for node in path_nodes:
            action_list = update_action_list(start, action_list, node)
        return action_list

    # calculate operator
    def get_operator(self, start):
        if self == start:
            return 'S'
        direction = (self.pos[0] - self.parent.pos[0], self.pos[1] - self.parent.pos[1])
        if direction == (1, 0):
            return 'D'
        elif direction == (1, 1):
            return 'RD'
        elif direction == (0, 1):
            return 'R'
        elif direction == (-1, 1):
            return 'RU'
        elif direction == (-1, 0):
            return 'U'
        elif direction == (-1, -1):
            return 'LU'
        elif direction == (0, -1):
            return 'L'
        elif direction == (1, -1):
            return 'LD'


# read map from file and get map file object
def read_from_file(file_name):
    # You can change the file reading function to suit the way
    # you want to parse the file
    file_handle = open(file_name, 'r')
    map = file_handle
    return map


# load map from map file
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
                # set neighbor nodes' parent as current node
                # try:
                #     all_nodes[i][j].parent = node
                # except:
                #     print('error')
                # add to neighbor nodes list
                neighbor_nodes.append(all_nodes[i][j])
    return neighbor_nodes


# calculate new g of a node. If smaller, reset its parent node and g value.
def calculate_new_g(node, new_parent):
    if new_parent.pos[0] - node.pos[0] + new_parent.pos[1] - node.pos[1] > 1:
        # current node is on the diagonal of parent node
        new_g = new_parent.g + 14
    else:
        # current node is not on the diagonal of parent node
        new_g = new_parent.g + 10
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


# get the map indicating current position
def get_current_step_map(all_nodes, current_node):
    current_map = ''
    for row in all_nodes:
        for node in row:
            if node == current_node and node.status == 'R':
                current_map += '*'
            else:
                current_map += node.status
        current_map += '\n'
    return current_map


# get current action list
def update_action_list(start, action_list, node):
    if node == start:
        return 'S'
    direction = (node.pos[0] - node.parent.pos[0], node.pos[1] - node.parent.pos[1])
    # if direction == (1, 0):
    #     return action_list + '-R'
    # elif direction == (1, 1):
    #     return action_list + '-RD'
    # elif direction == (0, 1):
    #     return action_list + '-D'
    # elif direction == (-1, 1):
    #     return action_list + '-LD'
    # elif direction == (-1, 0):
    #     return action_list + '-L'
    # elif direction == (-1, -1):
    #     return action_list + '-LU'
    # elif direction == (0, -1):
    #     return action_list + '-U'
    # elif direction == (1, -1):
    #     return action_list + '-RU'

    if direction == (1, 0):
        return action_list + '-D'
    elif direction == (1, 1):
        return action_list + '-RD'
    elif direction == (0, 1):
        return action_list + '-R'
    elif direction == (-1, 1):
        return action_list + '-RU'
    elif direction == (-1, 0):
        return action_list + '-U'
    elif direction == (-1, -1):
        return action_list + '-LU'
    elif direction == (0, -1):
        return action_list + '-L'
    elif direction == (1, -1):
        return action_list + '-LD'


# get accumulated cost
def update_cost(start, cost, node):
    if node == start:
        return 0
    direction = (node.pos[0] - node.parent.pos[0], node.pos[1] - node.parent.pos[1])
    if direction in {(1, 1), (-1, 1), (-1, -1), (1, -1)}:
        return cost + 1
    elif direction in {(1, 0), (0, 1), (-1, 0), (0, -1)}:
        return cost + 2


# get final output string
def get_result_string(start, goal, all_nodes):
    # if no path is found
    if goal.parent is None:
        return 'NO-PATH'

    # get nodes on the path from goal
    current_node = goal
    path_nodes = list()
    while current_node != start:
        try:
            path_nodes.append(current_node)
            current_node = current_node.parent
        except:
            print('error or NULL')
            break
    # reverse the nodes to get path from start to goal
    path_nodes.reverse()
    path_nodes.insert(0, start)

    solution = ''  # final solution string
    action_list = ''  # list of actions string
    cost = 0
    for i in range(len(path_nodes)):
        # get the map indicating current position
        solution += get_current_step_map(all_nodes, path_nodes[i]) + '\n'
        # get current action list
        action_list = update_action_list(start, action_list, path_nodes[i])
        # get accumulated cost
        cost = update_cost(start, cost, path_nodes[i])

        solution += action_list + ' ' + str(cost) + '\n\n'

    return solution


# console output
def console_output(current_node, start, open_list, close_list, expan_order):
    # build current node's path
    current_node.path = current_node.calculate_path(start)
    current_node.operator = current_node.get_operator(start)

    # node identifier, expansion order, g, h, f
    print('N' + str(current_node.id) + ':' + current_node.path, end=' ')
    if current_node == start:
        print(str(expan_order), str(current_node.g), str(current_node.h), str(current_node.f))
    else:
        print(current_node.operator, str(expan_order), str(current_node.g), str(current_node.h), str(current_node.f))

    # children
    print('Children: {', end='')
    for i in range(len(current_node.children)):
        # calculate current children's path
        current_node.children[i].path = current_node.children[i].calculate_path(start)
        print('N' + str(current_node.children[i].id) + ':' + current_node.children[i].path, end=' ')
        print(current_node.children[i].get_operator(start), end='')
        if i != len(current_node.children) - 1:
            print(', ', end='')
    print('}')

    # OPEN (f value ascending)
    open_list.sort(key=lambda node: node.f)  # sort OPEN according to f value
    print('OPEN: {', end='')
    for i in range(len(open_list)):
        print('(', end='')
        # calculate current node's path
        open_list[i].path = open_list[i].calculate_path(start)
        print('N' + str(open_list[i].id) + ':' + open_list[i].path, end=' ')
        print(open_list[i].get_operator(start), end=' ')
        print(str(open_list[i].g), str(open_list[i].h), str(open_list[i].f), end='')
        print(')', end='')
        if i != len(open_list) - 1:
            print(', ', end='')
    print('}')

    # CLOSED
    print('CLOSED: {', end='')
    order = 1
    for i in range(len(close_list)):
        print('(', end='')
        print('N' + str(close_list[i].id) + ':' + close_list[i].get_operator(start), end=' ')
        print(str(order), str(close_list[i].g), str(close_list[i].h), str(close_list[i].f), end='')
        print(')', end='')
        if i != len(close_list) - 1:
            print(', ', end='')
        order += 1
    print('}')

    print('\n')


# A-star main function
def graphsearch(map, flag):
    # load all nodes in a 2d-array
    # their indices are the same as their positions
    all_nodes, size = load_map(map)

    # locate start and goal
    start, goal = find_start_and_goal(all_nodes)

    # define open list and close list
    open_list = list()
    close_list = list()

    # define node id and expansion order
    node_id = 0
    expan_order = 1

    # 1. add start point into open list
    open_list.append(start)
    start.id = node_id
    node_id += 1

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
                if neighbor_node not in open_list:
                    # add it into open list
                    open_list.append(neighbor_node)
                    # set current_node as this node's parent
                    neighbor_node.parent = current_node
                    current_node.children.append(neighbor_node)
                    # set current node's id
                    neighbor_node.id = node_id
                    node_id += 1
                    # calculate f, g, h of the node
                    neighbor_node.calculate_g()
                    neighbor_node.calculate_h(goal)
                    neighbor_node.calculate_f()
                # if the node is already in open list
                else:
                    # try to calculate new g value
                    new_g = calculate_new_g(neighbor_node, current_node)
                    # if it is a better path (i.e. new g value is smaller), set current_neighbor as its parent node
                    if new_g < neighbor_node.g:
                        neighbor_node.parent = current_node
                        neighbor_node.calculate_g()
                        neighbor_node.calculate_h(goal)
                        neighbor_node.calculate_f()

        # console output
        if flag >= 1:
            console_output(current_node, start, open_list, close_list, expan_order)
            flag -= 1
            expan_order += 1

    # 3. save the path
    # move from goal to its parent, and parent's parent... reverse it and get the path
    solution = get_result_string(start, goal, all_nodes)

    return solution


###############################################################################

########### DO NOT CHANGE ANYTHING BELOW ######################################

###############################################################################


def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')

    file_handle.write(solution)


def main():
    # create a parser object

    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)

    # get all the arguments

    arguments = parser.parse_args()

    ##############################################################################

    # these print statements are here to check if the arguments are correct.

    #    print("The input_file_name is " + arguments.input_file_name)

    #    print("The output_file_name is " + arguments.output_file_name)

    #    print("The flag is " + str(arguments.flag))

    #    print("The procedure_name is " + arguments.procedure_name)

    ##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("\\")

        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1

    flag = arguments.flag

    # procedure_name = arguments.procedure_name

    try:

        map = read_from_file(input_file_name)  # get the map

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # print(map)

    solution_string = ""  # contains solution

    solution_string = graphsearch(map, flag)

    write_flag = 1

    # call function write to file only in case we have a solution

    if write_flag == 1:
        write_to_file(output_file_name, solution_string)


if __name__ == "__main__":
    main()

