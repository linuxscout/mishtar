#!/usr/bin/python
# -*- coding=utf-8 -*-
#
"""
Arabic Named enteties recognation pyarabic.named
@author: Taha Zerrouki
@contact: taha dot zerrouki at gmail dot com
@copyright:  Taha Zerrouki
@license: GPL
@date:2018/04/01
@version: 0.3
"""
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import pyarabic.araby as araby

       
class Chunked:
    """
    A general chunk class to detect phrases in many forms, like named, numbers, temporal, etc.
    """
    def __init__(self,):
        self.begintag = "NB"
        self.intertag = "NI"
        pass
    
    def detect_chunks(self, wordlist):
        """
        Detect named enteties words in a text and return positions of each phrase.

        Example:
            >>> detect_chunk(u"قال خالد بن رافع  حدثني أحمد بن عنبر عن خاله")
            ((1,3), (6,8))

        @param wordlist: wordlist
        @type wordlist: unicode list
        @return: list of numbers clause positions [(start,end),(start2,end2),]
        @rtype: list of tuple

        """
        started = False
        taglist = []
        previous = ""
        wordlist, wordtag_list = self.preprocess(wordlist)
        for i, word_voc in enumerate(wordlist):
            # get previous tag and next
            prev_tag = wordtag_list[i-1] if i>0 else ""
            next_tag = wordtag_list[i+1] if i<len(wordtag_list)-1 else ""
                
            #save the original word with possible harakat if exist
            word = araby.strip_tashkeel(word_voc)
            if not started:
                # if the word is a start tag word
                # a word which is a start tag like proper noun or an indicator 
                # الكلمة السابقة ليست موسومة، لكن الكلمة الحالية تجعلها كذلك
                if self.is_middle_tuple_tag(word, previous):
                    taglist.pop()
                    taglist.append(self.begintag)                                       
                    taglist.append(self.intertag)                                     
                    started = True

                #:كلمة توسم بنفسها
                elif self.is_wordtag(word):
                    taglist.append(self.begintag)
                    started = True       
                elif self.is_starttag(word):
                   taglist.append(self.begintag)
                   started = True
                else:
                    taglist.append("0")                    
                    started = False
                
            else: # توجد سلسلة منطلقة
                # الكلمة السابقة ليست موسومة، لكن الكلمة الحالية تجعلها كذلك
                if self.is_middle_tuple_tag(word, previous, next_tag):
                    taglist.append(self.intertag)

                #:كلمة توسم بنفسها
                elif self.is_wordtag(word):
                    taglist.append(self.intertag)
                # الكلمة لا تكون موسومة إلا إذا كانت مسبوقة
                elif self.is_middle_wordtag(word, next_tag):
                    # إذا كانت في آخر الجملة لا ت
                    #~ taglist.append(self.intertag+"3")
                    taglist.append(self.intertag)
                else:
                    taglist.append("0")
                    started = False;
            previous = word
        wordlist, taglist = self.postprocess(wordlist, taglist)
        return taglist
    def is_starttag(self, word):
        """
        return if the word is a start tag
        @param word: the given word
        @type word: unicode
        """
        return False

    def is_wordtag(self, word):
        """
        return if the word is a word tag any where
        @param word: the given word
        @type word: unicode
        """
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
    def preprocess(self, wordlist):
        """
        Make preprocessing for some cases 
        @param wordlist: the given wordl_ist
        @type wordlist: unicode list
        """
        taglist = []
        
        for word in wordlist:
            
            taglist.append(self.tag_word(word))

        return wordlist, taglist

    def postprocess(self, wordlist, taglist):
        """
        Make preprocessing for some cases 
        @param wordlist: the given wordl_ist
        @type wordlist: unicode list
        """
        
        return wordlist, taglist

    def tag_word(self, word):
        """
        give a tag to word
        """
        return ""        

    def extract_chunks(self, text, context=False):
        """
        Extract chunks words in a text.

        Example:
            >>> extract_chunk(u"قال خالد بن رافع  حدثني أحمد بن عنبر عن خاله")
            ("خالد بن رافع"، "أحمد بن عنبر ")

            >>> extract_chunks(u"تصدق عبد الله بن عمر بدينار", context=True)
            ("تصدق"، "عبد الله بن عمر"، "بدينار")

        @param text: input text
        @type text: unicode
        @return: named enteties words extracted from text
        @rtype: integer
        """
        phrases = []
        wordlist = araby.tokenize(text)
        positions = self.detect_positions(wordlist)

        for pos in positions:
            if len(pos) >= 2:
                if pos[0] <= len(wordlist) and pos[1] <= len(wordlist):
                    if pos[0]-1 >= 0:
                        previous = wordlist[pos[0]-1]
                    else: previous = u''
                    if pos[1]+1 < len(wordlist):
                        nextword = wordlist[pos[1]+1]
                    else: nextword = u''
                    if context:
                        phrases.append((previous, 
                        u' '.join(wordlist[pos[0]: pos[1]+1]), nextword))
                    else:
                        phrases.append(u' '.join(wordlist[pos[0]: pos[1]+1]))                        
        return phrases


    def detect_positions2(self, wordlist, debug=False):
        """
        Detect named enteties words in a text and return positions of each phrase.

        Example:
            >>> detect_positions(wordlist)
            ((1,3), (6,8))
        @param wordlist: wordlist
        @type wordlist: unicode list
        @return: list of numbers clause positions [(start,end),(start2,end2),]
        @rtype: list of tuple
        """
        positions = []
        start = -1
        end = -1
        taglist = self.detect_chunks(wordlist)
        for i, tag in enumerate(taglist):
            if tag == self.begintag:
                if start < 0:
                    start = i
                end = i
            elif tag == self.intertag:
                end = i
                start = -1
            elif start >= 0:
                    positions.append((start, end))
                    start = -1
                    end = -1
        # add the final phrases
        if start >= 0:   #There are a previous number phrase.
            positions.append((start, end))
        return positions
        
    def detect_positions(self, wordlist, debug=False):
        """
        Detect named enteties words in a text and return positions of each phrase.
        Example:
            >>> detect_positions(wordlist)
            ((1,3), (6,8))
        @param wordlist: wordlist
        @type wordlist: unicode list
        @return: list of numbers clause positions [(start,end),(start2,end2),]
        @rtype: list of tuple
        """
        positions = []
        start = -1
        end = -1
        wordlist, word_taglist = self.preprocess(wordlist)
        taglist = self.detect_chunks(wordlist)
        if debug:
            print("N", "tag", "start", "end", "pos", "word")        
        for i, tag in enumerate(taglist):
            # 
            if tag == self.begintag:
                if start < 0:
                    start = i
                end = i
            elif tag == self.intertag:
                end = i
                if start < 0:
                    start = i
                #~ start = -1
            elif start >= 0:
                    positions.append((start, end))
                    start = -1
                    end = -1
            if debug:
                print(i, tag, start, end, word_taglist[i], wordlist[i].encode('utf8'))
        # add the final phrases
        if start >= 0:   #There are a previous number phrase.
            positions.append((start, end))
        return positions        
    @staticmethod
    def get_previous_tag(word):
        """Get the word tags
        @param word: given word
        @type word: unicode
        @return: word tag
        @rtype: unicode
        """
        return ''

    @staticmethod
    def vocalize(wordlist, syn_tags=""):
        """ Vocalize a number words
        @param wordlist: words to vocalize
        @type wordlist: unicode list
        @param syn_tags: tags about the clause
        @type syn_tags: unicode
        @return: the vocalized wordlist.
        @rtype: unicode
        """
        return wordlist

    def pretashkeel(self, wordlist):
        """
        Detect chunk words in a text.
        @param wordlist: input text
        @type wordlist: unicode
        @return: wordlist with vocalized named clause
        @rtype: list
        """
        taglist = self.detect_chunks(wordlist)
        previous = ""
        vocalized_list = []
        chunk = []
        previous_tag = ""
        for word, tag in zip(wordlist, taglist):
            if tag in (self.begintag, self.intertag):
                chunk.append(word)
            else:
                if chunk:
                    # get the tag of previous word
                    previous_tag = self.get_previous_tag(previous)
                    vocalized = self.vocalize(chunk, previous_tag)
                    vocalized_list.extend(vocalized)
                    chunk = []
                vocalized_list.append(word)
                previous = word
        if chunk:
            # get the tag of previous word
            previous_tag = self.get_previous_tag(previous)
            vocalized = self.vocalize(chunk, previous_tag)
            vocalized_list.extend(vocalized)            

        return vocalized_list


if __name__ == '__main__':
    print("test it whithin mynamed or mynumber")

