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

import sys
sys.path.append('../')
import mishtar.mytemped as mytemped


if __name__ == '__main__':

    texts =[
'* قسم واحد فقط: شهر نوفمبر سنة 2015، ',
u'* قسمين : شهر أكتوبر 1973، الخامس من نوفمبر، ',  
u'* ثلاثة اقسام: يوم الجمعة الخامس عشر من شهر رمضان سنة 1435 هجرية.',  
    ]
    chunker = mytemped.myTemped()
    for text1 in texts:
        word_list = araby.tokenize(text1)
        tag_list2 = chunker.detect_chunks(word_list)
        result = chunker.extract_chunks(text1)
        print(text1.encode('utf8'))

        tuples = (zip(tag_list2, word_list))
        for tup in tuples:
            print(repr(tup).decode('unicode-escape').encode('utf8')           )
            #~ print(tup)


