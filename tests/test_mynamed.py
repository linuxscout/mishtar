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
from __future__ import absolute_import

import sys
sys.path.append('../')
import mishtar.mynamed

if __name__ == '__main__':
    import pyarabic.araby as araby
    TEXTS = [
        #~ u"وجد عبد الله بن عمر دينارا",
        u"جاء  خالد بن الوليد وقاتل مسيلمة بن حذام الكذاب في موقعة الحديقة",
        u'''روى أحمد بن عقيل الشامي عن أبي طلحة
     المغربي أنّ عقابا بن مسعود بن أبي سعاد قال''',
        #~ u"قال مُحَمَّدُ بْنُ خَالِدُ بْنُ إسماعيل في حديثه",
        #~ u"ِنْصَرَفْنَا إِلَى أَنَسُ بْنُ مَالِكَ الْحَديثِ",
        #~ u"ِخرج عبد الرحمن بن عوف",
        #~ u"ِخرج عبد الودود من المولد",
        #~ u"ِمررت بعبد الودود بن عمرو",
        #~ u"ِمررت بعبد الودود  في البيت",
        u"صرّح الأمير تشارلز الأول",
    ]
    for text1 in TEXTS:
        word_list = araby.tokenize(text1)

        chunker = mishtar.mynamed.myNamed()

        tag_list2 = chunker.detect_chunks(word_list)

        print "pos",chunker.detect_positions(word_list, debug=True)

        print "chunks", repr(chunker.extract_chunks(text1)).decode('unicode-escape').encode('utf8') 
        # extract chunks with context
        #~ print repr(chunker.extract_chunks(text1,context= True)).decode('unicode-escape').encode('utf8') 
        # predefined tashkeel 
        result = chunker.pretashkeel(word_list)
        print "tashkeel", (u' '.join(result))
        tuples = (zip(tag_list2, word_list))
        for tup in tuples:
            print repr(tup).decode('unicode-escape').encode('utf8')           


