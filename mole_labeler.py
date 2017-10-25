import numpy as np
import cv2, csv
import os, sys, shutil
import curses
import tty, termios
import time

results = []
current_fname = ""

def click_mole(event, x, y, flags, param):
    global results
    global current_fname

    if event == cv2.EVENT_LBUTTONDOWN:
        results.append([current_fname, x, y])

def labelMoles(images_dir, results_fname):
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
    window_name = ''
    
    for filename in os.listdir(images_dir):
        if (not filename.endswith(".png") and not filename.endswith(".jpg")) \
            or filename in processed_files:
            continue
        current_fname = filename
        cv2.namedWindow(current_fname)
        cv2.setMouseCallback(current_fname, click_mole)

        test_im = cv2.imread(images_dir + "/" + filename)
        cv2.imshow(current_fname, test_im)
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyWindow(current_fname)

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
    if len(sys.argv) < 3:
        print("Correct usage: python mole_labeler.py <images_directory> <results_filename>")
        exit(0)
    elif not sys.argv[2].endswith('.csv'):
        print("Error: The results_filename should be a .csv file")
        exit(0)

    images_dir = sys.argv[1]
    results_fname = sys.argv[2]
    labelMoles(images_dir, results_fname)
    exit(0)
