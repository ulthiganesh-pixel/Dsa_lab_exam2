import sys
import time
import re

# ==========================================
# 1. QUEUE / LINKED LIST FOR LINE NUMBERS
# ==========================================
class LineNode:
    """Node for the linked list storing line numbers."""
    def __init__(self, line_num):
        self.line_num = line_num
        self.next = None

class LineQueue:
    """Linked-list queue for tracking line numbers where a word appears."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, line_num):
        new_node = LineNode(line_num)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def to_list(self):
        """Convert linked list to a standard python list for output."""
        res = []
        curr = self.head
        while curr:
            res.append(curr.line_num)
            curr = curr.next
        return res


# ==========================================
# 2. TRIE IMPLEMENTATION
# ==========================================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.line_queue = LineQueue()

class TrieIndex:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, line_num):
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end_of_word = True
        curr.line_queue.add(line_num)

    def search(self, word):
        curr = self.root
        for char in word:
            if char not in curr.children:
                return None
            curr = curr.children[char]
        return curr.line_queue if curr.is_end_of_word else None

    def get_lexicographic_order(self):
        """Returns a list of (word, line_queue) tuples in lexicographic order."""
        result = []
        def _dfs(node, prefix):
            if node.is_end_of_word:
                result.append((prefix, node.line_queue))
            for char in sorted(node.children.keys()):
                _dfs(node.children[char], prefix + char)
        
        _dfs(self.root, "")
        return result


# ==========================================
# 3. ROBUST ITERATIVE BST IMPLEMENTATION
# ==========================================
class BSTNode:
    def __init__(self, word):
        self.word = word
        self.line_queue = LineQueue()
        self.left = None
        self.right = None

class BSTIndex:
    def __init__(self):
        self.root = None

    def insert(self, word, line_num):
        """Iterative insertion to prevent recursion depth errors on large files."""
        new_node = BSTNode(word)
        new_node.line_queue.add(line_num)

        if not self.root:
            self.root = new_node
            return

        curr = self.root
        while True:
            if word == curr.word:
                curr.line_queue.add(line_num)
                return
            elif word < curr.word:
                if not curr.left:
                    curr.left = new_node
                    return
                curr = curr.left
            else:
                if not curr.right:
                    curr.right = new_node
                    return
                curr = curr.right

    def search(self, word):
        curr = self.root
        while curr:
            if word == curr.word:
                return curr.line_queue
            elif word < curr.word:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def get_lexicographic_order(self):
        """Iterative in-order traversal using an explicit stack."""
        result = []
        stack = []
        curr = self.root

        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append((curr.word, curr.line_queue))
            curr = curr.right

        return result


# ==========================================
# 4. PYTHON DICTIONARY IMPLEMENTATION
# ==========================================
class DictIndex:
    def __init__(self):
        self.index_dict = {}

    def insert(self, word, line_num):
        if word not in self.index_dict:
            self.index_dict[word] = LineQueue()
        self.index_dict[word].add(line_num)

    def search(self, word):
        return self.index_dict.get(word, None)

    def get_lexicographic_order(self):
        sorted_keys = sorted(self.index_dict.keys())
        return [(k, self.index_dict[k]) for k in sorted_keys]


# ==========================================
# 5. PARSER & MAIN EXECUTION
# ==========================================
def parse_file_and_build(filepath, implementation_type):
    if implementation_type == 'trie':
        index = TrieIndex()
    elif implementation_type == 'bst':
        index = BSTIndex()
    elif implementation_type == 'dict':
        index = DictIndex()
    else:
        raise ValueError("Unknown implementation type")

    # Matches words separated by blanks, line breaks, full stop, comma, colon, or semicolon[cite: 2]
    word_pattern = re.compile(r'[^\s\.,;:]+')

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, start=1):
            words = word_pattern.findall(line)
            for word in words:
                index.insert(word, line_num)
                
    return index

def main():
    if len(sys.argv) < 3:
        print("Usage: python index_generator.py <input_file> <output_file> [trie|bst|dict]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    impl_type = sys.argv[3] if len(sys.argv) > 3 else 'dict'

    print(f"Building index using [{impl_type}] from {input_file}...")
    start_time = time.time()
    index = parse_file_and_build(input_file, impl_type)
    print(f"Construction time: {time.time() - start_time:.4f} seconds")

    print(f"Writing sorted index to {output_file}...")
    sorted_entries = index.get_lexicographic_order()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        for word, queue in sorted_entries:
            lines_str = ", ".join(map(str, queue.to_list()))
            out.write(f"{word} : {lines_str}\n")
            
    print("Done!")

if __name__ == "__main__":
    main()