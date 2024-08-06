class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

def build_tree(node_data, current_node_key):
    current_node_info = node_data.get(current_node_key)
    if not current_node_info:
        return None

    current_node = TreeNode(current_node_key)
    for child_key in current_node_info['children']:
        child_node = build_tree(node_data, child_key)
        if child_node:
            current_node.children.append(child_node)

    return current_node

def print_tree(root, depth=0):
    if root:
        print('  ' * depth + root.data)
        for child in root.children:
            print_tree(child, depth + 1)

# Given node data
node_data = {
    'A': {'children': ['B', 'C']},
    'B': {'children': ['D', 'E']},
    'C': {'children': ['F', 'E']},
    'E': {'children': ['G', 'H']},
}

# Identify the root node
root_node = None
for node in node_data:
    is_root = True
    for children in node_data.values():
        if node in children:
            is_root = False
            break
    if is_root:
        root_node = node
        break

print(root_node)

if root_node is not None:
    # Build the tree structure
    root = build_tree(node_data, root_node)
    # Print the tree structure
    print_tree(root)
else:
    print("No root node found in the provided data.")