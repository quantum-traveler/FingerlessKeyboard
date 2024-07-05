from english_words import get_english_words_set
import random
web2lowerset = get_english_words_set(['web2'], lower=True)
webtestset = random.sample(list(web2lowerset), 10)

#1 - qaz
#2 = wsx
#3 = edc
#4 - rtfgvb
#5 = yhnjum
#6 = ik
#7 = ol
#8 - p

def wordmap(word):
    finger_word = ''
    for letter in word:
        if letter =='r' or letter =='t' or letter =='f' or letter =='g' or letter =='v' or letter =='b':
            finger_word += '4'
        elif letter =='y' or letter =='h' or letter =='n' or letter =='j' or letter =='u' or letter =='m':
            finger_word += '5'
        elif letter =='q' or letter =='a' or letter =='z':
            finger_word += '1'
        elif letter =='w' or letter =='s' or letter =='x':
            finger_word += '2'
        elif letter =='e' or letter =='d' or letter =='c':
            finger_word += '3'
        elif letter =='i' or letter =='k':
            finger_word += '6'
        elif letter =='o' or letter =='l':
            finger_word += '7'
        elif letter =='p':
            finger_word += '8'
        else:
            finger_word += '0'

    return finger_word

def make_wordmap_dict(set):
    wordmap_dict = {}
    for word in set:
        wordmap_dict[word] = wordmap(word)
    return wordmap_dict


#print(make_wordmap_dict(webtestset))


#flipping the key value pairs

def make_dict(set):
    flipped = {}
    ini_dict = make_wordmap_dict(set)
    for key, value in ini_dict.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)

    duplicates = {}
    for key, value in flipped.items():
        if len(value) > 10:
            duplicates[key] = value

    return duplicates


#associate each region with a finger-typing motion


#implement hand detection w Mediapipe + OpenCV



