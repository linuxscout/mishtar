#!/usr/bin/python
# -*- coding=utf-8 -*-
"""
Arabic numbers routins
@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright: Arabtechies, Arabeyes, Taha Zerrouki
@license: GPL
@date:2017/02/14
@version: 0.3
# ArNumbers is imported from
license:   LGPL <http://www.gnu.org/licenses/lgpl.txt>
link      http://www.ar-php.org
category  Text
author    Khaled Al-Shamaa <khaled.alshamaa@gmail.com>
copyright 2009 Khaled Al-Shamaa
"""
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import math
import pyarabic.araby as araby
import pyarabic.number_const as nbconst
import pyarabic.named_const as nmconst
import pyarabic.number as number

if __name__ == '__main__':

    import sys
    sys.path.append('../')

    #~ import pyarabic.place_const as plconst
    import place_const as plconst
    import chunked
else:
    from . import place_const as plconst
    from . import chunked
    


class myPlace(chunked.Chunked):
    """
    A general chunk class to detect phrases in many forms, like named, numbers, temporal, etc.
    """
    def __init__(self,):
        self.begintag = "PB"
        self.intertag = "PI"
    
    def is_starttag(self, word):
        """
        return if the word is a start tag
        @param word: the given word
        @type word: unicode
        """
        key = word
        # the first word can have prefixes
        if word and word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
            key = word[1:]
        if key in plconst.PLACE_STARTWORDS:
            return True
        return False

    def is_wordtag(self, word):
        """
        return if the word is a word tag any where
        @param word: the given word
        @type word: unicode
        """
        key = word
        # some words must have WAW prefix
        if key in plconst.PLACE_WORDS:
            return True
        return False

    def is_middle_wordtag(self, word):
        """
        return if the word is a word tag only if there is a chunk
        @param word: the given word
        @type word: unicode
        """
        return False

    def is_middle_tuple_tag(self, word, previous):
        """
        return if the word is a word tag only if there the previous word is an indicator
        @param word: the given word
        @type word: unicode
        """
        key = previous
        # the first word can have prefixes
        if previous and previous[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
            key = previous[1:]
        if key in plconst.PLACE_STARTWORDS:
            return True
        return False

    @staticmethod
    def get_previous_tag(word):
        """Get the word tags
        @param word: given word
        @type word: unicode
        @return: word tag
        @rtype: unicode
        """
        word = araby.strip_tashkeel(word)
        #~ tags = u''
        if word in plconst.NOUN_NASEB_LIST:
            return u'منصوب'
        elif word in plconst.JAR_LIST:
            return u'مجرور'
        elif word in plconst.RAFE3_LIST:
            return u'مرفوع'
        else:
            return u''

    @staticmethod
    def vocalize(wordlist, syn_tags=""):
        """ Vocalize a place words clause

        @param wordlist: words to vocalize
        @type wordlist: unicode list
        @param syn_tags: tags about the clause
        @type syn_tags: unicode
        @return: the vocalized wordlist.
        @rtype: unicode
        """
        newlist = []
        return wordlist


if __name__ == '__main__':
    #import number as ArabicNumberToLetters
    TEXTS = [
             u'السلام عليكم 2014',
             u'زرت مملكة المغرب في الصيف',
             u'كان نهر النيل جميلا',
             u'جمهورية البرازيل تنافس الأقوياء',
            ]
    for txt in TEXTS:
        word_list = araby.tokenize(txt)

        myplace = myPlace()
        positions_phrases2 = myplace.detect_positions(word_list)
        print("#########")
        print(txt)
        print("positions", positions_phrases2)
        tag_list2 = myplace.detect_chunks(word_list)
        for tup in zip(tag_list2, word_list):
            print(tup)
        
        print("tashkeel", myplace.pretashkeel(word_list))
