# -*- coding: utf-8 -*-
import re
import json
import time
import datetime
import pickle

class gen_corpus(object):
    def __init__(self):
        self.inf_test = "tail.txt"
        self.inf = "cse517_tweet_scan"
        #ngram limit
        self.limit = 9
        #dics for storing ngram in memo
        self.dic0 = dict()
        self.dic1 = dict()
        self.dic2 = dict()
        self.dic3 = dict()
        self.dic4 = dict()
        self.dic5 = dict()
        self.dic6 = dict()
        self.dic7 = dict()
        self.dic8 = dict()
        self.dic9 = dict()
        self.dic_lst = [self.dic0, self.dic1, self.dic2, self.dic3, self.dic4, 
                        self.dic5, self.dic6, self.dic7, self.dic8, self.dic9]
        #target json file to store ngram corpus
        self.outfile0 = "ngram/1gram.json"
        self.outfile1 = "ngram/2gram.json"
        self.outfile2 = "ngram/3gram.json"
        self.outfile3 = "ngram/4gram.json"
        self.outfile4 = "ngram/5gram.json"
        self.outfile5 = "ngram/6gram.json"
        self.outfile6 = "ngram/7gram.json"
        self.outfile7 = "ngram/8gram.json"
        self.outfile8 = "ngram/9gram.json"
        self.outfile9 = "ngram/10gram.json"
        self.outfile_lst = [self.outfile0, self.outfile1, self.outfile2, self.outfile3, 
                            self.outfile4, self.outfile5, self.outfile6, self.outfile7, self.outfile8, self.outfile9]
        #clense the logs
        with open("logs/runtime.log", "w") as log:
                            log.write("Starteded on {}!\n".format(datetime.datetime.now()))
        with open("logs/errors.log", "w") as log:
                            log.write("Starteded on {}!\n".format(datetime.datetime.now()))

    def _ngrams(self, tokens, MIN_N, MAX_N):
        """
        helper function
        """
        n_tokens = len(tokens)
        for i in xrange(n_tokens):
            for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
                yield tokens[i:j]
        
    def gen_ngram(self, s):
        """
        function that gen ngram from string
        input: string, ie, "abc"
        output list of list [['a','b','c']['ab','bc']...]
        """
        limit = self.limit
        res = []
        s = u"\u0002" + s + u"\u0003"
        print s
        for i in xrange(min(len(s), limit)):
            tmp_lst = []
            for j in self._ngrams(s, i+1, i+1):
                tmp_lst.append(j)
            res.append(tmp_lst)
        #res.reverse()
        return res


    def extract_ngram(self):
        """
        main function
        """
        try:
            total_count = sum(1 for line in open(self.inf_test))
            print total_count
            timer = time.time()
            interval = 10000
            with open(self.inf_test, "r") as inf:

                line_count = 0
                for line in inf:
                    line_count += 1
                    if line_count%interval == 0:
                        print "{}% finished!\n".format(100*float(line_count)/float(total_count))

                        time_used = (time.time()-timer)/60
                        timer = time.time()
                        print "ETA:{}".format(time_used*((total_count-line_count)/interval))
                        with open("logs/runtime.log", "a") as log:
                            log.write("{}% finished!\n".format(100*float(line_count)/float(total_count)))
                            log.write("ETA: {} mins \n".format(time_used*((total_count-line_count)/interval)))
                    for each in [word for word in line.lower().decode('utf-8').split()]:
                        if each.startswith('#') or each.startswith('@') or each.startswith('http:') or each.startswith('https:'):
                            continue
                        else:
                            ngrams = self.gen_ngram(each)
                            #print ngrams
                            count = 0
                            for gram in ngrams:
                                for element in gram:
                                    if element in self.dic_lst[count]:
                                        self.dic_lst[count][element] += 1
                                    else:
                                        self.dic_lst[count][element] = 1
                                count += 1

            count = 0
            for outf in self.outfile_lst:
                with open(outf, 'w') as fp:
                    json.dump(self.dic_lst[count], fp)
                count += 1
            """
            output = open('output_test.txt', 'ab+')
            data = self.dic0

            pickle.dump(data, output)
            output.close()
            """

        except Exception as e:
            with open("logs/errors.log", "a") as log:
                print str(e)
                log.write(str(e)+" ###### on {}".format(datetime.datetime.now()))



obj = gen_corpus()
obj.extract_ngram()
