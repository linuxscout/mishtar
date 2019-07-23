#!/usr/bin/python
# -*- coding=utf-8 -*-
#
"""
Arabic Named enteties recognation pyarabic.named
@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright: Arabtechies,  Arabeyes,   Taha Zerrouki
@license: GPL
@date:2017/02/14
@version: 0.3
"""
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr

import sys
sys.path.append('../')
import mishtar.mytemped as mytemped

def eval_score(list_predef, list_predict):
    """ test the score of predict list in predef list """
    
    predefs = [x for x in list_predef if x]
    predicts = [x for x in list_predict if x]
    equal = 0
    inequal = 0
    for x in predefs:
        if x in predicts:
            equal += 1
        else:
            inequal += 1
    return equal, inequal

if __name__ == '__main__':
    filename = "samples/dataset.csv"
    
    texts = []
    # the file contains three fields (input text, first output, second output)
    # output can be null
    with open(filename) as fl:
        for line in fl :
        #line = fl.readline()
            line = line.decode('utf8')
            fields = line.split('\t')
            if len(fields) >= 3:
                texts.append(fields)
    #~ print(texts)
    #~ sys.exit()
    #~ texts =[
#~ '* قسم واحد فقط: شهر نوفمبر سنة 2015، ',
#~ u'* قسمين : شهر أكتوبر 1973، الخامس من نوفمبر، ',  
#~ u'* ثلاثة اقسام: يوم الجمعة الخامس عشر من شهر رمضان سنة 1435 هجرية.',  
    #~ ]
    tests={"correct":0,
        "incorrect":0,
        "total":0,
"test_correct":0,
        "test_incorrect":0,
        "test_total":0,        
        }
    debug  = True
    chunker = mytemped.myTemped()
    # training 
    limit = int(len(texts)*80/100)
    training_texts = texts[:limit]
    test_texts = texts[limit:]
    for item in training_texts:
        text1 = item[0]
        # get all not null targets
        targets = [x.strip() for x in item[1:] if x.strip() ]
        targets = [araby.strip_tashkeel(x.strip()) for x in targets if x]
        word_list = araby.tokenize(text1)
        tag_list2 = chunker.detect_chunks(word_list)
        result = chunker.extract_chunks(text1)

        equal, inequal = eval_score(targets, result)
        tests['correct'] += equal
        tests['incorrect'] += inequal
        
        if inequal and debug:
            # debug 
            print(text1.encode('utf8'))
            print("result")
            print(arepr(result))
            print("target")
            print(arepr(targets))
            #~ result2 = chunker.detect_chunks(word_list)        
            #~ print(arepr(result2))        
            result2 = chunker.detect_positions(word_list, debug=True)        
            print(arepr(result2))            
        
        #~ tuples = (zip(tag_list2, word_list))
        #~ for tup in tuples:
            #~ print(repr(tup).decode('unicode-escape').encode('utf8'))

   
    # tests
    for item in test_texts:
        text1 = item[0]
        # get all not null targets
        targets = [x.strip() for x in item[1:] if x.strip() ]
        targets = [araby.strip_tashkeel(x.strip()) for x in targets if x]
        result = chunker.extract_chunks(text1)
        equal, inequal = eval_score(targets, result)
        tests['test_correct'] += equal
        tests['test_incorrect'] += inequal
        
    tests['total'] =  tests['correct'] + tests['incorrect']
    accuracy = tests['correct']*100.0/tests['total']
    print("Training", tests, "accuracy %.2f%%"%accuracy)
    
    tests['test_total'] =  tests['test_correct'] + tests['test_incorrect']
    accuracy = tests['test_correct']*100.0/tests['test_total']
    print("Test", tests, "accuracy %.2f%%"%accuracy)
    #~ print(len(test_texts))
    #~ print(len(training_texts))
    #~ print(len(texts))
    #~ print(int(len(texts)*80.0/100))



