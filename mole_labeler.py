import numpy as np
import cv2, csv
import os, sys, shutil
import curses
import tty, termios
import time

PICS_DIR = 'images'
WINDOW_NAME = 'Test Image'
results = []
current_fname = ""

def click_mole(event, x, y, flags, param):
    global results
    global current_fname

    if event == cv2.EVENT_LBUTTONDOWN:
        results.append([current_fname, x, y])

def labelMoles(results_fname):
    global results
    global current_fname

    processed_files = []
    # Make a list of unique image names already processed so we don't repeat
    if os.path.exists(results_fname):
        with open(results_fname, 'r') as results_f:
            reader = csv.reader(results_f)
            for r in reader:
                processed_files.append(r[0])
        processed_files = set(processed_files)
    else:
        # If this is the first run, create the file
        open(results_fname, 'w').close()

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, click_mole)

    for filename in os.listdir(PICS_DIR):
        if not filename.endswith(".png") or filename in processed_files:
            continue
        current_fname = filename
        test_im = cv2.imread(PICS_DIR + "/" + filename)
        cv2.imshow(WINDOW_NAME, test_im)
        key = cv2.waitKey(0) & 0xFF

        if key == ord('n'):
            continue
        elif key == ord('q'):
            print("Quit early, not all data processed!")
            break

    with open(results_fname, "a") as results_f:
        for r in results:
            results_f.write("%s,%d,%d\n" % (r[0], r[1], r[2]))

    print("Done! See results in %s" % results_fname)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Correct usage: python mole_labeler.py <results_filename>")
        exit(0)
    elif not sys.argv[1].endswith('.csv'):
        print("Error: The results_filename should be a .csv file")
        exit(0)

    results_fname = sys.argv[1]
    labelMoles(results_fname)
    exit(0)
