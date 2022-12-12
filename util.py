from emoji import UNICODE_EMOJI
import re

def load_embedding_model():
    """ Load Word2Vec Vectors
        Return:
            wv_from_bin: All the embeddings
    """
    import gensim.downloader as api
    wv_from_bin = api.load("word2vec-google-news-300")

    #print("Loaded vocab size %i" % len(wv_from_bin.vocab.keys()))
    return wv_from_bin
wv_from_bin = load_embedding_model()

def is_year(word):
    if len(word)==4 and word.isnumeric() and int(word)>1500 and int(word)<2050:
        return True
    else:
        return False
    
def is_dim(word):
    markings = ['x','X']

    
    
    for marking in markings:
        parts = word.split(marking)
        switch = True
        if len(parts)<2:
            switch = False
        else:    
            for i in parts:
                if not i.isnumeric() and i != '':
                    switch = False
        if switch == True:
        
            return True
    return False

def is_size(word):
    if word[-2:] == 'cm' or word[-2:] == 'mm' :
        if word[:-2].isnumeric():
            return True
        else:
            return False
        
    if word[-1:] == 'm' or  word[-1:] == 'l':
        if word[:-1].isnumeric():
            return True
        else:
            return False
        
def is_frac(word):
    if '/' in word:
        parts = word.split('/')
        remain = ''.join(parts)
        if remain.isnumeric():
            return True
    else:
        return False
    
def is_des(word):
    if 'e' in word or "nan" in word:
        return False
    try:
        float(word)
        return True
    except:
        return False
def is_bag(word):
    if word[:3]=='bag' or word[-3:] == 'bag':
        return True
    return False        
        
def is_int(word):
    if ',' in word:
        word = list(word)
        word.remove(',')
    if ''.join(word).isnumeric():
        return True
    else:
        return False
    
def is_new(word):
    if word == 'nwt':
        return True
    else:
        return False
def title_case(word):
    word = list(word)
    word[0] = word[0].upper()
    word = ''.join(word )
    return word
def is_emoji(word):
    return word in UNICODE_EMOJI['en']

def is_hash(word):
    if word[0]=='#':
        return True
    else:
        return False
def is_gold(word):
    if len(word)==3 and word[-1] == 'k' and word[:2].isnumeric():
        return True
    else:
        return False
def is_2way(word):
    if word == "2way":
        return True
    else:
        return False
    
def is_era(word):
    if len(word) == 3 and word[-1] =='s' and word[:2] in ['50s','60s','70s','80s', '90s','00s']:
        return True
    else:
        return False
def to_alpha(word):
    translator={'â':'a','Â':'A','ä':'a','Ä':'A','à':'a','À':'A',
                'é':'e','É':'E',
                'ö':'o', 'Ö':'O',
                'ü': 'u','Ü':'U'}
    out = []
    for i in word:
        if i in translator:
            out.append(translator[i])
        else:
            out.append(i)
    return ''.join(out)

def clean_anc(word):
    if '.' in word:
        if word[-1]=='.':
            word = word[:-1] 
        parts = word.split('.')
        switch = True
        for i in range(len(parts)):
            if len(parts[i]) != 1:
                switch = False
        if switch:
            return 'acronym'
        if parts[-1] in wv_from_bin:
            return parts[-1]
        # if  parts[-1].isnumeric():
        #     return 'number'
        elif len(parts[-1]) != 0 and title_case(parts[-1]) in wv_from_bin:
            return title_case(parts[-1])
        else: 
            return word
    else:
        return word
    
    
def remove_sym(word):
    symbols = "@#$%^&*/\|\_}{[]~`-=><￡、',.?!():;"
    symbols += '"'
    out = []
    for i in word:
        if i in symbols:
            continue
        else:
            out.append(i)
    return ''.join(out)
def is_season(word):
    if word in ["summer","spring","autumn","winter","fall"]:
        return True
def vocab_clean(original, second_pass = False):
    original = to_alpha(original)
    i = original.lower()
    if is_emoji(i):
        return 'emoji'
    if len(i)== 1 and i.isalpha() and i != 'a':
        return 'LETTER'
    if len(i) == 1 and i.isnumeric():
        return 'digit'
    elif is_new(i):
        return 'New'
    elif is_gold(i):
        return 'gold'
    elif is_era(i):
        return 'era'
    elif is_year(i):
        return 'year'
    elif is_dim(i):
        return "dimension"
    elif is_size(i):
        return "size"
    elif is_season(i):
        return 'Season'
    
    elif is_frac(i):
        return 'fractional'
    elif is_int(i):
        return 'integer'
    
    elif is_2way(i):
        return 'direction'
    elif i in "',.?!():;" or i in '"':
        return 'punctuation'
    elif i in "@#$%^&*/\|\_}{[]~`-=><￡、+ｘ":
        return 'symbol'
    elif i.isnumeric():
        word = 'integer'
        return word
    elif is_des(i):
        return 'decimal'
    elif i == "'s":
        word = 's'
        return word
    for sym in '-&+ｘ':
        if sym in i:
            
            parts = i.split(sym)
            if is_int(parts[-1]):
                return 'integer'
            elif is_era(parts[-1]):
                return 'era'
            elif is_2way(parts[-1]):
                return 'direction'
            elif is_year(parts[-1]):
                return 'year'
            elif is_dim(parts[-1]):
                return "dimension"
            elif is_size(parts[-1]):
                return "size"
            elif is_frac(parts[-1]):
                return "fraction"
            elif is_des(parts[-1]):
                return 'decimal'
            elif is_new(parts[-1]):
                return 'New'
            elif is_season(i):
                return 'Season'
            
            elif any(chr.isalpha() for chr in parts[-1]) and any(chr.isdigit() for chr in parts[-1]):
                word = "model"
                return word
            
            elif parts[-1] not in wv_from_bin:
                
                total_len = 0 
                for i in parts:
                    total_len+=len(i)
                if total_len == 0 :
                    return "symbols"
                if len(parts[-1]) ==0:
                    parts[-1] = parts[0]
                    
                
                parts[-1] = title_case(parts[-1])
                
                if parts[-1] in wv_from_bin:
                    return parts[-1]
                else: 
                    
                    return "UNK"
            else:
                return parts[-1]
                
            
    if any(chr.isalpha() for chr in i) and any(chr.isdigit() for chr in i):
        word = "model"

        return word

                   
    elif i not in wv_from_bin:
        
        i = title_case(i)
        if i in wv_from_bin:
            return i 
        else:
            if is_hash(i):
                return 'Hashtag'
            i = clean_anc(i)
            
            if i in wv_from_bin:
                return i 
            
            if not second_pass:
                return vocab_clean(remove_sym(original),second_pass=True)
            
            else:
                parts = re.findall('[A-Z][^A-Z]*', original)
                if len(parts)==2 and parts[1] in wv_from_bin:
                    return parts[1]
                switch = True
                for letter in original:
                    if not letter.isupper():
                        switch = False
                if switch:
                    
                    return "NAME"
                if original[0].isupper():
                    switch = True
                    for letter in original[1:]:
                        if letter.isupper():
                            switch = False
                if switch:
                    
                    return "Name"
                if is_bag(i):
                    return 'bag'
                # print(original)
                return "UNK"

    else:
        
        return i