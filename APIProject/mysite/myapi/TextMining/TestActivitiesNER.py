import os
import re
import matplotlib.pyplot as plt
import numpy as np
from mysite.myapi.TextMining.ActivitiesNER import union_answers, standford_NER, match_locations, check_enumerations, \
    spacy_en_NER, senna_NER, group_locations, filter_enums, get_locations, exclude_answers







def get_results(out_path, test_path, path):
    out = open(out_path, 'r')
    gt = open(path + 'NamedEntity.txt', 'r')
    gt_text = gt.read()
    gt_text = gt_text.split('\n')
    out_text = out.read()

    found = 0
    list_out_text = out_text.split(")")
    for i in range(len(gt_text)):
        label = ""
        if i >= len(gt_text):
            break
        find = 0
        if gt_text[i].strip() in out_text:
            find = 1
            label = [word for word in list_out_text if gt_text[i].strip() in word or word in gt_text[i].strip()]

        gt_text[i] = gt_text[i] + " " + str(find) + " " + str(label)

    test_out = open(test_path, 'a')
    test_out.write(str(gt_text))

def get_activities_text_file(file_to_read, blogTitle):
  path = 'C:\\Users\\Clara2\\Desktop\\Licenta\TestBERT\\TestNERActivities\\' + blogTitle+'\\'
  if not os.path.exists(path):
    os.mkdir(path)
    file = open(file_to_read, 'r',encoding='utf-8')
    text = file.read()
    text = text.replace('.', '.\n')
    text = replace_non_eng_letters(text)

    enumerations = [x.group() for x in re.finditer(
        r'(([A-Z-][a-z-]+( ([a-z]+\s)*[A-Z-][a-z-]+)*, )+[A-Z-][a-z-]+ ([A-Z-][a-z-]+)*(and [A-Z-][a-z-]+ *(([a-z]+ )*[A-Z-][a-z-]+)*)*)',
        text)]
    enumerations = filter_enums(enumerations, "")
    #print("Enumerations")
    #print(enumerations)
    tokenized_text = group_locations(text)

    ###---------- Senna NER --------------------###
    classified_text_senna = senna_NER(text)
    locations_senna = match_locations(classified_text_senna, tokenized_text)
    locations_senna = check_enumerations(locations_senna, enumerations)

    locations_senna = get_locations(locations_senna)
    locations_senna = list(set(locations_senna))
    locations_senna = exclude_answers(locations_senna)

    out_path = path + 'out_entity_senna.txt'
    test_path = path + 'test_senna.txt'

    out = open(out_path, 'w')
    out.write(str(classified_text_senna))

    out = open(out_path, 'r')
    print(out.read())

    test = open(test_path, 'w')
    test.write(str(locations_senna))
    test.write("\n\nTOTAL:\n\n")
    test.write(str(len(locations_senna)))
    #get_results(out_path, test_path, path)
    ###---------- Senna NER --------------------###

    ###----------Spacy NER ---------------------###
    out_path = path + 'out_entity_spacy.txt'
    test_path = path + 'test_spacy.txt'

    classified_text_spacy = spacy_en_NER(text)
    locations_spacy = match_locations(classified_text_spacy, tokenized_text)
    locations_spacy = check_enumerations(locations_spacy, enumerations)

    locations_spacy = get_locations(locations_spacy)
    locations_spacy = list(set(locations_spacy))
    locations_spacy = exclude_answers(locations_spacy)

    out = open(out_path, 'w')
    out.write(str(classified_text_spacy))
    out = open(out_path, 'r')
    #print(out.read())

    test = open(test_path, 'w')
    test.write(str(locations_spacy))
    test.write("\n\nTOTAL:\n\n")
    test.write(str(len(locations_spacy)))

    #get_results(out_path, test_path, path)
    ###----------Spacy NER ---------------------###

    ###---------Standford NER-------------------###
    classified_text_standford = standford_NER(text)
    locations_standford = match_locations(classified_text_standford, tokenized_text)
    locations_standford = check_enumerations(locations_standford, enumerations)

    locations_standford = get_locations(locations_standford)
    locations_standford = list(set(locations_standford))
    locations_standford = exclude_answers(locations_standford)

    out_path = path + 'out_entity_standford.txt'
    test_path = path + 'test_standford.txt'

    out = open(out_path, 'w')
    out.write(str(classified_text_standford))

    out = open(out_path, 'r')
    #print(out.read())

    test = open(test_path, 'w')
    test.write(str(locations_standford))
    test.write("\n\nTOTAL:\n\n")
    test.write(str(len(locations_standford)))

    #get_results(out_path, test_path, path)
    ###---------Standford NER-------------------###

    result = open(path+ 'result_all.txt', 'w')

    main_list = set(locations_standford).union(locations_spacy)
    result.write(str(main_list) + "\n")
    result.write("Standford+Spacy: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = set(locations_standford).union(locations_senna)
    result.write(str(main_list) + "\n")
    result.write("Standford+Senna: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = set(locations_spacy).union(locations_senna)
    result.write(str(main_list) + "\n")
    result.write("Senna+Spacy: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = set(locations_spacy).union(locations_senna)
    main_list= main_list.union(locations_standford)
    result.write(str(main_list) + "\n")
    result.write("Senna+Spacy+Standford: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = np.setdiff1d(locations_standford, locations_spacy)
    result.write(str(main_list)+"\n")
    result.write("Standford-Spacy: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = np.setdiff1d(locations_spacy, locations_standford)
    result.write(str(main_list)+"\n")
    result.write("Spacy-Standford: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = np.setdiff1d(locations_spacy, locations_senna)
    result.write(str(main_list)+"\n")
    result.write("Spacy-Senna: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = np.setdiff1d(locations_senna, locations_spacy)
    result.write(str(main_list)+"\n")
    result.write("Senna-Spacy: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = np.setdiff1d(locations_standford, locations_senna)
    result.write(str(main_list)+"\n")
    result.write("Standford-Senna: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    main_list = np.setdiff1d(locations_senna, locations_standford)
    result.write(str(main_list)+"\n")
    result.write("Senna-Standford: ")
    result.write(str(len(main_list)))
    result.write("\n\n")

    print(union_answers(locations_senna, locations_standford, locations_spacy, text, classified_text_standford,
                        classified_text_spacy, classified_text_senna, enumerations))

#path = r'C:\Users\Clara2\Desktop\Licenta\TestBERT\TestNERActivities'
#for file in os.listdir(path):
#    get_activities_text_file(path+'\\'+file, file.split('.txt')[0])


def draw_result_chart(path):

    result = dict()
    result['spacy']=0
    result['senna']=0
    result['standford']=0

    #result = dict();
    #result['Spacy+Standford']=0
    #result['Senna+Spacy']=0
    #result['Standford+Senna']=0
    #result['All']=0


    for dir in os.listdir(path):
        if not '.txt' in dir:
            for file in os.listdir(path+dir):

                if 'result' in file and False:
                    test = open(path + dir + "\\" + file, 'r')
                    content = test.read()
                    content = content.split('\n')

                    for line in content:
                        if 'Standford+Spacy:' in line:
                            result['Spacy+Standford'] += int(line.split('Standford+Spacy:')[1].strip())

                        elif 'Standford+Senna:' in line:
                            result['Standford+Senna'] += int(line.split('Standford+Senna:')[1].strip())

                        elif 'Senna+Spacy:' in line:
                            result['Senna+Spacy'] += int(line.split('Senna+Spacy:')[1].strip())

                        elif 'Senna+Spacy+Standford:' in line:
                            result['All'] += int(line.split('Senna+Spacy+Standford:')[1].strip())

                if 'test' in file:
                    test = open(path+dir+"\\"+file, 'r')
                    content = test.read()
                    total_result = content.split('TOTAL:')[1].strip()
                    if 'spacy' in file:
                        result['spacy'] += int(total_result)
                    elif 'senna' in file:
                        result['senna'] += int(total_result)
                    elif 'standford' in file:
                        result['standford'] += int(total_result)

    # x-coordinates of left sides of bars
    left = [1, 2, 3]

    # heights of bars
    height = list()
    height.append(result['spacy']/76)
    height.append(result['senna']/76)
    height.append(result['standford']/76)


    # labels for bars
    tick_label = ['spacy', 'senna', 'standford']

    # x-coordinates of left sides of bars
    #left = [1, 2, 3, 4]

    # heights of bars
    #height = list()
    #height.append( result['Spacy+Standford']/76)
    #height.append( result['Senna+Spacy']/76)
    #height.append(result['Standford+Senna']/76)
    #height.append(result['All']/76)

    # labels for bars
    #tick_label = ['Spacy+Standford', 'Senna+Spacy', 'Standford+Senna', 'All']

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['black', 'orange'])

    # naming the x-axis
    plt.xlabel('x - axis')
    # naming the y-axis
    plt.ylabel('y - axis')
    # plot title
    plt.title('My bar chart!')

    # function to show the plot
    plt.show()

def draw_time_chart():
    # x-coordinates of left sides of bars
    left = [1, 2, 3, 4, 5]

    # heights of bars
    height = list()
    height.append(13)
    height.append(64)
    height.append(22)
    height.append(25)
    height.append(92)

    # labels for bars
    tick_label = ['Spacy', 'Senna', 'Standford', 'Standford+Spacy','All']

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['black', 'orange'])

    # naming the x-axis
    plt.xlabel('x - axis')
    # naming the y-axis
    plt.ylabel('seconds')
    # plot title
    plt.title('My bar chart!')

    # function to show the plot
    plt.show()

#draw_result_chart('C:\\Users\\Clara2\\Desktop\\Licenta\\TestBERT\\TestNERActivities\\')
#time per 10 blogs
draw_time_chart()

numer_of_blogs=76
