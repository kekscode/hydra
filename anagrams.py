import itertools

def parse_file(file):
    content = []
    with open(file) as f:
        for line in f.readlines():
            content.append(line.split(" "))

    # Flatten "list of lines" from book's content and deduplicate words
    flat_list = set(list(itertools.chain(*content)))
        
    return(flat_list)



def is_anagram(a, b):

    a = a.lower()
    b = b.lower()

    if a == b:
        return False

    def count_items(sequence):
        counts = {}
        for item in sequence:
            counts[item] = counts.get(item, 0) + 1
        return counts

    return count_items(a) == count_items(b)


if __name__ == "__main__":
    words = parse_file("./data/11-0.txt")
    for word in words:
        for candidate in words:
            # 1. now compare every word with every other word in the list using the anagram function
            # 2. when this works: scale over cpus and scale over threads and use the timeit module

            if is_anagram(word, candidate):
                print(word, candidate)
#            anagram = is_anagram()

