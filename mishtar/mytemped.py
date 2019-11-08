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
    sys.path.append('mishtar/')
    import mishtar.chunked as chuncked
    import mytemped_const as tconst
else:
    from mishtar import chunked
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
        if word[0] in tconst.PREFIXES:
           key = word[1:]
        # كلمة ابن لا تأتي هكذا إلا في البداية
        if key in tconst.AWQAT  and key in tconst.ORDINAL2 :
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
        if word in (u"يوم",u"مدة",u"شهر",u"سنة",u"عام",u"ليلة",u"اليوم",u"الليلة",u"",u"السنة",u"العام",u"القرن")   :
             return True

        if word in tconst.DAYS:
            return True
        if word in tconst.MONTHS:
            return True
        if word in tconst.YEARS:
            return True
        if word in tconst.CALENDERS:
            return True


        if word in tconst.AWQAT:
            return True

        return False
        # calendar test if Heh for hijir or meem for Miladi
        #if word.endswith(araby.MEEM) or word.endswith(araby.HEH):
            #if word[:-1].isnumeric():
                #return True
        if word.endswith(u'م') or word.endswith(u'ه'):
            if word[:-1].isnumeric():
                return True
        if word.endswith(u'ــ') or word.endswith(u'هـ'):
            if word[:-3].isnumeric():
                return True


        return False

    def is_middle_wordtag(self, word, next_tag=""):
        """
        return if the word is a word tag only if there is a chunk
        @param word: the given word
        @type word: unicode
        """

        #كلمة من لا تدخل إلا أذا سبقها ما يدل على الزمن
        # مثل السابع من شهر
        #الحرف / يستعمل للتفريق بين تسميتين للشهر
        if word in tconst.MIDDLE_WORDS and next_tag:
            return True
        if word in tconst.ORDINAL and next_tag =="number":
            return True
        if word in tconst.ORDINAL2 and next_tag =="number":
            return True
        if word in tconst.ORDINAL2 and next_tag:
            return True
        if word in tconst.ORDINAL2 and next_tag in tconst.CALENDERS:
            return True
        if word in tconst.ORDINAL2 and next_tag in tconst.DAYS:
            return True
        if word in tconst.ORDINAL2 and next_tag in tconst.ORDINAL2:
            return True



        # يدخل العدد في العبارة إذا سبقه شيء موسوم
        if word.isnumeric():
            return True
        return False

    def is_middle_tuple_tag(self, word, previous, next_tag=""):
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


###اوائل القرن








        if previous in tconst.ORDINAL2 and word in tconst.DAYS:
            return True
        if previous in tconst.ORDINAL and word in tconst.CALENDERS:
            return True
        #if previous in tconst.ORDINAL11 and word in tconst.CALENDERS:
            #return True
        if word in tconst.ORDINAL11 and next_tag in tconst.CALENDERS:
            return True



        if previous in (u"يوم",u"لمدة") and word in (u"أسابيع" ):
             return True


        # من رمضان
        if previous in tconst.MIDDLE_WORDS and word in tconst.MONTHS:
          return True
        #if previous in tconst.MIDDLE_WORDS and word in tconst.AWQAT:
         #  return True
        if previous in tconst.MIDDLE_WORDS and word in tconst.DAYS:
           return True
       # if previous in tconst.MIDDLE_WORDS and word in tconst.ORDINAL:
         #  return True
       # if previous in tconst.MIDDLE_WORDS and word in tconst.ORDINAL1:
         #  return True
       # if previous in tconst.MIDDLE_WORDS and word in tconst.ORDINAL2:
          # return True
       # if previous in tconst.MIDDLE_WORDS and word in tconst.TEMPS:
         #  return True
        # اليوم عدد والشهر كلمة
        if previous.isnumeric() and word in tconst.MONTHS:
            return True
        if previous.isnumeric() and word in tconst.ORDINAL2:
            return True
        ##
        if previous in (u'على') and word in tconst.ORDINAL2:
            return True

        #if word in tconst.ORDINAL2 and next_tag in tconst.DAYS:
         #   return True



         #تاريخ 14
       # if word in (u'تاريخ',u'التاريخ') and next_tag in tconst.ORDINAL:
          #  return True
          #تاريخ 14
       # if word in (u'تاريخ',u'التاريخ') and next_tag in tconst.ORDINAL1:
           # return True
        #سنة وبعدها عدد
        if previous in tconst.ORDINAL2 and word.isnumeric():
            return True
        if previous in tconst.ORDINAL2 and word in tconst.ORDINAL:
            return True
        if previous in tconst.ORDINAL2 and word in tconst.ORDINAL1:
            return True
        if previous in tconst.ORDINAL2 and word in tconst.ORDINAL2:
            return True

        ##
        if previous in tconst.ORDINAL2 and word in tconst.TEMPS:
            return True

        ###
        if previous in tconst.ORDINAL2 and word in (u'طويلة', u'قصيرة',u'طويلا', u'قصيرا',u"قليلة",u"معدودة",u"معدودات"):
            return True
        ###
        if previous in tconst.CALENDERS and word in tconst.ORDINAL :
            return True
        ####
        if previous in tconst.CALENDERS and word in tconst.ORDINAL1 :
            return True


        #نة تقريباس
        if previous in tconst.ORDINAL2 and word in (u"تقريبا",u"بالتقريب",u"قاربت",u"تقارب",u"أسابيع") :
            return True
        if previous in tconst.ORDINAL2 and word in (u"خمس",u"سبع",u"ثمان",u"تسع",u"عشر",u"ست") :
            return True
        if previous in tconst.ORDINAL1 and word in (u"أيام",u"اعوام",u"ايام",u"أعوام",u"سنين",u"سنوات",u"شهور",u"يوما",u"عاما",u"أسبوعا",u"سنة",u"شهرا",u"اشهر",u"أشهر",u"أسابيع",u"اسابيع") :
            return True
        #وتسعة

        #سنة وبعدها عدد  وفي أخره ميم أو هاء
        if previous in tconst.ORDINAL2 and word[:-2].isnumeric() and word[-1:] in (u'م',u'ـ'):
            return True
        if previous in tconst.ORDINAL2 and word[:-3].isnumeric() and word[:-2] in (u"ق") and word[-1:] in (u'م',u'ه'):
            return True
        if previous in tconst.TEMPS and word.isnumeric():
            return True

        if previous in (u"ق") and word in (u"."):
            return True
        if previous.isnumeric() and word in (u"ق"):
            return True
        #heurs
        if previous in (u":") and word.isnumeric():
            return True
        if previous.isnumeric() and word in (u":"):
            return True
        #عدد وبعده تقويم
        #مثل  ميلادي
        if compsd in tconst.MONTHS:
            return True
        if previous.isnumeric() and word in tconst.CALENDERS:
            return True
        if previous.isnumeric() and word in tconst.MIDDLE_WORDS:
            return True

        if previous  in tconst.ORDINAL2  and word in tconst.CALENDERS:
            return True
        if previous  in tconst.ORDINAL2  and word in tconst.MONTHS:
            return True
        if previous  in tconst.ORDINAL1  and word in tconst.CALENDERS:
            return True
        if compsd in tconst.CALENDERS:
            return True


            #les heurs
        if previous in tconst.ORDINAL2 and word[:-3].isnumeric() and word[:-2] in (u"ق") and word[-1:] in (u'م',u'ه'):
            return True

         #temps

        if previous  in tconst.ORDINAL1  and word in tconst.TEMPS:
            return True
        if word  in tconst.ORDINAL11  and next_tag in tconst.TEMPS:
            return True
        if previous  in tconst.ORDINAL11  and word in tconst.ORDINAL2:
            return True
        if previous  in tconst.ORDINAL11  and word in tconst.CALENDERS:
            return True
        if previous  in tconst.ORDINAL  and word in tconst.TEMPS:
            return True
        if previous  in tconst.MIDDLE_WORDS  and word in tconst.TEMPS:
            return True

        if previous  in tconst.TEMPS  and word in tconst.ORDINAL:
            return True
        if previous  in tconst.TEMPS  and word in tconst.ORDINAL1:
            return True

                    #ordinal

        if word in tconst.ORDINAL11 and next_tag in tconst.ORDINAL2:
            return True



        if previous  in tconst.ORDINAL  and word in tconst.ORDINAL11:

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
        if previous in tconst.ORDINAL2 and word in tconst.ADJS:
            return True
        if previous in tconst.ADJS and word in tconst.ORDINAL2:
            return True
        if previous in tconst.ORDINAL2 and word in tconst.ORDINAL:
            return True
        if previous in tconst.ORDINAL2 and word in tconst.TEMPS:
            return True

        if previous in tconst.ORDINAL and word in tconst.ORDINAL1:
            return True
        if previous in tconst.ORDINAL1 and word in tconst.ORDINAL2:
            return True
        if previous in tconst.ORDINAL11 and word in tconst.ORDINAL2:
            return True

        if previous in tconst.ORDINAL2 and word in tconst.ORDINAL1:
            return True
        #عدد ترتيبي ثم حرف من
        if previous in  tconst.ORDINAL and word in (u"من",):
            return True
           #الفاتح من
        if previous in  (u"الفاتح") and word in (u"من",):
            return True



        if previous in  tconst.TEMPS and word in tconst.ORDINAL:
            return True

        if previous in  tconst.MIDDLE_WORDS and word in tconst.CALENDERS:
            return True

        if compsd in tconst.ORDINAL:
            return True
        if compsd in tconst.CALENDERS:
            return True
        if compsd in tconst.COMPOSED:
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
        word = araby.strip_tashkeel(word)
        if word in (u"شهر",u"عشرة",u"يوم",u"سنة",u"عام",u"اليوم",u"الشهر",u"العام",u"السنة",u"للسنة",u"ليلة",u"للعام"):
            return "tmp"
        if word in tconst.DAYS:
            return "tmp;day"
        if word in tconst.MONTHS:
            return "tmp;month"
        if word in tconst.YEARS:
            return "tmp;year"
        if word in tconst.CALENDERS:
            return "tmp;calender"
        if word in tconst.TEMPS:
            return "tmp"
        if word in tconst.AWQAT:
            return "tmp"
        if word in tconst.ORDINAL:
            return "number"
        if word in tconst.ORDINAL1:
            return "number"
        if word in tconst.ORDINAL2:
            return "number"
        if word in tconst.ADJS:
            return "adj"
        if word in tconst.MIDDLE_WORDS:
            return "prep"
        return ""
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
(u'*  الساعة 05:22 قسمين : شهر أكتوبر 1973، الخامس من نوفمبر، ',  [u'شهر أكتوبر 1973', u'الخامس من نوفمبر'] ),
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
            print("predef", repr(predef_result))
            print("treatd", repr(result) )
            tuples = (zip(tag_list2, word_list))
            for tup in tuples:
                print(repr(tup)         )
