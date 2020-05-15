

def is_title(paragraph):

    count_punctuation = 0
    count_punctuation+=paragraph.count(".")
    count_punctuation+=paragraph.count("?")
    count_punctuation+=paragraph.count("!")

    if count_punctuation > 1:
        return False

    words = [word for word in paragraph.split(' ') if len(word)>0]
    count_upper_words = len([word for word in words if word[0].isupper()])
    if count_upper_words/len(paragraph.split(' ')) < 0.5:
        return False

    return True

def structure_text(text):
    text = text.split("\n")

    #print(text)
    structured_text = dict()

    title_before = ""
    for paragraph in text:
     if len(paragraph) > 0:
      if is_title(paragraph):
          structured_text[paragraph] = ""
          title_before=paragraph
      else: structured_text[title_before] = paragraph

    if len(structured_text.keys()) <= 1:
        return text
    else: return structured_text

def extract_sentances(structured_text, location):
    paragraphs = [paragraph for paragraph in structured_text.values() if location.lower() in paragraph.lower()]

    sentances = []
    for paragraph in paragraphs:
        for sentance in paragraph.split("."):
            if location.lower() in sentance.lower():
                sentances.append(sentance)

    return sentances

def extract_paragraph(text, location):

    text = text.replace(r"\\n","\n");
    text = text.replace(r"\n","\n");

    structured_text = structure_text(text)

    if  isinstance(structured_text, dict):
    #case 1: location is a subtitle
        for key in structured_text.keys():
            if location.lower() in key.lower():
                return structured_text[key]

    #case 2: extract sentances containing the location
    sentances = extract_sentances(structured_text, location)

    #case 3: extract asentances with pronoun transformation

    #result = dict()
    #result['sentances'] = sentances
    return ".".join(sentances)

#def combine_paragraphs(parapgraphs):
