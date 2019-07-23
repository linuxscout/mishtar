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
import pyarabic.named_const as named_const
import pyarabic.propernouns as propernouns

if __name__ == '__main__':

    import sys
    sys.path.append('../')
    import chunked
    import mytemped_const as tconst    
else:
    from . import chunked       
    from . import mytemped_const as tconst


class myTemped(chunked.Chunked):
    """
    A general chunk class to detect phrases in many forms, like named, numbers, temporal, etc.
    """
    def __init__(self,):
        #~ super(chunked.Chunked).__init__()
        #~ super(myTemped, self).__init__()
        chunked.Chunked.__init__(self,)
        self.begintag = "NB"
        self.intertag = "NI"
    
    def is_starttag(self, word):
        """
        return if the word is a start tag
        @param word: the given word
        @type word: unicode
        """
        key = word
        # if the word is precedded by a prefix, we extract the prefix and 
        if word[0] in (u'و', u'ف', u'ل', u'ب', u'ك'):
           key = word[1:]
        # كلمة ابن لا تأتي هكذا إلا في البداية
        if key in (u'شهر', u"يوم", u"سنة", u"عام", u"اليوم", u"الشهر", u"العام", u"السنة"  ):
           return True
        # if the word is  a word tag or as a prefixed word
        if self.is_wordtag(key):
            return True
        
        return False

    def is_wordtag(self, word):
        """
        return if the word is a word tag any where
        @param word: the given word
        @type word: unicode
        """
        # some words
        if word in (u'شهر', u'يوم', ):
            return True
        if word in tconst.DAYS:
            return True
        if word in tconst.MONTHS:
            return True
        # calendar test if Heh for hijir or meem for Miladi
        if word.endswith(araby.MEEM) or word.endswith(araby.HEH):
            if word[:-1].isnumeric():
                return True
        return False

    def is_middle_wordtag(self, word):
        """
        return if the word is a word tag only if there is a chunk
        @param word: the given word
        @type word: unicode
        """
        #كلمة من لا تدخل إلا أذا سبقها ما يدل على الزمن
        # مثل السابع من شهر
        #الحرف / يستعمل للتفريق بين تسميتين للشهر
        if word in tconst.MIDDLE_WORDS:
            return True
        # يدخل العدد في العبارة إذا سبقه شيء موسوم
        if word.isnumeric():
            return True
        return False

    def is_middle_tuple_tag(self, word, previous):
        """
        return if the word is a word tag only if there the previous word is an indicator
        @param word: the given word
        @type word: unicode
        """
        if not previous:
            return False
        # one letter prefixes
        if previous[0] in  tconst.PREFIXES:
           previous = previous[1:]
        # prefix wit two letters
        if previous[:1] in  tconst.PREFIXES:
           previous = previous[2:]
        compsd = u" ".join([previous, word])
        # من شهر
        if previous in (u'من', u'في') and word in (u'شهر', u"يوم", u"سنة", u"عام", u"اليوم", u"الشهر", u"العام", u"السنة"  ):
           return True
        # من رمضان
        if previous in (u'من',u'في') and word in tconst.MONTHS:
           return True
        # اليوم عدد والشهر كلمة
        if previous.isnumeric() and word in tconst.MONTHS:
            return True
        #سنة وبعدها عدد
        if previous in tconst.PRE_NUMERIC and word.isnumeric():
            return True
        #سنة وبعدها عدد  وفي أخره ميم أو هاء
        if previous in tconst.PRE_NUMERIC and word[:-1].isnumeric() and word[-1:] in (u'م',u'ه'):
            return True
        #عدد وبعده تقويم
        #مثل  ميلادي
        if previous.isnumeric() and word in tconst.CALENDERS:
            return True
        if compsd in tconst.CALENDERS:
            return True
            
        #شهر وبعده عدد
        if previous in tconst.MONTHS and word.isnumeric():
            return True
        #شهر /يوم/عام بعده صفة
        if previous in tconst.MONTHS and word in tconst.ADJS:
            return True
        if compsd in tconst.MONTHS:
            return True            
        if previous in tconst.DAYS and word in tconst.ADJS:
            return True
        if previous in ( u"السنة", u"العام") and word in tconst.ADJS:
            return True
            
        #عدد ترتيبي ثم حرف من
        if previous in  tconst.ORDINAL and word in (u"من",):
            return True
        if compsd in tconst.ORDINAL:
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
        if word in named_const.NOUN_NASEB_LIST:
            return u'منصوب'
        elif word in named_const.JAR_LIST:
            return u'مجرور'
        elif word in named_const.RAFE3_LIST:
            return u'مرفوع'
        else:
            return u''

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
        newlist = wordlist
        return newlist
        
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
        taglist = self.detect_chunks(wordlist)
        if debug:
            print("N", "tag", "start", "end", "word")        
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
                print(i, tag, start, end, wordlist[i].encode('utf8'))
        # add the final phrases
        if start >= 0:   #There are a previous number phrase.
            positions.append((start, end))
        return positions


if __name__ == '__main__':
    import pyarabic.named as named
    test_tuples =[
 ("""أعداد معتصمي النهضة وصل عصر يوم الجمعة التاسع من أغسطس/آب 2013 -وهو أحد أيام الكثافة العددية.""",
[u'يوم الجمعة التاسع من أغسطس / آب 2013',]),
("""منذ مذبحة رابعة في الـ14 من أغسطس/آب 2013، تتشابه حكاياتهم ومآسي من تركوهم 
وفي هذا السياق، يرى المتحدث  أن النظام المصري سيتخلص ممن شارك في ثورة 25 يناير 2011، """, 
[u'الـ14 من أغسطس/آب 2013',u' 25 يناير 2011', ]),
("""وانتقد عدد من النشطاء الحقوقيين المحليين المذبحة، وقال المدون وائل عباس إن أعداد ضحايا الفض لم يسبق له مثيل في مصر منذ حرب أكتوبر 1973 ونكسة 1967، مشيرا إلى أنه حادث إجرامي يجب أن يحاسب مرتكبوه، وأشار الناشط السياسي علاء عبد الفتاح إلى أنها مجزرة أسوأ من الكوابيس والخيالات.""",

[u'أكتوبر 1973', ]),

("""وحتى خلال الهبة -التي تشهدها الأراضي الفلسطينية منذ أكتوبر/تشرين الأول 2015- في الضفة الغربية """,
  [u'أكتوبر / تشرين الأول 2015', ]), 
     
(u'يتكون من  اسم يوم الأسبوع لفظايتكون من  اسم يوم الأسبوع لفظا مثل ',  [] ),
(u'* الجمعة',  [u'الجمعة'] ),
(u'* يوم الأحد',  [u'يوم الأحد'] ),
(u'ويضم رقم اليوم في الشهر: ',  [] ),
(u'* الجمعة 14',  [u'الجمعة 14'] ),
(u'* يوم الأحد الثاني ',  [u'يوم الأحد الثاني'] ),
(u'* السبت الخامس والعشرون ',  [u'السبت الخامس والعشرون'] ),
(u'* اليوم الثالث عشر ',  [u'اليوم الثالث عشر'] ),
(u'* الثالث عشر',  [] ),
(u'* 14 نوفمبر',  [u'14 نوفمبر'] ),
(u'* غرة رمضان',  [u'غرة رمضان'] ),
(u'* الفاتح من شعبان',  [u'الفاتح من شعبان'] ),
(u'* الشهر السادس',  [u'الشهر السادس'] ),
(u'* شهر 5',  [u'شهر 5'] ),
(u'* 14/05/2016',  [u'14/05/2016'] ),
(u'* من شهر آب',  [u'من شهر آب'] ),
(u'* من شهر رمضان',  [u'من شهر رمضان'] ),
(u'* رمضان 1437',  [u'رمضان 1437'] ),
(u'* من شهر ذي القعدة',  [u'من شهر ذي القعدة'] ),
(u'* شهر ذي القعدة',  [u'شهر ذي القعدة'] ),
(u'* شهر جمادى الأولى',  [u'شهر جمادى الأولى'] ),
(u'* جمادى الآخرة',  [u'جمادى الآخرة'] ),
(u'* جمادى الثانية',  [u'جمادى الثانية'] ),
(u'* 14 أكتوبر / تشرين الأول',  [u'14 أكتوبر / تشرين الأول'] ),
(u'* الشهر الجاري',  [u'الشهر الجاري'] ),
(u'* الشهر الحالي',  [u'الشهر الحالي'] ),
(u'* السنة الجارية',  [u'السنة الجارية'] ),
(u'* السنة الماضية',  [u'السنة الماضية'] ),
(u'* السنة القادمة',  [u'السنة القادمة'] ),
(u'* العام الجاري',  [u'العام الجاري'] ),
(u'* العام الماضي',  [u'العام الماضي'] ),
(u'* العام الفائت',  [u'العام الفائت'] ),
(u'* العام المنصرم',  [u'العام المنصرم'] ),
(u'* سنة 450م',  [u'سنة 450م'] ),
(u'* سنة 19 ق.م.',  [u'سنة 19 ق.م.'] ),
(u'* عام 2015',  [u'عام 2015'] ),
(u'* 15 هجري',  [u'15 هجري'] ),
(u'* 15 هجرية ',  [u'15 هجرية'] ),
(u'* 15 للهجرة',  [u'15 للهجرة'] ),
(u'15 هـ',  [u'15 هـ'],),
(u'15 هجرية',  [u'15 هجرية'],),
(u'15 هجري',  [u'15 هجري'],),
(u'15 للهجرة',  [u'15 للهجرة'],),
(u'4 قبل الهجرة',  [u'4 قبل الهجرة'],),
(u'4 ق.ه.',  [u'4 ق.ه.'],),
(u'15 م',  [u'15 م'],),
(u'15 ميلادي',  [u'15 ميلادي'],),
(u'15 ميلادية',  [u'15 ميلادية'],),
(u'15 للميلاد',  [u'15 للميلاد'],),
(u'15 قبل الميلاد',  [u'15 قبل الميلاد'],),
(u'15 ق.م. ',  [u'15 ق.م. '],),
(u'""تتركب العبارة التاريخية من :"',  [] ),
(u'* قسم واحد فقط: سنة 2015، شهر نوفمبر',  [u'سنة 2015', u'شهر نوفمبر'] ),
(u'* قسمين : شهر أكتوبر 1973، الخامس من نوفمبر، ',  [u'شهر أكتوبر 1973', u'الخامس من نوفمبر'] ),
(u'* ثلاثة اقسام: يوم الجمعة الخامس عشر من شهر رمضان سنة 1435 هجرية.',  [u'يوم الجمعة الخامس عشر من شهر رمضان سنة 1435 هجرية'] ),

    ]
    chunker = myTemped()
    for tuple_test in test_tuples:
        text1 = tuple_test[0];
        predef_result = tuple_test[1]

        word_list = araby.tokenize(text1)
        tag_list2 = chunker.detect_chunks(word_list)
        result = chunker.extract_chunks(text1)
        if result != predef_result:
            print("predef", repr(predef_result).decode('unicode-escape').encode('utf8'))
            print("treatd", repr(result).decode('unicode-escape').encode('utf8') )
            tuples = (zip(tag_list2, word_list))
            for tup in tuples:
                print(repr(tup).decode('unicode-escape').encode('utf8')           )


