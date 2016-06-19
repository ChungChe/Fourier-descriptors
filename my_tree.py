# tree node, includes name, parent, and children
class node:
    def __init__(self, name):
        self.__name = name
        self.__children = []
        self.__parent = 'Root'
    def get_parent_name(self):
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
    
    def get_node(self, node_name):
        return self.nodes[node_name]

    def get_parent(self, node_name):
        parent_name = "Root"
        if node_name != "Root":
            parent_name = self.nodes[node_name].get_parent_name()
        return self.nodes[parent_name]
    
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
    t = tree()
    t.add_node("node1")
    t.add_node("node2")
    t.add_node("node1_1", "node1")
    t.add_node("node1_2", "node1")
    t.add_node("node2_1", "node2")
    t.add_node("node2_2", "node2")

    t.dfs("Root")
    print("=======")
    t.bfs("Root")

    print(t.nodes["node1"].get_parent_name())
    print(t.nodes["node1_1"].get_parent_name())
    print(t.nodes["node2"].get_parent_name())
    print(t.nodes["node2"].get_children())
    print(t.nodes["node2_1"].get_parent_name())
    
    r = t.get_parent("Root")
    print("Root's parent: " + r.get_name())
    r1 = t.get_parent("node2")
    print("node2's parent: " + r1.get_name())
    r2 = t.get_parent("node2_1")
    print("node2_1's parent: " + r2.get_name())
    n = t.get_node("node1")
    print(n.get_name())

#test()
