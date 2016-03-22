'''
Created on Mar 22, 2016
Copyright (c) 2015-2016 Teodoro Montanaro

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
@author: tmontanaro
'''

from sys import argv
import os


def say(text, language='en-gb'):
    '''
    :param text: text that we want to <say>
    :param language: language of the specified text

    This method uses the voicerss service for text to speech:
    a) it save the generated audio into an mp3 file
    b) it plays the mp3 file using the system mplayer
    '''

    # prepare the command to fetch the mp3 file generated by voicerss service
    # we use the system wget command to download the generated mp3 file
    wget_line = 'wget -q -U Mozilla -O test.mp3 "http://api.voicerss.org/?key=372c6bee13824fad884ed65442e123bd&hl=' + language + '&src=' + text + '"'

    # fetch the mp3
    os.system(wget_line)

    # play it (system dependent)
    # parameters for mplayer (used to remove unwanted messages):
    #  -quiet
    #    Make console output less verbose; in particular, prevents the status line (i.e. A: 0.7 V: 0.6 A-V: 0.068 ...) from being displayed
    #  -nolirc
    #    Turns off LIRC support.
    #  -msglevel <all=<livello>:<modulo>=<livello>:...>
    #    Control verbosity directly for each module
    os.system("mplayer -quiet -nolirc -msglevel all=-1 test.mp3")


def read_2_tasks(tasks_list):
    '''
    :param tasks_list: list of existing tasks

    Make the computer <speak> the first 2 tasks in the list (the item should be sorted in alphabetic order)
    '''

    # check if the list is empty
    if (len(tasks_list) == 0):
        print "The list is empty"
    else:
        # sort the list
        sorted_list = sorted(tasks_list)
        number_of_iteration = 0
        # if we have less then 2 items in the list we read only the existing ones
        # otherwise we read only the first 2 items
        if (len(sorted_list) >= 2):
            number_of_iteration = 2
        else:
            number_of_iteration = len(sorted_list)
        element_count = 0
        while (element_count < number_of_iteration):
            say(sorted_list[element_count])
            element_count += 1


def new_task(tasks_list):
    '''
    :param tasks_list: list of existing tasks
    :return new list of tasks
    Add a new element to the given list
    '''

    # ask the user to insert the task she wants to add
    string = raw_input("Type the new task:\n>")

    # actually add the item to the list
    tasks_list.append(string)
    print "The new task was successfully added to the list"

    # return the modified list
    return tasks_list


def remove_task(tasks_list):
    '''
    :param tasks_list: list of existing tasks
    :return updated list of tasks

    Remove an element from the given list
    '''

    # ask the user to insert the task she wants to remove
    string = raw_input("Type the entire content of the task you want to delete:\n>")

    # check if the task is actually present in the list
    if (string in tasks_list):
        tasks_list.remove(string)
        print "The element was successfully deleted"
    else:
        print "The element you specified is not in the list!"

    # return the modified list
    return tasks_list


def remove_multiple_tasks(tasks_list):
    '''
    :param tasks_list: list of existing tasks
    :return updated list of tasks

    Remove all the elements that contain a provided string
    '''

    # create a list to store tasks we will remove at the end
    remove_list = []

    # ask for the substring
    substring = raw_input("Type the substring you want to use to remove all tasks that contain it:\n>")

    # mark tasks that contains the specified substring
    for single_task in tasks_list:
        # if the substring is contained in the task we save it in the remove_list
        if (substring in single_task):
            remove_list.append(single_task)
    if (len(remove_list) > 0):
        for task_to_remove in remove_list:
            if (task_to_remove in tasks_list):
                tasks_list.remove(task_to_remove)
                print "The element '" + task_to_remove + "' was successfully removed"
    else:
        print "We did not find any tasks to delete!"
    return tasks_list


def print_sorted_list(tasks_list):
    '''
    :param tasks_list: list of existing tasks

    Print the elements of the list, sorted in alphabetic order
    '''

    # check if the list is empty
    if (len(tasks_list) == 0):
        print "The list is empty"
    else:
        # we don't want to modify the real list of elements: we want only to print it after sorting
        # there are 2 possibilities:
        # a) using the sort method
        #   temp_tasks_list = tasks_list[:]
        #   temp_tasks_list.sort()
        #   print temp_tasks_list
        # b) using the sorted method (the sorted method return a new list)
        print sorted(tasks_list)


if __name__ == '__main__':
    # main program

    # initialize the task list
    tasks_list = []
    # set a variable to False: it will be used to re-execute the program multiple times
    ended = False

    # if the user did not insert a filename we start from an empty list
    filename = ""
    if (len(argv) > 1):
        filename = argv[1]
        try:
            # open the file
            txt = open(filename)

            # read the file: load each row in an element of the list without "/n"
            tasks_list = txt.read().splitlines()

            # close the file
            txt.close()

        except IOError:
            print("File not found! We will start with an empty list")

    # keep asking strings until the user types 4 (to exit)
    while not ended:

        # print the menu every time we finish to perform an operation
        print "Insert the number corresponding to the action you want to perform"
        print "1: insert a new task"
        print "2: remove a task (by typing all its content)"
        print "3: remove all the existing tasks that contain a provided string;"
        print "4: show all existing tasks sorted in alphabetic order"
        print "5: read the first 2 tasks"
        print "6: close the program"

        # get the action as input
        string = raw_input("Your choice:\n>")

        # check if the inserted string is actually a number
        # we will ask the user a new input until it will insert a number
        while string.isdigit() != True:
            # if the string is not a number we will ask a new input
            string = raw_input("Wrong input! Your choice:\n>")

        # convert the string to int (integer number)
        choice = int(string)

        # depending on the chosen input we perform the right action
        if (choice == 1):  # insert a new task
            tasks_list = new_task(tasks_list)
        elif (choice == 2):  # remove a task
            tasks_list = remove_task(tasks_list)
        elif (choice == 3):  # remove tasks containing a provided string
            tasks_list = remove_multiple_tasks(tasks_list)
        elif (choice == 4):  # show the list of tasks
            print_sorted_list(tasks_list)
        elif (choice == 5):  # make the computer <speak> the first 2 tasks
            read_2_tasks(tasks_list)
        elif (choice == 6):  # exit
            ended = True

    # if user inserted the character "4", we save results on file
    if (ended and filename != ""):
        try:
            # open file in write mode
            txt = open(filename, "w")

            # empty the file
            txt.truncate()

            # write each task as a new line in the file
            for single_task in tasks_list:
                txt.write(single_task + "\n")

            # close the file
            txt.close()

        except IOError:
            print("Problems in saving todo list to file")
