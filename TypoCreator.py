import pandas as pd
import numpy as np
import string
import random

def case_variaties(word: str)->list[str]:
    'Change the capitalisation of the first two letters'
    case_list = []
    case_list.append([word.lower(), word])
    case_list.append([word.upper(), word])
    case_list.append([word[:1].upper()+word[1:], word])
    case_list.append([word[:2].upper()+word[2:], word])
    return case_list

def enter_signs(word: str)->list[str]:
    'add # and + at the end, because of fat fingers when hitting enter'
    enter_list = []
    enter_list.append([word+'#', word])
    enter_list.append([word+'+', word])
    return enter_list

def no_spaces(word: str)->str:
    'eliminate all spaces from word'
    return [word.replace(' ',''), word]

def swap_letter(word: str)->list[str]:
    'swap every letter of a word pairwise'
    swap_list = []
    for idx, letter in enumerate(word):
        swap_list.append([word[:idx] + word[idx+1] + word[idx]+word[idx+2:], word])
        if idx + 2 == len(word):
            break
    return swap_list

def double_letter(word: str)-> list[str]:
    'double every letter in the word'
    double_letter_list = []
    for idx, letter in enumerate(word):
        double_letter_list.append([word[:idx] + letter + word[idx:], word])
    return double_letter_list

def one_out(word: str)->list[str]:
    'Remove on every possible position one letter from the input word'
    one_out = []
    for idx in range(len(word)):
        one_out.append([word[:idx] + word[idx+1:], word])
    return one_out

neighbors = {
    'a': ['q', 'w', 's','y','<'], 
    'b': ['v',' ','g','h','n'],
    'c': ['x','d','f','v', ' '],
    'd': ['e', 'r', 'f','c','x','s'],
    'e': ['w','3','4','r','d','s'],
    'f': ['d','r','t','g','v','c'],
    'g': ['f','t','z','h','b','v'],
    'h': ['g','z','u','j','n','b'],
    'i': ['u','8','9','o','k','j'],
    'j': ['h','u','i','k','m','n'],
    'k': ['j','i','o','l',',','m'],
    'l': ['k','o','p','ö','.'],
    'm': ['n','j','k',',',' '],
    'n': ['b','h','j','m',' '],
    'o': ['i','9','0','p','l','k'],
    'p': ['o','0','ß','ü','ö','l'],
    'q': ['1','2','w','a'],
    'r': ['e','4','5','t','f','d'],
    's': ['a','w','e','d','x','y'],
    't': ['r','5','6','z','g','f'],
    'u': ['z','7','8','i','j','h'],
    'v': ['c','f','g','b',' '],
    'w': ['q','2','3','e','s','a'],
    'x': ['y','s','d','c',' '],
    'y': ['<','a','s','x'],
    'z': ['t','6','7','u','h','g'],
    '1': ['^','2','q','4'],
    '2': ['1','3','w','q','5'],
    '3': ['2','4','e','w','6'],
    '4': ['3','5','r','e','1','7'],
    '5': ['4','6','t','r','2','8'],
    '6': ['5','7','z','t','3','9','+'],
    '7': ['6','8','u','z','4'],
    '8': ['7','9','i','u','5','/'],
    '9': ['8','0','o','i','6','*','+'],
    '0': ['9','ß','p','o']
    }

def replace_with_neighbor(word: str, neighbors = neighbors)->list[str]:
    'replace every letter in the word with every possible neighbor on a german keyboard'
    neighbor_replaced_words = []
    for idx, letter in enumerate(word):
        for neighbor in neighbors.get(letter.lower(),letter):
            if letter.isupper():
                neighbor_replaced_words.append([word[:idx] + neighbor.upper() + word[idx+1:], word])
            else:
                neighbor_replaced_words.append([word[:idx] + neighbor + word[idx+1:], word])
    return neighbor_replaced_words

def b4_after_with_neighbor(word: str)->list[str]:
    'place before and after every letter in the word every possible neighbor on a german keyboard'
    neighbor_replaced_words = []
    for idx, letter in enumerate(word):
        for neighbor in neighbors.get(letter.lower(),letter):
            if letter.isupper():
                neighbor_replaced_words.append([word[:idx] + neighbor.upper() + word[idx:], word])
                neighbor_replaced_words.append([word[:idx+1] + neighbor.upper() + word[idx+1:], word])
            else:
                neighbor_replaced_words.append([word[:idx] + neighbor + word[idx:], word])
                neighbor_replaced_words.append([word[:idx+1] + neighbor + word[idx+1:], word])
    return neighbor_replaced_words


def add_noise(word: str)->list[str]:
    'add a random string with random length at the end of the word'
    noise_words = []
    for _ in range(6):
        noise_words.append([word+''.join([random.choice(string.ascii_letters) for i in range(random.randint(1,8))]), word])
    return noise_words

def main(word_list: list)->list[str]:
    varieties_list = []
    for word in word_list:
        varieties_list.append([[word, word]])
        varieties_list.append(case_variaties(word))
        varieties_list.append(enter_signs(word))
        if ' ' in word:
            varieties_list.append(no_spaces(word))
        varieties_list.append(swap_letter(word))
        varieties_list.append(double_letter(word))
        varieties_list.append(one_out(word))
        varieties_list.append(replace_with_neighbor(word))
        varieties_list.append(b4_after_with_neighbor(word))
        varieties_list.append(add_noise(word))
    return varieties_list

text = list(pd.read_csv('pokemon.csv',delimiter=';')['Pokemon'])
all_variations = main(text)

bootstrap_size = 1000
bootstrap = []
for i in range(bootstrap_size):
    variation = np.random.randint(1,len(all_variations))
    bootstrap.append(all_variations[variation][np.random.randint(0,len(all_variations[variation]))])

df = pd.DataFrame(bootstrap, columns=['word','cluster'])
df.to_csv('clustered_typos.csv')