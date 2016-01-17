# -*- coding: utf-8 -*-

import json

class laplaceSmoothing(object):
    def __init__(self):
        self.ngram_json = ["ngram/1gram.json", "ngram/2gram.json", "ngram/3gram.json", 
                                 "ngram/4gram.json", "ngram/5gram.json", "ngram/6gram.json", 
                                 "ngram/7gram.json", "ngram/8gram.json", "ngram/9gram.json"]
        self.n1gram = dict()
        self.n2gram = dict()
        self.n3gram = dict()
        self.n4gram = dict()
        self.n5gram = dict()
        self.n6gram = dict()
        self.n7gram = dict()
        self.n8gram = dict()
        self.n9gram = dict()
        self.ngram_corpus = [self.n1gram, self.n2gram, self.n3gram,
                             self.n4gram, self.n5gram, self.n6gram, 
                             self.n7gram, self.n8gram, self.n9gram]
        
        for i in xrange(9):
            with open(self.ngram_json[i]) as tmpf:    
                self.ngram_corpus[i] = json.load(tmpf)
            #print "{0}gram (type:{2}): {1}\n".format(i, self.ngram_corpus[i], type(self.ngram_corpus[i]))
        print "{0}gram (type:{2}): {1}\n".format(1, self.ngram_corpus[0], type(self.ngram_corpus[i]))

        #total tokens of unigram
        self.N = 0
        for each in self.ngram_corpus[0].values():
            self.N += each
        print "N is {}".format(self.N)

        #vocabulary size for each ngram
        self.V = [0]*9
        for i in xrange(9):
            self.V[i] = len(self.ngram_corpus[i])
            print "{0}gram's V size: {1}\n".format(i+1, self.V[i])


    def get_laplace_proba(self, ngram, word):
        word = word.decode('utf-8')
        print word
        #unigram 
        if ngram ==1:
            if word in self.ngram_corpus[ngram-1]:
                print "count found {}".format(self.ngram_corpus[ngram-1][word])
                laplace_proba = float(self.ngram_corpus[ngram-1][word]+1)/float(self.N+self.V[ngram-1])
            else:
                print "Unseen word."
                laplace_proba = float(1)/float(self.N+self.V[ngram-1])

        #2-9gram
        else:
            prev = word[:-1]
            if prev in self.ngram_corpus[ngram-1]:
                prev_count = self.ngram_corpus[ngram-1][prev]
            else:
                prev_count = 0
                
            if word in self.ngram_corpus[ngram-1]:
                print "count found {}".format(self.ngram_corpus[ngram-1][word])
                laplace_proba = float(self.ngram_corpus[ngram-1][word]+1)/float(prev_count + self.V[ngram-2])
            else:
                print "Unseen Word!"
                laplace_proba = float(1)/float(prev_count + self.V[ngram-2])

        print "laplace proba of {0}: {1}".format(word.encode('utf-8'), laplace_proba)
        return laplace_proba
        
        
obj = laplaceSmoothing()
obj.get_laplace_proba(4, "wifi")

