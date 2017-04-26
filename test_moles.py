import numpy as np
import cv2
import os, sys, shutil
import curses
import tty, termios
import time

# From https://gist.github.com/jasonrdsouza/1901709
def getchar():
    # Returns a single character from standard input
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def testMoles(trial_num):
    data = []
    for filename in os.listdir(trial_num):
        if not filename.endswith(".jpg") or filename == "full_face.jpg":
            continue
        path = trial_num + "/" + filename
        print path
        test_im = cv2.imread(path)
	
	c = ''
	while c not in ["x","n","y"]:
	    cv2.imshow("Test Image", test_im)
            c = chr(cv2.waitKey())

        if c == "x":
            print "Exiting early - Results not saved!!!"
            exit(0)
        elif c == "n":
            data.append((path, "0"))
        elif c == "y":
            data.append((path, "1"))

    with open("train_data.csv","a+") as train_data:
        for row in data:
            train_data.write(row[0] + "," + row[1] + "\n")

    shutil.copytree(trial_num, "completed/" + trial_num)
    shutil.rmtree(trial_num)

    print "Done! See results in csv file."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Correct usage: python test_moles.py <trial number>"
        exit(0)

    trial_num = sys.argv[1]
    testMoles(trial_num)
    exit(0)
