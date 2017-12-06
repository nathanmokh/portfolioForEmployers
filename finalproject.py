import math

def clean_text(txt):
    """returns a cleaned list of inputted text"""
    result = ''
    for words in txt:
        s = words.lower()
        s = s.replace('.','')
        s = s.replace(',','')
        s = s.replace('?','')
        result += s
    return result

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)

def stem(s):
    """Returns the stem of a string"""
    if len(s) > 0 and len(s) < 4:
        return s
    
    if s[-1] == 's':
        s = s[:-1]
    if s[-3:] == 'ing' or s[-3:] == 'ize' or s[-3:] == 'ise':
        if len(s) <= 4:
            s = s
        elif s[-4] == s[-5]:
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-2:] == 'er':
        s = s[:-2]
    elif s[-1] == 'e':
        s = s[:-1]
    elif s[-1] == 'y':
        s = s[:-1] + 'i'
    if s[-4:] == 'ship' and s != 'ship':
        s = s[:-4]
    
    #Three letter prefixes (three cases)
    if s[:3] == 'pre' or s[:3] == 'sub' or s[:3] == 'dis':
        s = s[3:]
    if s[:2] == 'un':
        s = s[2:]
        
    return s

def compare_dictionaries(d1, d2):
    """returns a log similarity score between two dictionaries"""
    score = 0
    total = sum(d1.values())
    for x in d2:
        if x in d1:
            score += math.log(d1[x] / total) * d2[x]
        else:
            score += math.log(.5 / total) * d2[x]
    return score
            
    

class TextModel:

    def __init__(self, model_name):
        """Constructor for TextModel"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.curse_words = {}
        

    def __repr__(self):
        """Return string representation"""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of George Carlin swear words used: ' + str(len(self.curse_words)) + ' out of 7'
        return s

    def add_string(self, s):
        """Adds a string to the attributes"""
        #find sentence length
        count = 0
        for w in s.split():
            count += 1
            if w[-1] == '.' or w[-1] == '?' or w[-1] == '!':
                if count not in self.sentence_lengths:
                    self.sentence_lengths[count] = 1
                    count = 0
                else:
                    self.sentence_lengths[count] += 1
                    count = 0
        #Carlin Count
        swearCount = 0
        #https://en.wikipedia.org/wiki/Seven_dirty_words
        for w in s.split():   
            if w == 'shit' or w == 'piss' or w == 'fuck' or w == 'cunt' or w == 'cocksucker' \
               or w == 'motherfucker' or w == 'tits':
                swearCount += 1
                if w not in self.curse_words:
                    self.curse_words[w] = 1
                else:
                    self.curse_words[w] += 1
        #word count            
        word_list = clean_text(s)
        word_list = word_list.split()
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        #word length count
        for w in self.words:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
        #Stem count
        for w in word_list:
            w = stem(w)
            if w not in self.stems:
                self.stems[w] = 1
            else:
                self.stems[w] += 1
        

    def add_file(self, filename):
        """Adds text from a file to the TextModel"""
        f = open(filename, 'r', encoding = 'utf8', errors = 'ignore')
        p = f.read()
        self.add_string(p)
        f.close()

    def save_model(self):
        """Saves the object by writing the feature dictionaries to files"""
        wordsDict = self.words
        lenDict = self.word_lengths
        stemsDict = self.stems
        sentenceLenDict = self.sentence_lengths
        carlinDict = self.curse_words

        filename = self.name + '_' + 'words'
        f = open(filename, 'w')
        f.write(str(wordsDict))
        f.close()

        filename = self.name + '_' + 'word_lengths'
        g = open(filename, 'w')
        g.write(str(lenDict))
        g.close()

        filename = self.name + '_' + 'stems'
        h = open(filename, 'w')
        h.write(str(stemsDict))
        h.close()

        filename = self.name + '_' + 'sentence_lengths'
        i = open(filename, 'w')
        i.write(str(sentenceLenDict))
        i.close()

        filename = self.name + '_' + 'curse_words'
        j = open(filename, 'w')
        j.write(str(carlinDict))
        j.close()

        
        
    def read_model(self):
        filename = self.name + '_' + 'words'
        f = open(filename, 'r')
        d_str = f.read()
        d = dict(eval(d_str))
        f.close()
        self.words = d

        filename = self.name + '_' + 'word_lengths'
        g = open(filename, 'r')
        d_str = g.read()
        d = dict(eval(d_str))
        g.close()
        self.word_lengths = d

        filename = self.name + '_' + 'stems'
        h = open(filename, 'r')
        d_str = h.read()
        d = dict(eval(d_str))
        h.close()
        self.stems = d

        filename = self.name + '_' + 'sentence_lengths'
        i = open(filename, 'r')
        d_str = i.read()
        d = dict(eval(d_str))
        i.close()
        self.sentence_lengths = d

        filename = self.name + '_' + 'curse_words'
        j = open(filename, 'r')
        d_str = j.read()
        d = dict(eval(d_str))
        j.close()
        self.curse_words = d

    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores"""
        scoresList = []
        a = compare_dictionaries(other.words, self.words)
        scoresList += [a]
        a = compare_dictionaries(other.word_lengths, self.word_lengths)
        scoresList += [a]
        a = compare_dictionaries(other.stems, self.stems)
        scoresList += [a]
        a = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        scoresList += [a]
        a = compare_dictionaries(other.curse_words, self.curse_words)
        scoresList += [a]
        return scoresList

    def classify(self, source1, source2):
        """Compares the object to two other source objects"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name, scores1)
        print('scores for ' + source2.name, scores2)
        weighted_sum1 = 10*scores1[0] + 5*scores1[1] + 7*scores1[2] + 3*scores1[3] + 1*scores1[4]
        weighted_sum2 = 10*scores2[0] + 5*scores2[1] + 7*scores2[2] + 3*scores2[3] + 1*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print()
            print('The work' + ' by ' + self.name + ' is more likely to have come from ' + source1.name)
            print()
        else:
            print()
            print('The work' + ' by ' + self.name + ' is more likely to have come from ' + source2.name)
            print()

        
        
def test():
    """ A test """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ Tests the program """
    print('Loading...')
    print()
    source1 = TextModel('rowling')
    source1.add_file('harryPotter.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('sonnets.txt')

    new1 = TextModel('nathan')
    new1.add_file('billyBudd.txt')
    new1.classify(source1, source2)
    print()
    print('loading next file....')
    print()

    source3 = TextModel('Michelle Obama')
    source3.add_file('michelle.txt')

    source4 = TextModel('Donald Trump')
    source4.add_file('donald.txt')

    new2 = TextModel('Melania Trump')
    new2.add_file('melania.txt')
    new2.classify(source3, source4)

