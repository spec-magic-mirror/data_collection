import numpy as np
import cv2
import sys, os, csv
from shutil import copyfile

class MoleCropper:
    version = "0.0.1"

    def __init__(self, dir, fname):
        self.mole_list = []
        self.cropped_dir = dir + "/cropped"
        self.original_dir = "images"
        self.size = 64
        self.img_idx = 0
        self.x_idx = 1
        self.y_idx = 2
        if not os.path.exists(self.cropped_dir):
            os.makedirs(self.cropped_dir)
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            #headers = reader.next()
            for row in reader:
                self.mole_list.append(row)

    def cropMoles(self):
        count = 0
        for mole in self.mole_list:
            img_fname = mole[self.img_idx]
            x = int(float(mole[self.x_idx]))
            y = int(float(mole[self.y_idx]))
            img_path = self.original_dir + "/" + img_fname
            if os.path.exists(img_path):
                img = cv2.imread(img_path)
                crops = self.getMoleCrop(img, x, y)
                if crops:
                    mole_img = self.getMoleImage(img, crops)
                    cv2.imwrite(self.cropped_dir + "/%d.png" % count, mole_img)
                    count += 1

    def getMoleCrop(self, original_img, x, y):
        crop_pts = []
        # TODO: find better way of handling out of bounds instead of just skipping them
        y_min = y-self.size/2
        y_max = y+self.size/2
        x_min = x-self.size/2
        x_max = x+self.size/2
        if y_min >= 0 and x_min >= 0 \
                and y_max < original_img.shape[0] and x_max < original_img.shape[1]:
            crop_pts = [y_min, y_max, x_min, x_max]
            crop_pts = [int(c) for c in crop_pts]
        return crop_pts

    def getMoleImage(self, original_img, mc):
        y = (mc[1]-mc[0])/2 + mc[0]
        x = (mc[3]-mc[2])/2 + mc[2]

        mole_img = original_img[mc[0]:mc[1], mc[2]: mc[3]]
        #if mole_img.shape[0] > self.size:
        #    mole_img = cv2.resize(mole_img, (self.size, self.size))
        return mole_img

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Error: Incorrect Usage"
        print "Correct Usage: mole_crop.py <session folder> <coords_csv>"
        print "The .csv file should have rows as <img_filename, x, y>"
        print "e.g. \"python mole_crop.py test test/mole_list.csv\""
        exit(-1)

    mc = MoleCropper(sys.argv[1], sys.argv[2])
    mc.cropMoles()

    exit(0)
