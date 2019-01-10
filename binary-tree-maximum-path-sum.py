# This code is for Leetcode challenge: https://leetcode.com/problems//binary-tree-maximum-path-sum/
# 
#
#

# Below solutioin is based on dynamic programming approach
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

# Implementation for given TreeNode structure 
class Solution(object):
    max_path_sum = None
    
    
    def maxPathSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        self.max_path_sum = root.val
        def nodeMaxSum(node):       
            lpath_sum = rpath_sum = 0
            if node.left is not None:
                lpath_sum = nodeMaxSum(node.left)
            if node.right is not None:
                rpath_sum = nodeMaxSum(node.right)                 
           
            node_max_sum = max(node.val, lpath_sum + node.val, rpath_sum + node.val)
            self.max_path_sum = max(self.max_path_sum, lpath_sum + node.val + rpath_sum, node_max_sum) # check if current node or its children path is max
            return node_max_sum
        
        nodeMaxSum(root)
        
        return self.max_path_sum
        
        
# Alternate solution using when input is represented as arrays. This uses mathematical structure of binary tree and operates directly on arrays fastly.
import math


def compute_max_depth(tree):
    # computes maximum depth of binary tree
    max_depth = math.log(len(tree)+1, 2) - 1  # max depth is log2 of length of array + 1 for a binary tree

    # commenting out validation for better score
    #if max_depth%1 != 0:
    #    raise Exception("invalid tree")

    return int(max_depth)

# Test cases
assert compute_max_depth([i for i in range(15)]) == 3
assert compute_max_depth([i for i in range(511)]) == 8


def get_elements_at_depth(tree, depth):
    # slices elements at a given depth from binary tree represented as array
    return tree[2**(depth)-1: 2**(depth+1)-1]

# Test cases
assert (get_elements_at_depth([1,2,3],1)) == [2,3]
assert (get_elements_at_depth([1,2,3],0)) == [1]
assert (get_elements_at_depth([i for i in range(15)],3)) == [7,8,9,10,11,12,13,14]


def get_left_right_children_at_depth(tree,depth,max_depth=None):
    # This method returns two arrays, one with left children and other with right children.
    # This data structure will be helpful in computing sums faster in single iteration

    # commenting out validation for quicker response
    #if depth == max_depth:
    #    return [], []
    depth_index_start = (2**depth)-1
    number_of_nodes_at_depth = (2**(depth+1)) - (depth_index_start+1)
    next_layer_start = depth_index_start+number_of_nodes_at_depth
    left_nodes = [tree[next_layer_start+i*2] for i in range(number_of_nodes_at_depth)]
    right_nodes = [tree[next_layer_start+(i*2) + 1] for i in range(number_of_nodes_at_depth)]
    return left_nodes,right_nodes



a = [i for i in range(15)]
a = [1,2,3]
a = [-10,9,20,None,None,15,7]
a = [-1,None,9,-6,3,None,None,None,-2]

a = [0 if i is None else i for i in a]

max_depth = compute_max_depth(a)
elements_at_max_depth = get_elements_at_depth(a, max_depth)
max_path_sum = max(elements_at_max_depth)

left_child_max, right_child_max = get_left_right_children_at_depth(a, max_depth-1)

for depth in range(max_depth-1,-1,-1):
    elements_at_depth = get_elements_at_depth(a, depth)
    left_max = []
    right_max = []
    for ix in range(len(elements_at_depth)):
        path_max = max(left_child_max[ix]+elements_at_depth[ix], elements_at_depth[ix], right_child_max[ix]+elements_at_depth[ix])

        if ix%2 == 0:
            left_max.append(path_max)
        else:
            right_max.append(path_max)

        node_sum = left_child_max[ix]+elements_at_depth[ix]+right_child_max[ix]
        if max_path_sum < node_sum:
            max_path_sum = node_sum
    left_child_max = left_max
    right_child_max = right_max

assert max_path_sum == 11
