
import itertools
import json

from nltk import word_tokenize
import en_core_web_sm
from nltk.tag import StanfordNERTagger
from nltk.tag import SennaNERTagger
import os
import re
from nltk.corpus import stopwords

#from mysite.myapi.TextMining.ParagraphExtraction import structure_text
#from mysite.myapi.TextMining.TextProcessing import remove_punctuation, remove_stop_words
from .ParagraphExtraction import structure_text
from .TextProcessing import remove_punctuation, remove_stop_words


def check_part_group(text):
    # part group should not contain punctuation
    punctuations = '!()-[]{};:\,<>./?@#$%^&*_~€™'
    for punctuation in punctuations:
        if punctuation in text:
            return False

    # part group should not be a stop word
    stopwords = {' and ', ' or '}
    for word in stopwords:
        if word in text.lower() or word.strip() == text.lower():
            return False
    return True


def group_locations(text):
    # text=remove_stop_words(text)
    # text=remove_punctuation(text)
    tokenized_text = text.split(' ')

    tokenized_text = list(tokenized_text)

    tokenized_text = list(filter(lambda a: a != "", tokenized_text))
    tokenized_text = list(filter(lambda a: len(a) > 1, tokenized_text))
    appended = 0

    locations = []
    count = 0
    spplited_token = False
    max = len(tokenized_text) - 1
    for i in range(1, max):
        if i > max:
            break
        if len(tokenized_text[i]) > 1:
            spplited_token = False
            token = tokenized_text[i]

            #if "Lake" in token:
                #print("stop")

            #if 'Theatre' in token:
             #   print("stop")
            if appended == 0:
                prev_word = tokenized_text[i - 1]
                count = 0

            newLineCondPrevWord = prev_word[len(prev_word) - 1] == '\n' or '\n' not in prev_word
            if '\n' in token:  # and (appended == 1 or token[len(token) - 1] == '\n'):
                token = token.split('\n')[0]
                spplited_token = True
            if '\n' in prev_word and appended == 0 and len(prev_word.split('\n')) > 1:
                if len(prev_word.split('\n')[prev_word.count('\n')]) > 1:
                    prev_word = prev_word.split('\n')[prev_word.count('\n')]
                    newLineCondPrevWord = True

            if len(token) > 1:
                cond1 = prev_word[0].isupper() and check_part_group(prev_word) and token[0].isupper() and not \
                token[1].isupper() and newLineCondPrevWord and '\n' not in token
                cond2 = prev_word[0].isupper() and check_part_group(prev_word) and tokenized_text[i + 1][
                0].isupper() and not \
                        tokenized_text[i + 1][1].isupper() and check_part_group(
                token) and newLineCondPrevWord and '\n' not in token

                if cond1 == True or cond2 == True:
                    count = count + 1

                    token = prev_word + " " + token

                    appended = 1
                    if spplited_token == True:
                        appended = 0
                        if not '\n' in token.strip('\n'):
                            locations.append(token)
                    if prev_word in locations:
                        locations.remove(prev_word)
                    prev_word = token
                else:
                    appended = 0

    # exclude_tokens = []
    for token in locations:
        locations[locations.index(token)] = remove_punctuation(token.strip('\n'))

    # for token in exclude_tokens:
    #   locations.remove(token)
    return locations


# f= open(r"C:\Users\Clara2\Desktop\Licenta\TestBERT\TestActivities\zagreb1.txt","r")
# group_locations((f.read()))

def match_locations(classified_text, tokenized_text):
    locations = []
    for word in classified_text:

        if word[1] == 'LOCATION' or word[1] == 'B-LOC' or word[1] == 'I-LOC' or word[1] == 'GPE' or word[1] == 'LOC' or \
                word[1] == 'FAC':

            if len(word[0].split(' ')) > 1 and len(word[0].split("\n")) > 1:  # result of spacy
                word1 = word[0].split("\n")[0]
                word2 = word[0].split("\n")[1]
                locations.append((remove_punctuation(word1), word[1]))
                locations.append((remove_punctuation(word2), word[1]))
            else:
                match = [x for x in tokenized_text if word[0] in x]
                if len(match) > 0:
                    locations.append((remove_punctuation(match[0]), word[1]))
                else:
                    locations.append((remove_punctuation(word[0]), word[1]))

    locations = list(dict.fromkeys(locations))

    return locations


def check_tag_location(tag):
    return tag == 'LOCATION' or tag == 'FAC' or tag == 'GPE' or tag == 'FAC' or tag == 'B-LOC' or tag == 'I-LOC'

def union_tags(classified_text1, classified_text2, classified_text3, text_tag):
    # text_tag = dict()


    for text1 in classified_text1:

        if not remove_punctuation(text1[0]) in text_tag.keys():
            if len(classified_text2) > 0:
                matches2 = [text2 for text2 in classified_text2 if
                        remove_punctuation(text2[0]) == remove_punctuation(text1[0])]
            if len(classified_text3) > 0:
                matches3 = [text3 for text3 in classified_text3 if
                        remove_punctuation(text3[0]) == remove_punctuation(text1[0])]

            matches = list()
            for match in text1:
                tag = match
                if check_tag_location(tag):
                    tag = 'LOC'
                matches.append(tag)

            if len(classified_text2) > 0:
                for match in matches2:
                    tag = match[1]
                    if check_tag_location(tag):
                        tag = 'LOC'
                    matches.append(tag)

            if len(classified_text3) > 0:
                for match in matches3:
                    tag = match[1]
                    if check_tag_location(tag):
                        tag = 'LOC'
                    matches.append(tag)

            text_tag[remove_punctuation(text1[0])] = matches
            # print(text_tag[remove_punctuation(text1[0])])

    return text_tag


def check_enumerations(locations, enumerations):
    for i in range(len(locations)):
        for j in range(len(enumerations)):
            if locations[i][0] in enumerations[j]:
                enumeration = enumerations[j].replace(' and ', ', ')
                for enum in enumeration.split(','):
                    if enum not in locations:
                        locations.append(enum)
    return locations


def union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


def get_locations(locations):
    stop_words = set(stopwords.words('english'))

    new_locations = []
    locations = list(filter(lambda a: len(a[0]) > 1 and not a[0] == '', locations))

    for loc in locations:
        no = 0

        if type(loc) == tuple:
            splitted = loc[0].split(' ')

            if len(splitted) == 1 and not loc[0][0].isupper():
                no = 1
            var = loc[0]
            if splitted[0].lower() in stop_words:
                var = var.split(splitted[0] + ' ')
                if len(var) > 1:
                    var = var[1]
                else:
                    var = var[0]

            if no == 0:
                new_locations.append(var.strip())
        else:
            splitted = loc.split(' ')
            if len(splitted) == 1 and not loc[0].isupper():
                no = 1
            if splitted[0].lower() in stop_words:
                loc = loc.split(splitted[0] + ' ')[1]
            if no == 0:
                new_locations.append(loc.strip())
    return new_locations


def exclude_answers(locations):
    excluded_locations = []
    for i in range(0, len(locations)):
        loc1 = remove_stop_words(locations[i]).strip()
        for j in range(0, len(locations)):
            loc2 = remove_stop_words(locations[j]).strip()
            if not locations[j] in excluded_locations:
                if not loc1.find(loc2) == -1 and not i == j:
                    excluded_locations.append(locations[j])

    for ex in excluded_locations:
        if ex in locations:
            locations.remove(ex)

    return locations


def min_freq(text_freq, locations):
    freq_list = [0] * 100

    for freq in text_freq.values():
        freq_list[freq] += 1

    index_min = 0
    i = 0
    #print(freq_list)
    for freq in freq_list:
        if freq - sum(freq_list[i + 1:]) >= 1 and index_min == 0:
            if i == 1 and len(locations) == 10:
                index_min = i
            if not i == 1:
                index_min = i

        i = i + 1

    return index_min -1


def calculate_freq(locations, text, destination):
    loc_freq = dict()
    for loc in locations:
        loc = remove_stop_words(loc).strip()
        words = loc.split(' ')
        if len(words) > 1:
            max = 0
            for word in words:
                if word not in destination:
                    freq = text.count(word)
                    if freq > max:
                        max = freq

            loc_freq[loc] = int(max)
        else:
            if loc not in destination:
                freq = text.count(loc)
                loc_freq[loc] = freq

    freq_list = [0] * 100

    freq_enitity = dict()
    for entity in loc_freq.keys():
        words = entity.split(' ')
        if len(words) > 1:
            for word in words:
                if len(word) > 1:
                    if word[0].isupper():
                        if word not in freq_enitity.keys():
                            freq_enitity[word] = text.count(word)
        elif entity[0].isupper():
            if entity not in freq_enitity.keys():
                freq_enitity[entity] = text.count(entity)

    for freq in freq_enitity.values():
        freq_list[freq] += 1

    index_min = 0
    i = 0
    for freq in freq_list:
        i = i + 1
        if freq - sum(freq_list[freq_list.index(freq) + 1:]) and index_min == 0 >= 1:
            index_min = freq_list.index(freq)

    return loc_freq, index_min


def calculate_score(text_freq, text_tag, enumerations, destination, titles):
    text_score = dict()
    for location in text_freq.keys():

        if location in titles:
            score = 1;
        else:
          if len(location.split(' ')) > 1:
            tags = list()
            for word in location.split(' '):
                if word not in destination:
                    added = 0

                    word = remove_punctuation(word)
                    if word in text_tag.keys():
                        score_other = text_tag[word].count('O') + text_tag[word].count('B-MISC') + text_tag[word].count(
                            'I-MISC')
                        score_other = score_other / (len(text_tag[word]) - 1)
                        if not score_other > 0.5:
                            tags.append(text_tag[word])
                            added += 1
            tags = [j for i in tags for j in i]

            if len(tags) > 0:
                score = str(tags).count('LOC') / (len(tags) - added)
            else:
                score = 0
          else:
            if location not in destination:
                score = text_tag[location].count('LOC') / (len(text_tag[location]) - 1)

        text_score[location] = score

    enum_score = dict()
    for location in text_score.keys():
        if location not in destination:
            for enum in enumerations:
                if remove_punctuation(remove_stop_words(location)) in remove_punctuation(remove_stop_words(enum)):
                    if enum not in enum_score.keys():
                        enum_score[enum] = text_score[location]
                    if enum_score[enum] < text_score[location]:
                        enum_score[enum] = text_score[location]

    for location in text_score.keys():
        for enum in enum_score.keys():
            if remove_punctuation(remove_stop_words(location)) in remove_punctuation(remove_stop_words(enum)):
                text_score[location] = enum_score[enum]

    return text_score


def union_classified_tags(classified_text_standford, classified_text_spacy, classified_text_senna):
    text_tag = dict()
    text_tag = union_tags(classified_text_standford, classified_text_spacy, classified_text_senna, text_tag)
    text_tag = union_tags(classified_text_spacy, classified_text_standford, classified_text_senna, text_tag)

    if len(classified_text_senna) > 0:
        text_tag = union_tags(classified_text_senna, classified_text_spacy, classified_text_standford, text_tag)

    return text_tag


def union_dicts(*dicts):
    return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))


def union_text_freq(text_freq):
    new_text_freq = dict()
    for elem in text_freq:
        for key in elem.keys():
            if key not in new_text_freq.keys():
                new_text_freq[key] = int(elem[key])
            else:
                new_text_freq[key] += int(elem[key])
    return new_text_freq


def union_text_tag(text_tag):
    new_text_tag = dict()
    for elem in text_tag:
        for key in elem.keys():
            if key not in new_text_tag.keys():
                new_text_tag[key] = list(elem[key])
            else:
                new_text_tag[key].extend(list(elem[key])[1:])
    return new_text_tag


def filter_answers(text_freq, text_tag, enumerations, destination, titles):
    text_score = calculate_score(text_freq, text_tag, enumerations, destination, titles)

    match_score = [loc for loc in text_score.keys() if text_score[remove_stop_words(loc).strip()] >= 0.5]
    #print(match_score)
    min = min_freq(text_freq, match_score)
    #print(min)
    filtered_locations = [loc for loc in match_score if text_freq[remove_stop_words(loc).strip()] > min or (min == 1 and text_freq[remove_stop_words(loc).strip()] == min)]


    for location in text_score.keys():
        for enum in enumerations:
            if remove_punctuation(remove_stop_words(location)) in remove_punctuation(remove_stop_words(enum)):
                if location in filtered_locations:
                    filtered_locations.remove(location)
                # if enum not in filtered_locations:
                # filtered_locations.append(enum)
    filtered_locations = exclude_answers(filtered_locations)
    return filtered_locations




def union_answers(locations_senna, locations_standford, locations_spacy):
    if len(locations_senna) > 0:
        locations_senna = get_locations(locations_senna)
    if len(locations_standford)> 0:
        locations_standford = get_locations(locations_standford)
    if len(locations_spacy) > 0:
        locations_spacy = get_locations(locations_spacy)

    final_list = union(locations_spacy, locations_standford)
    if len(locations_senna) > 0:
        final_list = union(final_list, locations_senna)
    final_list = exclude_answers(final_list)

    return final_list


def standford_NER(text):
    java_path = "C:\\Program Files\\Java\\jdk1.8.0_231\\bin\java.exe"
    os.environ['JAVAHOME'] = java_path
    st = StanfordNERTagger(
        'C:\\Users\\Clara2\\Downloads\\stanford-ner-2018-10-16\\classifiers\\english.all.3class.distsim.crf.ser.gz',
        'C:\\Users\\Clara2\\Downloads\\stanford-ner-2018-10-16\\stanford-ner.jar',
        encoding='utf-8')
    classified_text = st.tag(word_tokenize(text))
    return classified_text


def spacy_en_NER(text):
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    locations = []
    for X in doc.ents:
        if '\n' in X.text:
            for word in X.text.split('\n'):
                locations.append((remove_punctuation(word), X.label_))
        else:
            locations.append((remove_punctuation(X.text), X.label_))
    return locations


def senna_NER(text):
    nertagger = SennaNERTagger('C:\\Users\\Clara2\\Downloads\\senna-v3.0\\senna-v3.0\\senna')
    text = text.split('\n')

    list = []
    for sentance in text:
        sentance = sentance.split()
        list.append(nertagger.tag(sentance))
    locations = [j for i in list for j in i]
    return locations




def filter_enums(enumerations, destination):
    excluded_enums = []
    for enum in enumerations:
        if enum.count(',') < 2 and 'and' not in enum:
            excluded_enums.append(enum)

        match = [x for x in destination.split(' ') if
                 x + "," in enum or x + " and" in enum or "and " + x in enum or ", " + x in enum]
        if len(match) > 0:
            excluded_enums.append(enum)

    for enum in excluded_enums:
        if enum in enumerations:
            enumerations.remove(enum)
    return enumerations


def get_activities(text, destination):
    f = open(r"C:\Users\Clara2\Desktop\Licenta\TestBERT\TestNERActivities\Where To Find Tutankhamun Treasures.txt", "r")
    text = f.read()

    text = text.replace(r"\\n", "\n")
    text = text.replace(r"\n", "\n")

    #the titles and sub-titles may contain important locations
    structured_text = structure_text(text)

    text = text.replace('.', '.\n')

    #elements from an enumeration should have the same tag
    enumerations = [x.group() for x in re.finditer(
        r'(([A-Z-][a-z-]+( ([a-z]+\s)*[A-Z-][a-z-]+)*, )+[A-Z-][a-z-]+ ([A-Z-][a-z-]+)*(and [A-Z-][a-z-]+ *(([a-z]+ )*[A-Z-][a-z-]+)*)*)',
        text)]
    enumerations = filter_enums(enumerations, destination)

    tokenized_text = group_locations(text)

    if isinstance(structured_text, dict):
        tokenized_text.extend(structured_text.keys())
    tokenized_text = list(set(tokenized_text))

    ###---------- Senna NER --------------------###
    #classified_text_senna = senna_NER(text)
    #locations_senna = match_locations(classified_text_senna, tokenized_text)
    #locations_senna = check_enumerations(locations_senna, enumerations)

    classified_text_senna = []
    locations_senna= []
    ###---------- Senna NER --------------------###

    ###----------Spacy NER ---------------------###
    classified_text_spacy = spacy_en_NER(text)
    locations_spacy = match_locations(classified_text_spacy, tokenized_text)
    locations_spacy = check_enumerations(locations_spacy, enumerations)

    #locations_spacy = []
    #classified_text_spacy = []
    ###----------Spacy NER ---------------------###

    ###---------Standford NER-------------------###
    classified_text_standford = standford_NER(text)
    locations_standford = match_locations(classified_text_standford, tokenized_text)
    locations_standford = check_enumerations(locations_standford, enumerations)

    #locations_standford=[]
    #classified_text_standford=[]
    ###---------Standford NER-------------------###

    final_list = union_answers(locations_senna, locations_standford, locations_spacy)

    text = remove_punctuation(text)
    text = text.replace('\n', '')
    text = text.split(' ')

    text_freq, min = calculate_freq(final_list, text, destination)
    text_tag = union_classified_tags(classified_text_standford, classified_text_spacy, classified_text_senna)

    result = dict()
    result['text_tag'] = text_tag
    result['text_freq'] = text_freq
    result['enumeratio'] = enumerations
    result['location'] = final_list
    if isinstance(structured_text, dict):
        result['titles'] = list(structured_text.keys())
    else: result['titles'] =[]

    return result

get_activities("", "")

def get_final_result(result_blogs):

    jdata = json.loads(eval(result_blogs))

    destination = jdata[len(jdata) - 1]["destination"]

    locations = []
    text_freq = []
    text_tag = []
    enumerations = []
    titles = []
    for result in jdata:
        if len(result.keys()) > 1:
            locations.append(result["location"])
            text_freq.append(result["text_freq"])
            text_tag.append(result["text_tag"])
            enumerations.append(result["enumeratio"])
            titles.append(result['titles'])

    locations = [j for i in locations for j in i]
    locations = list(set(locations))
    locations = exclude_answers(locations)

    enumerations = [j for i in enumerations for j in i]
    enumerations = list(set(enumerations))
    enumerations = exclude_answers(enumerations)

    titles = [j for i in titles for j in i]
    titles = list(set(titles))
    titles = exclude_answers(titles)

    text_freq = union_text_freq(text_freq)
    text_tag = union_text_tag(text_tag)

    # f.write(str(locations))
    # f.write(str(text_tag))
    # f.write(str(text_freq))
    # f.write(str(enumerations))
    # f.write(str(min))

    return filter_answers(text_freq, text_tag, enumerations, destination,titles)


