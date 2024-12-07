import os
import warnings
import sys
import time

from PIL import Image
import cv2
import numpy as np


def array2image(pxarray, output_path):
    output_path += "" if output_path.endswith(".png") else ".png"
    Image.fromarray(pxarray.astype("uint8")).save(output_path)

def frames2vid(fpath: str,
               vpath: str,
               framerate: int = 30,
               flabel: str = "f",
               fftype: str = "png"):
        """converts images labelled frame__.png to mp4 video"""

        fpath = os.path.join(fpath, "")

        if not vpath.endswith(".mp4"):
            vpath += ".mp4" 

        # get list of files if of the form "frame__.png"
        files = [f for f in os.listdir(fpath)
                 if f.startswith(flabel)
                 and f.endswith(".npy")]

        Nframes = len(files)

        if not Nframes:
            warnings.warn(f"No files {flabel}__.npy found")
            return 1
        
        # get image dimensions based off the first file in files
        # height, width, _ = cv2.imread(os.path.join(fpath, files[0])).shape
        height, width, _ = np.load(f"{fpath}{files[0]}").shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(vpath, fourcc, framerate, (width, height))

        t0 = time.time()
        print("\nStitching frames together...")

        for i, file in enumerate(files):
            filename = f"{fpath}{file}"
            pxarray = np.load(filename)[..., ::-1].astype(np.uint8)
            out.write(pxarray)
            loading_bar(i, Nframes, w_tot=50, t0=t0)
        out.release()

        return 0

    
def loading_bar(i: int,
                r: int,
                w_tot: int = 50,
                t0: float = None):
    """
    Create a simple loading bar to show to progress of a for loop

    eg. t0 = time.time()
        for i in range(r):
            code()
            loading_bar(i, r, 50, t0)
    """

    w = w_tot / r
    i += 1

    t_fin = time.time()
    sys.stdout.write("\r|{}{}| {:>6}%\t\t{}".format(
        "█" * round(i * w),
        "-" * round((r - i) * w),
        round(100 * i / r, 2),
        "Done!\n" if i == r
        else "Estimated time left: {}s".format(
            round((t_fin - t0) * (r - i) / i)) if t0 else ""))
    sys.stdout.flush()


def str_between(string: str,
                start: str,
                end: str):
    """returns text between [start] and [end]"""

    return (string.split(start))[1].split(end)[0]


def get_highest_strings_int(strings: list, 
                            start_string: str, 
                            end_string: str):
    i1 = len(start_string)
    i2 = len(end_string)
    
    highest = -1
    
    for string in strings:
        int_string = string[i1:len(string) - i2]
        if int_string == "":
            highest = max(highest, 0)
            continue
        
        try:
            i = int(int_string)
        except ValueError:
            continue

        highest = max(i, highest)

    return highest


def delete_all_files_in_directory(dir_path):
    """
    Delete all files in a directory
    Does not delete subdirectories
    """

    for fname in os.listdir(dir_path):
        file_path = os.path.join(dir_path, fname)
        
        # Check if it's a file (not a subdirectory)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Delete the file