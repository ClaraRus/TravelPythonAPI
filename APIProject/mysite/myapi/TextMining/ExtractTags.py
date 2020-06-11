import heapq
import string
from operator import itemgetter

import nltk
import numpy
import spacy
from nltk.corpus import stopwords
from rake_nltk import Rake

from .ParagraphExtraction import structure_text
from .TextProcessing import get_preprocessed_text, remove_punctuation, frequency, \
    lemantized_form, remove_useless_words


def filter_text(dictionary, label):
    filteredText = []
    for key in dictionary.keys():
        if label in dictionary[key]:
            filteredText.append(key)

    return filteredText


def filter_keyword(lines, keyword):
    interested_lines = []
    for line in lines:
        interested_lines.append(line)

    return interested_lines


def common_word(line1, line2):
    print(line1)
    print(line2)

    for wordL1 in line1.split(' '):
        for wordL2 in line2.split(' '):
            if wordL1 == wordL2:
                print(wordL1)
                return wordL1
    return ''


def coommon_word_group(keys, line):
    for key in keys:
        for word in line.split(' '):
            if key == word:
                return key
    return ""


def group_lines(lines):
    groups = dict()
    groups["no_group"] = []
    i = 0
    was_added = False
    for i in range(len(lines) - 2):
        for j in range(i + 1, len(lines) - 1):

            common_group = coommon_word_group(groups.keys(), lines[i])
            if not common_group == "":
                groups[common_group].append(lines[i])
                was_added = True
                break

            word = common_word(lines[i], lines[j])
            if not word == '':
                was_added = True
                if word in groups.keys():
                    groups[word].append(lines[i])
                    break;
                else:
                    groups[word] = []
                    groups[word].append(lines[i])
                    break;

        if not was_added:
            groups["no_group"].append(lines[i])
        was_added = False

    return groups


def get_tags_from(lines):
    groups = group_lines(lines)
    groups = remove_useless_tags(groups)

    tags = list(groups.keys())
    tags.remove('no_group')
    tags += create_tags_from(groups['no_group'])

    for tag in tags:
        if len(tag) < 4:
            tags.remove(tag)

    return tags


def create_tags_from(no_group):
    nouns = []
    tags = []
    for phrase in no_group:
        pos_tag = nltk.pos_tag(nltk.word_tokenize(phrase))
        nouns = nouns + list(filter(lambda tag: tag[1] == 'NN' and len(tag[0]) > 2, pos_tag))

    for noun in nouns:
        if not noun[0] in tags:
            tags.append(noun[0])

    return tags


def remove_useless_tags(groups):
    useless_keys = []
    for key in groups.keys():
        if not key == 'no_group':
            pos_tag = nltk.pos_tag(nltk.word_tokenize(key))
            if not pos_tag[0][1] == 'NN' and len(pos_tag[0][0]) > 2:
                groups['no_group'] += groups[key]
                useless_keys.append(key)

    for useless_key in useless_keys:
        del groups[useless_key]

    return groups


def get_adj_freq(text):
    adj_freq = dict()
    nlp = spacy.load("en_core_web_sm")
    text = " ".join(text)
    doc = nlp(text)
    for token in doc:
        if "JJ" in token.tag_ and len(token.text) > 2:
            if not token.text in adj_freq.keys():
                adj_freq[token.text] = text.count(token.text)
    return adj_freq


def get_keywords_from(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["’", "‘", "“", "”"])
    r = Rake(stopwords=stop_words, punctuations=string.punctuation, min_length=3)
    a = r.extract_keywords_from_text(text)
    b = r.get_ranked_phrases()
    c = r.get_ranked_phrases_with_scores()

    return b


def get_tags(text_from_url):
    text = text_from_url.replace(r"\\n", "\n")
    text = text.replace(r"\n", "\n")

    structured_text = structure_text(text)
    # text = get_preprocessed_text(text_from_url)
    # ranked_keywords = get_keywords_from(text)
    # tags = get_tags_from(ranked_keywords)

    print(structured_text)

    text = get_preprocessed_text(text_from_url)

    adj_freq = get_adj_freq(text)
    most_adj_freq_words = heapq.nlargest(10, adj_freq.items(), key=itemgetter(1))

    text = remove_useless_words(text)
    text = [remove_punctuation(word) for word in text if len(word) > 1]
    frq_dict = frequency(text)
    most_freq_words = heapq.nlargest(3, frq_dict.items(), key=itemgetter(1))

    tags = []

    tags.extend([tuple[0].lower() for tuple in most_freq_words])
    tags.extend([tuple[0].lower() for tuple in most_adj_freq_words])

    if type(structured_text) is dict:
        structured_text = [lemantized_form(word.lower())[0] for word in structured_text.keys()]

    # for word in most_freq_words:
    #    doc = nlp(word[0].lower())
    #    if "NN" in doc[0].tag_:
    #        tags.append(word[0].lower())

    nlp = spacy.load("en_core_web_sm")

    title = structured_text[0]
    for key in structured_text:
        if not key == title:
            for word in key.split(' '):
                doc = nlp(word.lower())
                if len(doc) > 0:
                    if "NN" in doc[0].tag_ and len(word) > 2:
                        tags.append(word.lower())

    tags.extend([word for word in title.split(' ') if word not in stopwords.words("english")])

    tags = list(set(tags))
    return tags


f = open(r"C:\Users\Clara2\Desktop\Licenta\TestBERT\TagsNew.txt", "r")
get_tags(f.read())

# if __name__ == "__main__":
# text = "COVID-19 UPDATE: Dear traveler and reader, if your travel plans have been modified, canceled, etc - you should know that you may be able to request a refund - platforms like Airbnb have been pretty helpful, several airlines will allow you to get a refund if your flight is affected, hotels on booking.com may be refunded if you put it a request for free cancelation (it worked for some of my bookings). Good luck and stay safe out there! What A Broken Backpack is doing: I decided to cancel my travel plans and stay put. Since I do not have a home, my plan is to settle in Bangkok and see how this situation evolves. After our struggle to get out of the Philippines following travel restrictions - we decided to leave and go somewhere where we feel safe and at home - and - that’s Thailand. Unsure on what to do? Join our  Facebook group and discuss with long-term travelers. BE KIND!If you’re planning your trip to Jerusalem, you may be wondering how long you need and more importantly, what to do and see. Whether you’re heading to Jerusalem for religious reasons or not, you should know that there’s more to it than just religious sites. (I’m only saying this because I’m not a religious person). To help you make the most of your time there, here are my recommendations for your 3 days in Jerusalem.To help you understand how fascinating and complex Jerusalem is   I’ll start with a short history lesson.Jerusalem is located in the Middle East between the Mediterranean Sea and the Dead Sea. Jerusalem might be one of the oldest cities in the world but is also important for religious reasons. In fact, it’s considered holy in Judaism, Christianism as well as Islamism religions.Over the years, Israel and Palestine have been claiming Jerusalem. Even though this conflict isn’t resolved yet   you can still visit Jerusalem as a traveler.Wondering what to do in Jerusalem? Let’s start! Table of Contents How to Spend 3 Day in JerusalemVisit Jerusalem Day 1Visit Jerusalem Day 2Visit Jerusalem Day 3Recommended Restaurants in JerusalemCheese   WineMachneyuda RestaurantJacko StreetBetzavtaRecommended Accommodation in JerusalemBudget OptionJerusalem Tips   Before You GoHow to Spend 3 Day in Jerusalem If you only have 3 days to visit Jerusalem, it should be enough to cover the essentials. In fact, you might even have extra time to add some shopping time or a short day trip from Jerusalem. You might be able to squeeze some of these things in 2 days if you’re on a tight schedule. Visit Jerusalem Day 1 Explore the Old City of Jerusalem  The Old City of Jerusalem is a small neighborhood (4 km-wide) which is very interesting. The Old City is divided into four quarters: Armenian, Jewish, Christian and Muslim. That said, walking around the Old City is basically discovering different cultures, enjoying different smells and diving into a whole new world every time you turn the corner. You might be seeing people following Jesus’s path Via Dolorosa which is a Christian pilgrimage marked by 9 stations of the Cross.Personally, my favorite quarters are the Muslim and the Christian one as I really love their colorful markets and it feels like a lot more is going on around there. If you want to do some souvenir shopping, these are the spots!PSST. We explored Jerusalem with Matilda Dias, a certified tour guide, and she was excellent. You can contact her via email: matids at gmail.com. Tower of David  In the Armenian quarter of the Old City, you might be able to spot the Tower of David (as well as a museum). You can access the tower only if you’d like to enjoy the view. The lookout costs ILS 10 and is only open on weekdays. You’ll find a great view of the Old City   which is totally worth it. Western Wall    The Western Wall is also known as the Wailing Wall is known worldwide. Regardless of your religion, you can still come and leave your prayer (or your wish) between the bricks of the walls. When visiting, you’ll find out that the wall is divided for men and women and you’ll see people praying on chairs as well as while touching the wall.You might be interested to know that in busy times of the year, they will remove the prayers every three days and will bury them   which means your prayer will stay safe. Church of the Holy Sepulchre  While you’re around the Old City, I suggest you visit the Church of the Holy Sepulchre. If you aren’t that religious, you can still go inside (it’s free) and take a look at the Church   it’s beautiful even for those like me who aren’t religious.This church is very popular for Christians visiting from all around the world. It is known to be the place where Jesus was crucified as well as his tomb. Don’t be surprised   you’re going to see long queues of people waiting to touch the closest thing to Jesus.    Visit Jerusalem Day 2 Machane Yehuda Market Mahane Yehuda Market seems like any other markets in Israel   which is why you must visit this market during day time… and night time. Two times? Yeah   you read this right. What appears to be a normal market during the day is quite the opposite during the night. All stands become bars with different DJs and are quite popular amongst the younger generations. Mamilla Mall  Mamilla Mall is basically a shopping street for pedestrians located on Alrov Mamilla Avenue. You’ll find popular shops, cute caf s and some great views around there. Located not too far from the Old City (close to Jaffa Gate), you can always go back there if you feel like you didn’t have enough time the previous day. The First Station I discovered the First Station in 2018 during a previous trip to Jesuralem. I was surprised to find such a hype place with busy restaurants, cultural events as well as shops. If you want to experience something different, this would be my first pick when it comes to unusual things to do in Jerusalem. Seeing it at night time would also be a great option as it gets even prettier. Visit Jerusalem Day 3 Day 3 is a bit of a buffer day which means you might have arrived in Jerusalem on an evening, or perhaps you’re going to leave Jerusalem for your next destination. Either way, here are some great options to consider if you have more time in Jerusalem. Mount of Olives Walking the Mount of Olives will give you all the great views you could be seeking. As it’s slightly further (save the location here), most people can’t go unless they have more time around Jerusalem. Jaffa Street Walking around Jaffa Street also show you another beautiful side of Jerusalem. You can find shops, restaurants and trams which is also great for photos. Organize a Day Trip to the Dead Sea, Masada and Ein Gedi  If you feel like you’ve seen enough of Jerusalem, you could also organize a day trip just outside of Jerusalem. After all, I’m sure the Dead Sea is on your list. While you’re at it, why not seeing Masada and Ein Gedi too.Read more about the Dead Sea and about day trips to the Dead Sea, Masada and Ein Gedi here. Recommended Restaurants in Jerusalem Cheese   Wine  Cheese   Wine is a rooftop restaurant located at Notre Dame of Jerusalem. The food is delicious but it’s even more special, thanks to the view. (Save the location here.) Machneyuda Restaurant This might look a bit odd   but the chefs made (threw) our desserts directly on the table. Epic dessert experience! Machneyuda is one of the most famous restaurants in Jerusalem   in fact, you have to book a table in advance to save your spot! The menu is always changing depending on what the market offers on that day. The atmosphere is vibrant. (Save the location here.) Jacko Street Jacko Street is located in the same area as the previous one, which is super close to the famous market. It’s a bit more elegant and offers delicious meals. (Save the location here.) Betzavta Shabbat Dinner with Betzavta | Photo by Or Kaplan Want to experience an Israeli dinner experience? Book a dinner with Betzavta. I d recommend you to do it on a Friday for a traditional Shabbat family dinner. Recommended Accommodation in Jerusalem I’ve been to Jerusalem three times and here are my recommendations. These three hotels offer great views as well as very comfortable stays. They were all great! The only difference between them was the locations. Mamilla Hotel: Mamilla Hotel is closed to Mamilla Mall as well as the Old City (my favorite location-wise).Inbal Jerusalem Hotel: Inbal Jerusalem Hotel is located at a walkable distance from the First Station.Herbert Samuel: Herbert Samuel is located around Jaffa Street (downtown). Budget Option Abraham Hostel Jerusalem: Hostels are quite expensive in Israel   so that’s also the case in Jerusalem. Abraham is great for backpackers as it offers a fully-equipped kitchen as well as great activities. You should know that families and couples are also welcome at Abraham Hostels. Jerusalem Tips   Before You Go  You should know that Jerusalem is a bit more conservative than Tel Aviv depending on the neighborhood of course. That said, if you’re planning on visiting religious sites, you should cover your knees as well as shoulders. At the Western Wall, men will need a hat or they can grab a head covering.You should also know that Shabbat is happening from Friday evening (at sundown) until Saturday evening (at sundown). Don’t be surprised if many shops and restaurants are closed during this time   especially in Jerusalem. You might need to make sure to buy food at the grocery store and book yourself. (Or you could join a traditional Shabbat dinner with an Israeli family. By the way, Betzavta (see in the restaurant section above) organizes dinner every day, not only for Shabbat. I strongly recommend it!)Entering and leaving Israel is sometimes complicated   read more about what it’s like here.Planning your week in Israel? Check out my recommended itinerary here.   READ MORE ABOUT ISRAEL Best food in Israel Swimming in the Dead Sea What to do in Tel Aviv BEFORE YOU GO TO ISRAEL  Book your flight: If your flight isn t booked yet   check out the flights on Skyscanner or via Google Flights. My top saving tip is flexibility. If you re flexible, you should be able to find a cheaper flight. Book your accommodation: I always use Airbnb and Booking.com. If you d rather stay in a hostel, you should take a look at the options on Hostelworld. If you click on the Airbnb link and you don t have an account yet   you ll get a $30 discount on your first booking. Protect your cute face: Oh, you may want to protect your cute face with a travel medical insurance. I would suggest SafetyWing as they offer the best rates, especially for long-term travelers. Otherwise, you can also take a look at World Nomads. Pack the essentials: You can consult this list when it s time to pack your bag! Do not leave without a universal charger, a power bank and your passport!  Do you need a visa? If you aren t sure if you need a visa, it would be a smart idea to take a quick look before you go. You can use iVisa   it s super useful and easy to use. SUPPORT US Get your monthly (and funny) dose of adventures! Subscribe now! You may also want to follow us on Facebook.Disclaimer: This post may include affiliate links. If you click one of them, we may receive a cute commission at no extra cost to you.  Thanks to MediaCentral for inviting me to Israel. As always, all opinions are my own. Happy travels."
# f = open(r"C:\Users\Clara2\Desktop\Licenta\TestBERT\TagsNew.txt", "r")
# get_preprocessed_text(f.read())
