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
    
def evaluate(result_table):
    """
    Evaluate the result table
    """
    correct = 0
    incorrect = 0
    output_total = 0 # detected
    tests={}
    for item  in result_table:
        targets = item.get("targets",[])
        output = item.get("output",[])
        equal, inequal = eval_score(targets, output)
        correct += equal
        incorrect += inequal
        output_total += len(output)
    total = correct +  incorrect
    tests['correct'] = correct
    tests['incorrect'] = incorrect
    tests['total'] = total
    tests['total_output'] = output_total
    tests['accuracy']= correct*100.0/total
    tests['recall']  = correct*100.0/total
    tests['precision']= correct*100.0/output_total
    
    tests['fscore']=  2* tests['precision']*tests['recall'] / (tests['precision']+tests['recall'])
    return tests
    
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
    
    filename = args.filename
    command = args.command 
    debug = args.debug 
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
    # training 
    limit = int(len(texts)*80/100)
    #ignore first line
    training_texts = texts[1:limit]
    test_texts = texts[limit:]
    # result  table
    result_table_train= []
    result_table_test= []

    for key, item in enumerate(training_texts):
        text1 = item[0]
        # get all not null targets
        targets = [x.strip() for x in item[1:] if x.strip() ]
        targets = [araby.strip_tashkeel(x.strip()) for x in targets if x]
        word_list = araby.tokenize(text1)
        tag_list2 = chunker.detect_chunks(word_list)
        result = chunker.extract_chunks(text1)
        result_table_train.append({"text":text1, "targets":targets,"output":result})
        equal, inequal = eval_score(targets, result)
        print("Equal",equal, inequal)        
        
        if inequal and debug:
            # debug 
            print("ID"+str(key), text1.encode('utf8'))
            print("result")
            print(arepr(result))
            print("target")
            print(arepr(targets))
            result2 = chunker.detect_positions(word_list, debug=True)        
            print(arepr(result2))            
   
    # tests
    for item in test_texts:
        text1 = item[0]
        # get all not null targets
        targets = [x.strip() for x in item[1:] if x.strip() ]
        targets = [araby.strip_tashkeel(x.strip()) for x in targets if x]
        result = chunker.extract_chunks(text1)
        result_table_test.append({"text":text1, "targets":targets,"output":result})

    #  Print metrics
    print("\tPrec.\tRecall\tfscore\tAccu\tCorrect\tIncor.\toutput\tTotal");
    tests = evaluate(result_table_train)
    print('Train\t%.2f\t%.2f\t%.2f\t%.2f\t%d\t%d\t%s\t%d'%(tests['precision'], tests['recall'], tests['fscore'] , tests['accuracy'],tests['correct'], tests['incorrect'], tests['total_output'], tests['total']))
    tests = evaluate(result_table_test)
    print('Test \t%.2f\t%.2f\t%.2f\t%.2f\t%d\t%d\t%s\t%d'%(tests['precision'], tests['recall'], tests['fscore'] , tests['accuracy'],tests['correct'], tests['incorrect'], tests['total_output'], tests['total']))
    
    # metrics
    #~ Precision P= # of correct entities detected / # of entities detected (1)
    #~ Recall R= # of correct entities detected / # of entities manually labeled (2)
    #~ F1-score F= 2 P R / P+R
    #  citation Mesfar, S. (2007, June). Named entity recognition for arabic using syntactic grammars. In International Conference on Application of Natural Language to Information Systems (pp. 305-316). Springer, Berlin, Heidelberg
