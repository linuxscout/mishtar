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
import mishtar.mynamed as mynamed
import mishtar.mynumber as mynumber


import argparse
def grabargs():
    parser = argparse.ArgumentParser(description='Extract chuncks from CSV file ')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=False,
    help="Output file to convert", metavar="OUT_FILE")

    parser.add_argument("-c", dest="command", required=False,
    help="Chunks to extract: name, temp", metavar="COMMAND")
    #~ parser.add_argument("--dir", dest="data_directory",
    #~ help="Data directory for other external stemmers results", metavar="data_directory")
    
    parser.add_argument("--debug", type=bool, nargs='?',
                        const=True, 
                        help="debug result.")
    #~ parser.add_argument("--all", type=bool, nargs='?',
                        #~ const=True, 
                        #~ help="Test all stemmers.")
    args = parser.parse_args()
    return args
    
def eval_score(list_predef, list_predict):
    """ test the score of predict list in predef list """
    
    predefs = [araby.strip_tashkeel(x) for x in list_predef if x]
    predefs = [u" ".join(araby.tokenize(x)) for x in list_predef if x]
    predicts = [araby.strip_tashkeel(x) for x in list_predict if x]
    equal = 0
    inequal = 0
    for x in predefs:
        if x in predicts:
            equal += 1
        else:
            inequal += 1
    return equal, inequal
def factory_chuncker(name):
    """ create a chuncker """

    if name == "temp":
        return  mytemped.myTemped()
    elif name == "name":
        return  mynamed.myNamed()
    elif name == "number":
        return  mynumber.myNumber()
    else:
        return  mynamed.myNamed()
if __name__ == '__main__':
    args = grabargs()
    
    filename = args.filename #"samples/dataset.csv"
    #~ filename = "samples/dataset.csv"
    command = args.command 
    debug = args.debug 
    #~ print(filename, command, debug)
    #~ sys.exit()
    chunker = factory_chuncker(command)
    
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
        "total_result":0,
"test_correct":0,
        "test_incorrect":0,
        "test_total":0,        
        "test_total_result":0,        
        }
    #~ debug  = True
    #~ chunker = mytemped.myTemped()
    # training 
    limit = int(len(texts)*80/100)
    #ignore first line
    training_texts = texts[1:limit]
    test_texts = texts[limit:]
    for key, item in enumerate(training_texts):
        text1 = item[0]
        # get all not null targets
        targets = [x.strip() for x in item[1:] if x.strip() ]
        targets = [araby.strip_tashkeel(x.strip()) for x in targets if x]
        word_list = araby.tokenize(text1)
        tag_list2 = chunker.detect_chunks(word_list)
        result = chunker.extract_chunks(text1)

        equal, inequal = eval_score(targets, result)
        print("Equal",equal, inequal)        
        tests['correct'] += equal
        tests['incorrect'] += inequal
        tests['total_result'] += len(result)        
        
        if inequal and debug:
            # debug 
            print("ID"+str(key), text1.encode('utf8'))
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
        tests['test_total_result'] += len(result)
        
    tests['total'] =  tests['correct'] + tests['incorrect']
    tests['accuracy']= tests['correct']*100.0/tests['total']
    tests['recall']= tests['correct']*100.0/tests['total']
    tests['precision']= tests['correct']*100.0/tests['total_result']
    tests['fscore']=  2* tests['precision']*tests['recall'] / (tests['precision']+tests['recall'])
    #~ print("Training", tests, "accuracy %.2f%%"%accuracy)
    
    tests['test_total'] =  tests['test_correct'] + tests['test_incorrect']
    tests['test_accuracy'] = tests['test_correct']*100.0/tests['test_total']
    tests['test_recall']= tests['test_correct']*100.0/tests['test_total']
    tests['test_precision']= tests['test_correct']*100.0/tests['test_total_result']
    tests['test_fscore']=  2* tests['test_precision']*tests['test_recall'] / (tests['test_precision']+tests['test_recall'])

    #~ print("Test", tests, "accuracy %.2f%%"%accuracy)
    print("\tPrec.\tRecall\tfscore\tAccu\tCorrect\tIncor.\tTotal");
    print('Train\t%.2f\t%.2f\t%.2f\t%.2f\t%d\t%d\t%d'%(tests['precision'], tests['recall'], tests['fscore'] , tests['accuracy'],tests['correct'], tests['incorrect'], tests['total']))
    print('Test\t%.2f\t%.2f\t%.2f\t%.2f\t%d\t%d\t%d'%(tests['test_precision'], tests['test_recall'], tests['test_fscore'] , tests['test_accuracy'],tests['test_correct'], tests['test_incorrect'], tests['test_total'])) 
    #~ print('Test\t%.2f\t%d\t%d\t%d'%(tests['test_accuracy'],tests['test_correct'], tests['test_incorrect'], tests['test_total']))
    # metrics
    #~ Precision P= # of correct entities detected / # of entities detected (1)
    #~ Recall R= # of correct entities detected / # of entities manually labeled (2)
    #~ F1-score F= 2 P R / P+R
    #  citation Mesfar, S. (2007, June). Named entity recognition for arabic using syntactic grammars. In International Conference on Application of Natural Language to Information Systems (pp. 305-316). Springer, Berlin, Heidelberg
