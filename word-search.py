# This code is for Leetcode challenge: https://leetcode.com/problems/word-search-ii/
# 
#
#

# Below solution is based on Tire/Tree approach
class Solution(object):

    def findWords(self, board, words):

        class Node(object):
            children = None
            word = None

            def __init__(self):
                                
                self.children = {}

        def build_lookup(words):
            root = Node()

            for word in words:
                cur = root
                for c in word:
                    if c not in cur.children:
                        cur.children[c] = Node()
                    cur = cur.children[c]

                cur.word = word
            return root

        matched_words = set()

        def do_lookup(board, row_ix, col_ix, node, matched_words, height, width):

            if node.word:
                matched_words.add(node.word)

            c = board[row_ix][col_ix]
            board[row_ix][col_ix] = None
            if c in node.children:
                if row_ix > 0:
                    do_lookup(board, row_ix-1, col_ix, node.children[c], matched_words, height, width)

                if col_ix > 0:
                    do_lookup(board, row_ix, col_ix-1, node.children[c], matched_words, height, width)

                if row_ix < height-1:
                    do_lookup(board, row_ix+1, col_ix, node.children[c], matched_words, height, width)

                if col_ix < width - 1:
                    do_lookup(board, row_ix, col_ix+1, node.children[c], matched_words, height, width)
                    
                if node.children[c].word:
                    matched_words.add(node.children[c].word)

            board[row_ix][col_ix] = c

        height = len(board)
        width = len(board[0])

        lookup = build_lookup(words)

        for row_ix in range(height):
            for col_ix in range(width):
                do_lookup(board, row_ix, col_ix, lookup, matched_words, height, width)


        return list(matched_words)
        
# This solution uses recursion and results in time-out
class AlternateSolution(object):
    def findWords(self, board, words):
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        def get_matching_adjacents(board, board_height, board_width, row_ix, col_ix, char):
            matching_adjacents = []
            if col_ix < board_width-1 and board[row_ix][col_ix+1] == char:
                matching_adjacents.append(str((row_ix, col_ix+1)))

            if col_ix > 0 and board[row_ix][col_ix-1] == char:
                matching_adjacents.append(str(( row_ix, col_ix-1)))

            if row_ix < board_height-1 and board[row_ix+1][col_ix] == char:
                matching_adjacents.append(str(( row_ix+1, col_ix)))

            if row_ix > 0 and board[row_ix-1][col_ix] == char:
                matching_adjacents.append(str(( row_ix-1, col_ix)))

            return matching_adjacents

        class WordTree(object):
            node_index = None
            parent_indices = []
            val = None

            def __init__(self,node_index, parent_indices, val):

                self.node_index = node_index
                self.parent_indices = parent_indices
                self.val = val


        def match_word(board, node, word,width, height):

            if node.val == word:
                return word

            if len(word) > width * height:
                return None


            for c in word[len(node.val):]:


                matching_adjacents = get_matching_adjacents(board, height, width, node.node_index[0], node.node_index[1], c)
                if len(matching_adjacents) == 0:
                    return None

                for matching_adjacent in matching_adjacents:
                    if matching_adjacent not in node.parent_indices:
                        adjacent_node = WordTree(matching_adjacent,[str(node.node_index)],node.val+c)
                        adjacent_node.parent_indices.extend(node.parent_indices)

                        matched_word = match_word(board, adjacent_node, word,width, height)
                        if matched_word:

                            return matched_word

            return None


        def scan_words(board, word, height,width):

            first_ch = word[0]
            for row_ix in range(height):
                row = board[row_ix]
                for col_ix in range(width):
                    c = row[col_ix]

                    if first_ch == c:
                        root = WordTree(tuple((row_ix, col_ix)),[],first_ch)
                        matched_word = match_word(board, root, word,width, height)
                        if matched_word:
                            return matched_word



        board_height = len(board)
        board_width = len(board[0])
        matched_words = []
        for word in words:
            scanned_word = scan_words(board,word, board_height,board_width)

            if scanned_word and scanned_word not in matched_words:
                matched_words.append(scanned_word)

        return sorted(matched_words)

