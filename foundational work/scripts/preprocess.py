import json

with open('/content/stance_dataset.json') as f:
    data = json.load(f)

print(data[0])
target_txt = data[0]['target_text']
response_txt = data[0]['response_text']

print(target_txt)
print(response_txt)

import re
from collections import Counter

def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = Counter(words(open('/content/drive/MyDrive/ISB_NLP Task/words.txt').read()))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

viterbi_segment('votethemallout')

def replace_uppercase(string):
    # Convert the string to lowercase
    lowercase_string = string.lower()

    # Replace all uppercase characters with their lowercase counterparts
    for char in string:
        if char.isupper():
            lowercase_string = lowercase_string.replace(char, char.lower())

    return lowercase_string

print(replace_uppercase('VoteThemAllOut'))

# We want to process hashtags and URLs

def hashtag_proc(hashtag):
    return viterbi_segment(hashtag)[0]


def proc(string):
    final_string = ""
    punctuations = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    i = 0
    while i < len(string):
        #print(i)
        if string[i] == '#':
            hashtag = ""
            j = i+1
            #print("j:",j)
            while string[j]!=' ':
                hashtag+=string[j]
                j+=1
            hashtag = replace_uppercase(hashtag)
            hashtag = hashtag_proc(hashtag)
            for word in hashtag:
                final_string+=word
                final_string+=' '
            i = j
        elif string[i] in punctuations:
            i+=1
            continue
        else:
            final_string += string[i]
        i+=1

    final_string_1 = ''
    for word in final_string.split():
        if 'https' in word:
            continue
        else:
            final_string_1+=word
            final_string_1+=' '

    return final_string_1

print(proc(response_txt))



input_strings = []
labels = []

for i in range(len(data)):
    #print(i)
    #print(data[i])
    label = 0
    final_string = ""
    final_string += 'Interaction Type: '
    if data[i]['interaction_type'] == 'Quote':
        final_string += 'Quote, '
    elif data[i]['interaction_type'] == 'Reply':
        final_string += 'Reply, '

    final_string += 'Event: '
    if data[i]['event'] == 'Santa_Fe_Shooting':
        final_string += 'Santa Fe Shooting, '
    elif data[i]['event'] == 'General_Terms':
        final_string += 'General Terms, '
    elif data[i]['event'] == 'Student_Marches':
        final_string += 'Student Marches, '
    elif data[i]['event'] == 'Student_Marches':
        final_string += 'Student Marches, '
    elif data[i]['event'] == 'Iran_Deal':
        final_string += 'Iran Deal, '

    try:
        final_string += 'Target Text: '
        final_string += proc(data[i]['target_text'])
        final_string += ', '
    except:
        None

    try:
        final_string += 'Response Text: '
        final_string += proc(data[i]['response_text'])
    except:
        None

    input_strings.append(final_string)
   
    if data[i]['label'] == 'Explicit_Denial':
        label = 1
    elif data[i]['label'] == 'Implicit_Denial':
        label = 2
    elif data[i]['label'] == 'Implicit_Support':
        label = 3
    elif data[i]['label'] == 'Explicit_Support':
        label = 4
    elif data[i]['label'] == 'Queries':
        label = 5
    elif data[i]['label'] == 'Comment':
        label = 6

    labels.append(label)

for i in range(10):
    print(input_strings[i])

json_list = []

for i in range(len(labels)):
    new_dict = {}
    new_dict['prompt'] = input_strings[i]
    new_dict['completion'] = labels[i]
    json_list.append(new_dict)

for i in range(10):
    print(json_list[i])

json_string = json.dumps(json_list)

with open('stance_dataset_modified.json', 'w') as f:
    f.write(json_string)

import csv


fieldnames = json_list[0].keys()

with open('stance_dataset_modified.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for row in json_list:
        writer.writerow(row)


input_strings = []
labels = []

for i in range(len(data)):
    #print(i)
    #print(data[i])
    label = 0
    final_string = []
    if data[i]['interaction_type'] == 'Quote':
        final_string.append('Quote')
    elif data[i]['interaction_type'] == 'Reply':
        final_string.append('Reply')

    if data[i]['event'] == 'Santa_Fe_Shooting':
        final_string.append('Santa Fe Shooting')
    elif data[i]['event'] == 'General_Terms':
        final_string.append('General Terms')
    elif data[i]['event'] == 'Student_Marches':
        final_string.append('Student Marches')
    elif data[i]['event'] == 'Iran_Deal':
        final_string.append('Iran Deal')

    try:
        final_string.append(proc(data[i]['target_text']))
    except:
        None

    try:
        final_string.append(proc(data[i]['response_text']))
    except:
        None

    input_strings.append(final_string)
   
    if data[i]['label'] == 'Explicit_Denial':
        label = 1
    elif data[i]['label'] == 'Implicit_Denial':
        label = 2
    elif data[i]['label'] == 'Implicit_Support':
        label = 3
    elif data[i]['label'] == 'Explicit_Support':
        label = 4
    elif data[i]['label'] == 'Queries':
        label = 5
    elif data[i]['label'] == 'Comment':
        label = 6

    labels.append(label)

json_list = []

for i in range(len(labels)):
    new_dict = {}
    new_dict['interaction_type'] = input_strings[i][0]
    new_dict['event'] = input_strings[i][1]
    try:
        new_dict['target_text'] = input_strings[i][2]
    except:
        new_dict['target_text'] = ""
    try:
        new_dict['response_text'] = input_strings[i][3]
    except:
        new_dict['response_text'] = ""
    new_dict['label'] = labels[i]
    json_list.append(new_dict)

import csv


fieldnames = json_list[0].keys()

with open('stance_dataset_modified_1.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for row in json_list:
        writer.writerow(row)

