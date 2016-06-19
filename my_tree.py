# tree node, includes name, parent, and children
class node:
    def __init__(self, name):
        self.__name = name
        self.__children = []
        self.__parent = 'Root'
    def get_parent(self):
        return self.__parent
    def get_name(self):
        return self.__name
    def get_children(self):
        return self.__children
    def set_parent(self, name):
        self.__parent = name
    def add_child(self, name):
        self.__children.append(name)
    def child_exists(self, name):
        if name in self.__children:
            return True
        return False

# tree, includes nodes
class tree:
    def __init__(self):
        self.nodes = dict()
        self.nodes["Root"] = node("Root")

    def add_node(self, node_name, parent_node_name = 'Root'):
        self.nodes[node_name] = node(node_name)
        self.nodes[node_name].set_parent(parent_node_name)

        if not self.nodes[parent_node_name].child_exists(node_name):
            self.nodes[parent_node_name].add_child(node_name)

    def dfs(self, current_node_name):
        print(current_node_name)
        for elem in self.nodes[current_node_name].get_children():
            self.dfs(elem)
    def bfs(self, current_node_name):
        bfs_list = []
        bfs_list.extend(self.nodes[current_node_name].get_children())
        print(bfs_list)
        self.__bfs_traverse(bfs_list)

    def __bfs_traverse(self, bfs_order_list):
        current_node_name = bfs_order_list[0]
        print(current_node_name)
        bfs_order_list.pop(0)
        if len(bfs_order_list) == 0:
            return
        bfs_order_list.extend(self.nodes[current_node_name].get_children())
        self.__bfs_traverse(bfs_order_list) 

def test():
    my_tree = tree()
    my_tree.add_node("node1")
    my_tree.add_node("node2")
    my_tree.add_node("node1_1", "node1")
    my_tree.add_node("node1_2", "node1")
    my_tree.add_node("node2_1", "node2")
    my_tree.add_node("node2_2", "node2")

    my_tree.dfs("Root")
    print("=======")
    my_tree.bfs("Root")

    print(my_tree.nodes["node1"].get_parent())
    print(my_tree.nodes["node1_1"].get_parent())
    print(my_tree.nodes["node2"].get_parent())
    print(my_tree.nodes["node2"].get_children())
    print(my_tree.nodes["node2_1"].get_parent())

#test()
