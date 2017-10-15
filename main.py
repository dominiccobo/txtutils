import math
import os
import re
import time
from os.path import basename, dirname
from OrderedDefaultList import OrderedDefaultdict

'''
    DISCLAIMER: This is a short program I wrote late at night as I wanted to get back into Python again, 
    and as I couldn't sleep I thought it would be a good idea.
    It is not as clean as a distributable tool, but is still in working condition and may be updated in 
    the future.
'''

# TODO: (1) Convert into Flask based application


def main():
    """
        Initial entry method for the program
    :return: Does not return any method
    """
    print('Text analysis tool initiated: ')
    file_to_open = select_file()
    analyse_file(file_to_open)


def select_file():
    """
        Displays generic prompt for file selection. Also performs file existence checking, ensuring
        non-existent files aren't opened.

    :return: pointer to the file opened if it is opened.
    """
    file_selected = False
    file = ''

    while not file_selected:
        file_directory = input('Please input a file directory: ')
        file_name = input('Please input a text document (.txt) filename: ')

        file_path = file_directory + file_name + '.txt'
        if os.path.exists(file_path):
            file_selected = True
            file = open(file_path, 'r')
        else:
            print('Invalid file specified\n')

    return file


def analyse_file(file):
    """
        Calls on respective methods then performs relative analysis on files, measuring the performance.
    :param file: file pointer referencing file that is to be analysed.
    :return: Does not return any value.
    """
    start = int(round(time.time() * 1000))
    data = file.read()

    lines = len(data.splitlines())
    words = len(data.split())
    characters = len(data)
    duplicates = count_word_instances(data.lower())

    end = int(round(time.time() * 1000))

    string_to_return = 'Dom\'s cheesy python file analysis tool\nmore tools @ dominiccobo.com'
    string_to_return += '\n\nAnalysis Completed for file {}'.format(file.name)
    string_to_return += '\nPerformance stats for analysis: completion took ~{}ms'.format(end-start)
    string_to_return += '\nLines counted: {}'.format(lines)
    string_to_return += '\nWords counted: {}'.format(words)
    string_to_return += '\nCharacters counted: {}'.format(characters)
    string_to_return += '\nWord occurrence count:'

    for key, value in duplicates.items():
        string_to_return += '\n\t{}: {}'.format(key, value)

    string_to_return += '\n\nOriginal data:\n\n{}'.format(data)

    file.close()

    # create a statistical file
    log = open('{}/{}_analysis.txt'.format(dirname(file.name), basename(file.name)), 'w+')
    log.write(string_to_return)
    log.close()

    print('Analysis completed. Output written to same directory.')


def merge_sort_divide(list_to_divide):
    """
        Recursively halves a list until it is formed of single elements.
    :param list_to_divide: Data string to recursively halve.
    :return: Halved list.
    """
    if len(list_to_divide) < 2:
        return list_to_divide

    mid_point = math.floor(len(list_to_divide) / 2)

    return sort_and_merge(merge_sort_divide(list_to_divide[:mid_point]), merge_sort_divide(list_to_divide[mid_point:]))


def sort_and_merge(data_set_left, data_set_right):
    """
        Applies remainder of top-down approach from the merge sort algorithm, returning sorted lists.
    :param data_set_left: Left hand side of list to sort and merge
    :param data_set_right: Right hand side of list to sort and merge
    :return: Merged and sorted list
    """
    sorted_result = []
    l_pos = r_pos = 0
    while l_pos < len(data_set_left) and r_pos < len(data_set_right):
        if data_set_left[l_pos] < data_set_right[r_pos]:
            sorted_result.append(data_set_left[l_pos])
            l_pos += 1
        else:
            sorted_result.append(data_set_right[r_pos])
            r_pos += 1

    sorted_result += data_set_left[l_pos:]
    sorted_result += data_set_right[r_pos:]
    return sorted_result


def count_word_instances(data_string):
    """
        Applies analysis of words in file, reduces time vastly by merge sorting, before comparing for occurrences.
    :param data_string: data string to count instances of words in
    :return: the dictionary containing it
    """
    # Pass the string, sorted into a list into the merge sort algorithm
    sorted_data = merge_sort_divide(re.sub("[^\w]", " ", data_string).split())
    dict_occurrences = OrderedDefaultdict(int)

    for i, word in enumerate(sorted_data):
        dict_occurrences[word] += 1

    return dict_occurrences


if __name__ == '__main__':
    main()
