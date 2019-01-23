import csv
import Trie
class Utils:

    @staticmethod
    # load and clean data
    def load_data():
        with open('csv_data/data.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            data = list(reader)
        trie = Trie.TrieNode()
        for elem in data:
            if ' ' in elem: elem.remove(' ')
            if '' in elem: elem.remove('')
            trie.insert(' '.join(elem).strip().lower())
        return trie

    @staticmethod
    # Search using levenshtein algorithm
    def search(word, maxCost, trie):
        size = len(word)
        # build first row
        currentRow = range(len(word) + 1)

        results = []

        # recursively search each branch of the trie
        for letter in trie.children:
            Utils.look_recursive(trie.children[letter], letter, word, currentRow,
                                 results, maxCost, size)

        return results

    @staticmethod
    def look_recursive(node, letter, word, previousRow, results, maxCost, size):

        columns = len(word) + 1
        currentRow = [previousRow[0] + 1]

        # Create a row for the letter, with a column for each letter in the search word
        for column in range(1, columns):

            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1

            if word[column - 1] != letter:
                replaceCost = previousRow[column - 1] + 1
            else:
                replaceCost = previousRow[column - 1]

            currentRow.append(min(insertCost, deleteCost, replaceCost))


        if currentRow[-1] <= maxCost and node.word != None:
            # Add result with weighted levenshtein forumla for ranking 0 being closest match and 1 no match.
            results.append((node.word, currentRow[-1]/max(len(node.word), size)))

        if min(currentRow) <= maxCost:
            for letter in node.children:
                Utils.look_recursive(node.children[letter], letter, word, currentRow,
                                     results, maxCost, size)
