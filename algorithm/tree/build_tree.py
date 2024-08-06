class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

def build_tree(node_data):
    # Create a dictionary to keep track of parent-child relationships
    parent_child_map = {}

    # Build the parent-child relationship map
    for parent, info in node_data.items():
        children = info['children']
        for child in children:
            parent_child_map[child] = parent

    # Find the root node by checking which node doesn't have a parent
    root_node_key = None
    for key in node_data.keys():
        if key not in parent_child_map:
            root_node_key = key
            break

    if root_node_key is None:
        raise ValueError("No root node found in the provided data.")

    def build_subtree(node_key):
        node = TreeNode(node_key)
        for child_key in node_data.get(node_key, {}).get('children', []):
            child_node = build_subtree(child_key)
            node.children.append(child_node)
        return node

    # Build the tree starting from the root node
    root_node = build_subtree(root_node_key)
    return root_node

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
    'D': {'children': []},
    'E': {'children': ['G', 'H']},
    'F': {'children': []},
    'G': {'children': []},
    'H': {'children': []}
}

# Build the tree and find the root node
root_node = build_tree(node_data)

# Print the tree structure
print_tree(root_node)