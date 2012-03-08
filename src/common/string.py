import re
import unicodedata
import string
from common.funcfun import sreduce
import html.entities
from collections import Counter
from common.czech_stemmer import cs_stem
from common.porter2 import en_stem

savedStems = {}
wordCounter = Counter()

def createStem(word, lang, save=False):
	if save:
		try:
			stem = savedStems[word]
		except Exception:
			stem = getLangStem(word, lang)
			savedStems[word] = stem
		wordCounter[word] += 1
		return stem
	else:
		return getLangStem(word, lang)

def getLangStem(word, lang):
	if lang == 'cs':
		return cs_stem(word, False)
	elif lang == 'en':
		return en_stem(word)
	else:
		raise Exception('Language not supported. ' + str(lang))

def replace_single(text, strings, replacement):
	return re.sub('|'.join(map(re.escape, strings)), replacement, text)	

def replace_dict(text, dic):
	for k, v in dic.items():
		text = text.replace(k, v)
	return text

def sjoin(lst):
	return ''.join(map(str, lst))

def isletter(char):
	if strip_accents(char).lower() in string.ascii_lowercase:
		return char
	else:
		return False

def strip_accents(s): 
	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def replace_white_spaces(text, replace = ''):
	return re.sub('\s+', replace, text)

def remove_nonletters(text, replace = '', keep = []):
	return sjoin(map(lambda x: isletter(x) or keep_nonletters(x, keep) or replace, text))

def keep_nonletters(x, keep):
	if x in keep:
		return x
	else:
		return False

def normalize_text(text):
	functions = [lambda x: remove_nonletters(x, ' '), lambda x: replace_white_spaces(x, ' '), lambda x: x.lower().strip()]
	return sreduce(functions, text)

def to_normal_lower(word):
	return strip_accents(word.lower().strip())

def normalizePDF(text):
	remove = [' ˇ´ ',
			' ˚ ', 
			' ´', 
			' ˚', 
			' ˇ ', 
			' ˇ']
	
	for rem in remove:
		text = text.replace(rem, '')
	text = text.replace('ı', 'i')
	text = text.replace('t’', 't')
	
	return text

def normalizeWord(word, lang):
	word = strip_accents(createStem(word, lang))
	word = word.lower()
	return word

# source: http://effbot.org/zone/re-sub.htm#unescape-html
def unescapeHTMLEntities(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(html.entities.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)	

# source: http://effbot.org/zone/re-sub.htm#strip-html
def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import html.entities
            entity = html.entities.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return chr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return entity 
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	