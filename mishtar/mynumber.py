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
from __future__ import absolute_import

import math
import pyarabic.araby as araby
import pyarabic.number_const as nbconst
import pyarabic.named_const as nmconst
import pyarabic.number as number
if __name__ == '__main__':
    import sys
    sys.path.append('../')
    import chunked
else:
    from . import chunked
    


class myNumber(chunked.Chunked):
    """
    A general chunk class to detect phrases in many forms, like named, numbers, temporal, etc.
    """
    def __init__(self,):
        self.begintag = "DB"
        self.intertag = "DI"
    
    def is_starttag(self, word):
        """
        return if the word is a start tag
        @param word: the given word
        @type word: unicode
        """
        key = word
        # the first word can have prefixes
        if word and word != u'واحد' \
            and word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
            key = word[1:]
        if key in nbconst.NUMBER_WORDS or key.isnumeric():
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
        if word != u'واحد' and word.startswith(u'و'):
            key = word[1:]
        if key in nbconst.NUMBER_WORDS or key.isnumeric():
            if key not in (u'أحد', u'إحدى', u'اثنا', u'اثني', u'اثنتي', \
             u'اثنتا')  or nextword in (u'عشر', u'عشرة'):        
                return True
        return False

    def is_middle_wordtag(self, word, next_tag=""):
        """
        return if the word is a word tag only if there is a chunk
        @param word: the given word
        @type word: unicode
        """
        return False

    def is_middle_tuple_tag(self, word, previous, next_tag=""):
        """
        return if the word is a word tag only if there the previous word is an indicator
        @param word: the given word
        @type word: unicode
        """
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
        if word in nmconst.NOUN_NASEB_LIST:
            return u'منصوب'
        elif word in nmconst.JAR_LIST:
            return u'مجرور'
        elif word in nmconst.RAFE3_LIST:
            return u'مرفوع'
        else:
            return u''

    @staticmethod
    def vocalize(wordlist, syn_tags=""):
        """ Vocalize a number words clause

        Example:
            >>> txt = u"خمسمئة وثلاثة وعشرين"
            >>> wordlist = araby.tokenize(txt)
            >>> vocalized = vocalize_number(wordlist)
            >>> print u" ".join(vocalized)
            خَمْسمِئَة وَثَلاثَة وَعِشْرِينَ

        @param wordlist: words to vocalize
        @type wordlist: unicode list
        @param syn_tags: tags about the clause
        @type syn_tags: unicode
        @return: the vocalized wordlist.
        @rtype: unicode
        """
        newlist = []
        prefix = u""
        nextword = u""
        # we can pass tags to this number word
        tags = syn_tags
        if len(wordlist) == 1:
            word = wordlist[0]
            word_nm = araby.strip_tashkeel(word)
            key = word_nm
            voc = word
            # the first word can have prefixes
            if word_nm and not wordlist and word_nm != u'واحد' \
                 and word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
                if word_nm[0] in (u'ل', u'ب', u'ك'):
                    tags += u"مجرور"
                key = word[1:]
            elif word_nm != u'واحد' and word_nm.startswith(u'و'):
                key = word_nm[1:]
            # تحذب بعض الكلمات لأنها تلتبس مع أسماء الأجزاء مثل خُمس وخمس
            if key in nbconst.NUMBER_WORDS and \
              key not in (u'عشر', u'خمس', u'سبع', u'تسع', u'خمسا', \
    u'سبعا', u'تسعا', u'عشرا', u'ألفين', u'عشرة', u'صفر', u'ألف'):
                voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['i']
            return [voc, ]
        for i, word in enumerate(wordlist):
            #save the original word with possible harakat if exist
            #~ word = wordlist[i]
            word_nm = araby.strip_tashkeel(word)
            key = word_nm
            # the first word can have prefixes
            if i == 0 and word_nm and word_nm != u'واحد' and\
                word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
                if word_nm[0] in (u'ل', u'ب', u'ك'):
                    tags += u"مجرور"
                key = word[1:]
            elif word_nm != u'واحد' and word_nm.startswith(u'و'):
                key = word_nm[1:]
            if key in nbconst.NUMBER_WORDS:
                if word_nm.endswith(u'ين'):
                    tags += u"مجهول" # إما مجرور أو منصوب
                elif word_nm.endswith(u'ان')  or word_nm.endswith(u'ون'):
                    tags += u"مرفوع"
        #add tashkeel
        #wordlist = araby.stripTashkeel(u" ".join(wordlist)).split(' ')
        pre_key = u''
        for i, word in enumerate(wordlist):
            #~ word = wordlist[i]
            if i+1 < len(wordlist):
                nextword = wordlist[i+1]
            else: nextword = u""
            key = word
            # the first word can have prefixes
            if word and word != u'واحد' and\
                word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
                key = word[1:]
                prefix = word[0]
                if prefix in  (u'و', u'ف', u'ك'):
                    prefix += u'َ'
                elif prefix in  (u'ل', u'ب'):
                    prefix += u'ِ'
            else:
                prefix = u''
            if key in nbconst.VOCALIZED_NUMBER_WORDS:
                voc = u''
                if nbconst.VOCALIZED_NUMBER_WORDS[key]['s'] == "*":
                    voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['i']

                # مبني على النصب في حالة المركب العددي
                elif nextword == u'عشر' or nextword == u'عشرة':
                    voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['n']
                # مبني على النصب في حالة المركب العددي
                elif key == u'عشر' and pre_key in nbconst.NUMBER_TEN_MASCULIN_UNITS:
                    voc = u'عَشَرَ'
                elif key == u'عشرة' and pre_key in nbconst.NUMBER_TEN_FEMININ_UNITS:
                    voc = u'عَشْرَةَ'
                elif u'مرفوع' in tags:
                    if nextword.startswith(u'و'):
                        voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['r2']
                    else:
                        voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['r']
                elif u'مجهول' in tags:
                    voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['i']

                elif u'مجرور' in tags:
                    if nextword.startswith(u'و'):
                        voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['j2']
                    else:
                        voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['j']
                # منصوب
                elif u'منصوب' in tags:
                    if nextword.startswith(u'و'):
                        voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['n2']
                    else:
                        voc = prefix + \
                          nbconst.VOCALIZED_NUMBER_WORDS[key]['n']
                else:
                    voc = prefix + nbconst.VOCALIZED_NUMBER_WORDS[key]['i']
                newlist.append(voc)
            else:
                newlist.append(prefix+key)
            pre_key = key
        return newlist
    @staticmethod
    def text2number(text):
        """
        Convert arabic text into number, for example convert تسعة وعشرون = >29.

        Example:
            >>> text2number(u"خمسمئة وثلاث وعشرون")
            523

        @param text: input text
        @type text: unicode
        @return: number extracted from text
        @rtype: integer
        """
        #the result total is 0
        total = 0
        # the partial total for the three number
        partial = 0
        text = araby.strip_tashkeel(text)
        words = text.split(u' ')
        #print words
        for word in words:
            if word and word != u'واحد' and word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
                word = word[1:]
            if word != u'واحد' and word.startswith(u'و'):
                word = word[1:]

            if word in nbconst.NUMBER_WORDS:
                actualnumber = nbconst.NUMBER_WORDS[word]
                if actualnumber % 1000 == 0:
                    # the case of 1000 or 1 million
                    if partial == 0:
                        partial = 1
                    total += partial* actualnumber
                    #re-initiate the partial total
                    partial = 0
                else:
                    partial += nbconst.NUMBER_WORDS[word]
        # add the final partial to total
        total += partial
        return total

    @staticmethod
    def is_unit(word):
        """
        return if the given word is a unit
        @param word: given word to be tested
        @type word: unicode
        @return: if word is a unit return True else False.
        @rtype: Boolean
        """
        return word in nbconst.UNIT_WORDS
    @staticmethod
    def vocalize_unit(numeric, unit):
        """ Vocalize a number words
        @param numeric: given number
        @type numeric: integer
        @param unit: unit to vocalize
        @type unit: unicode
        @return: the vocalized unit, or unit word if itsnt a unit word.
        @rtype: unicode
        """
        #detect tags
        # The given word is not a unit
        unit_nm = araby.strip_tashkeel(unit)
        if not is_unit(unit_nm):
            return unit
        tags = u""
        vocalizedunit = unit

        # العدد بين واحد واثنان يتطلب صفة للوحدة ويكون بعدها
        # هذه الحالة لا تبرمج

        if numeric >= 0 and numeric <= 2:
            return unit
        # الإضافة إلى تمييز مضاف  إليه مجرور مفرد
        # تممييز الألف والمئة والمليون والمليار
        # يتطلب إضافة إلى مفرد
        # مثلا ألف رجل
        elif  numeric % 100 == 0 or  numeric % 1000 == 0:
            tags = u'SingleMajrour'
            vocalizedunit = nbconst.UNIT_WORDS[unit_nm]['a']
        # العدد المفرد يتطلب
        # إضافة إلى الجمع
        elif numeric % 100 <= 10:
            tags += "Plural"
            vocalizedunit = nbconst.UNIT_WORDS[unit_nm]['p']

        elif numeric % 100 < 100:
            tags += 'SingleMansoub'
            vocalizedunit = nbconst.UNIT_WORDS[unit_nm]['n']
        else:
            tags = ''
            vocalizedunit = nbconst.UNIT_WORDS[unit_nm]['i']
        if not vocalizedunit:
            return 'Error' + tags
        else:
            return vocalizedunit



if __name__ == '__main__':
    #import number as ArabicNumberToLetters
    TEXTS = [u"مليونان وألفان وإثنا عشر",
             u"جاء مليونان وألفان وإثنا عشر",
             u"وجدت خمسمئة وثلاث وعشرون دينارا",
             u"خمسمئة وثلاث وعشرون دينارا",
             u"وجدت خمسمئة وثلاثة وعشرين دينارا فاشتريت ثلاثة عشر دفترا",
             u"لم أجد شيئا",
             u"وجدت خمسمئة وثلاثة وعشرين دينارا فاشتريت ثلاثة عشر دفترا",
             u'من ثلاثمئة وخمسين بلدا ',
             u'من ثلاثمئة وخمسين بلدا ',
             u'من أربعمئة وخمسين بلدا ',
             u'السلام عليكم 2014',
            ]
    #~ arepr = arabrepr.ArabicRepr()
    for txt in TEXTS:
        word_list = araby.tokenize(txt)
        positions_phrases = number.detect_number_phrases_position(word_list)
        print("*******")
        print(txt)
        print("positions", positions_phrases)
        nb_phrases = number.extract_number_phrases(txt)
        tag_list = number.detect_numbers(word_list)
        for tup in zip(tag_list, word_list):
            print(tup)
        
        print("tashkeel", repr(number.pre_tashkeel_number(word_list)))

        mynumber = myNumber()
        positions_phrases2 = mynumber.detect_positions(word_list)
        print("#########")
        print(txt)
        print("positions", positions_phrases2)
        tag_list2 = mynumber.detect_chunks(word_list)
        for tup in zip(tag_list2, word_list):
            print(tup)
        
        print("tashkeel", mynumber.pretashkeel(word_list))
        if tag_list2  != tag_list:
            print("error")
            for tup in zip(tag_list, tag_list2, word_list):
                print(tup)
