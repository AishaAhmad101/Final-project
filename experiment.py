# File name: experiment.py
# This experiment asks the user a math question and waits until a correct response is provided
# Aisha Ahmad

# =====================
# IMPORT MODULES
# =====================
import numpy as np
from psychopy import core, gui, visual, event, gui, visual, monitors, logging
import os
import random
from datetime import datetime
import csv

# =====================
# PATH SETTINGS
# =====================
# -define the main directory where you will keep all of your experiment files
main_dir = os.getcwd()

# -define the directory where you will save your data
data_dir = os.path.join(main_dir, 'data')

# -check that these directories exist
print(os.path.isdir(data_dir))

# =====================
# COLLECT PARTICIPANT INFO
# =====================
# -create a dialogue box that will collect current participant number, age, gender, handedness
# get date and time
# -create a unique filename for the data
exp_info = {'subject_nr': 0, 'age': 0, 'handedness': (
    'right', 'left', 'ambi'), 'gender': "", "session": 1}

my_dlg = gui.Dlg(title="Subject Info")
my_dlg.addText('exp_info')
# doesn't allow user to change value from preset
my_dlg.addFixedField('session:', 1)
my_dlg.addField('subject_nr:', 0)
my_dlg.addField('age:', 0)
my_dlg.addField('gender:', "")
my_dlg.addField('handedness:', choices=['right', 'left', 'ambi'])

print("All variables have been created! Now ready to show the dialog box!")
ok_data = my_dlg.show()

today_date = str(datetime.now())
ok_data.append(today_date)

filename = str(ok_data[1]) + '_' + today_date + '.csv'
sub_dir = os.path.join(main_dir, 'sub_info', filename)

# =====================
# STIMULUS AND TRIAL SETTINGS
# =====================
# -number of trials and blocks *
blocks = 1
trials = 10

# -stimulus properties like size, orientation, location, duration *
stimulus_height = 400
stimulus_width = 400
stimulus_orientation = "landscape"
stimulus_location = "center"
stimulus_duration = 1

# -start message text *
start_message = "Images will be shown to you for 1 seconds each to determine how long it takes you to find a face."

# =====================
# PREPARE CONDITION LISTS
# =====================
# -check if files to be used during the experiment (e.g., images) exist
# -create counterbalanced list of all conditions *
question_list = []
answer_list = []

for i in range(10):
    number1 = random.randint(0, 100)
    number2 = random.randint(0, 100)

    question_list.append(str(number1) + " + " + str(number2) + " =")
    answer_list.append(number1 + number2)

# =====================
# PREPARE DATA COLLECTION LISTS
# =====================
# -create an empty list for correct responses (e.g., "on this trial, a response of X is #correct")
correct_list = []

# -create an empty list for participant responses (e.g., "on this trial, response was a #X") *
response_list = []

# -create an empty list for response accuracy collection (e.g., "was participant #correct?") *
accuracy_list = []

# -create an empty list for response time collection *
response_time_list = []

# =====================
# CREATION OF WINDOW AND STIMULI
# =====================

# -define the monitor settings using psychopy functions
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([2736, 1824])

# -define the window (size, color, units, fullscreen mode) using psychopy functions
win = visual.Window(monitor=mon, size=(800, 800),
                    color=[-1, -1, -1], units="pix", fullscr=False)

# -define experiment start text unsing psychopy functions
start_msg = 'Welcome to my experiment! Addition questions will be displayed on the screen and your goal is to answer the questions as quick as possible. After entering your response you must click enter to lock in your answer. You will move on to the next question irregardless if you got the question right or not.\nPress any key to continue'

# -define block (start)/end text using psychopy functions
block_msg = "Press any key to continue to the next block."
end_trial_msg = "End of trial"

# -define stimuli using psychopy functions
# text=start_msg is the same as writing text="Welcome to my experiment!"
start_text = visual.TextStim(win, text=start_msg)
block_text = visual.TextStim(win, text=block_msg)
end_trial_text = visual.TextStim(win, text=end_trial_msg)

# -create response time clock
stimulus_timer = core.Clock()

# =====================
# START EXPERIMENT
# =====================
# -present start message text
start_text.draw()
win.flip()

# -allow participant to begin experiment with button press
event.waitKeys()

# =====================
# BLOCK SEQUENCE
# =====================
# -for loop for nBlocks *


for block in range(blocks):
    # -present block start message
    block_text.draw()
    win.flip()
    event.waitKeys()

    # =====================
    # TRIAL SEQUENCE
    # =====================
    # -for loop for nTrials *
    for trial in range(trials):
        # -set stimuli and stimulus properties for the current trial
        currentQ = visual.TextStim(win, text=question_list[trial])

        # =====================
        # START TRIAL
        # =====================
        stimulus_timer.reset()
        # -display question
        currentQ.draw()
        # -flip window
        win.flip()
        # -listen for key inputs
        key_list = []

        while 'return' not in key_list:
            keys = event.getKeys(
                keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'return'])

            key_list.extend(keys)

        end_timer = stimulus_timer.getTime()

        key_list.remove("return")
        answer = "".join(key_list)

        if answer == str(answer_list[trial]):
            correct_list.append(answer)
            accuracy_list.append(1)
        else:
            correct_list.append(-1)
            accuracy_list.append(-1)

        response_list.append(answer)
        response_time_list.append(end_timer)

# print(correct_list)
# print(accuracy_list)
# print(response_list)
# print(response_time_list)

# ======================
# END OF EXPERIMENT
# ======================
# -close window
win.close()

# creates and populates csv file
with open("./data/test.csv", 'w') as f:
    writer = csv.writer(f)

    # add headers to the csv file
    writer.writerow(["response", "accuracy",
                    "correct responses", "response time"])

    # adds rows to the csv file
    for i in range(len(response_list)):
        row = [response_list[i], accuracy_list[i],
               correct_list[i], response_time_list[i]]
        writer.writerow(row)
