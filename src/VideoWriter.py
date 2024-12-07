################################################################################
##
##  File: VideoWriter.py
##
##  The MIT License
##
##  Copyright (c) 2006 Division of Applied Mathematics, Brown University (USA),
##  Department of Aeronautics, Imperial College London (UK), and Scientific
##  Computing and Imaging Institute, University of Utah (USA).
##
##  Permission is hereby granted, free of charge, to any person obtaining a
##  copy of this software and associated documentation files (the "Software"),
##  to deal in the Software without restriction, including without limitation
##  the rights to use, copy, modify, merge, publish, distribute, sublicense,
##  and/or sell copies of the Software, and to permit persons to whom the
##  Software is furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included
##  in all copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
##  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
##  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
##  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
##  DEALINGS IN THE SOFTWARE.
##
##  Description:  Implements the VideoWriter object which handles saving frames 
##                and videos
##
################################################################################


import os
import math
import warnings
import numpy as np

import src.media_functions as med


class VideoWriter:
    def __init__(self, vw_spec, display):
        self.record = vw_spec["record"]
        if not self.record:
            return
        self.vw_spec = vw_spec
        self.display = display

        # initialise frames
        self.frame_dir = ".cache/frames"
        os.makedirs(self.frame_dir, exist_ok=True)
        self.max_frames = 21600     # 10 mins 36 fps
        self.zero_padding = math.ceil(math.log10(self.max_frames))
        self.frame_number = 0

        # output video
        self.vid_dir = vw_spec["vid_dir"]
        self.vid_name = vw_spec["vid_name"]
        self.vid_ftype = ".mp4"
        self.fps = vw_spec["fps"]
    
    def save_frame(self):
        if not self.record:
            return
        
        if self.frame_number > self.max_frames:
            return
        
        frame_name = f"f{self.frame_number:0{self.zero_padding}d}.npy"
        self.frame_number += 1
        np.save(os.path.join(self.frame_dir, frame_name), self.display.pxarray)
    
    def save_video(self):
        if not self.record:
            return
        
        os.makedirs(self.vid_dir, exist_ok=True)

        # find the lowest suitable name
        existing_vid_names = [f for f in os.listdir(self.vid_dir)
            # filter OUT directories
            # keep only vid_name[XYZ].mp4
            if os.path.isfile(os.path.join(self.vid_dir, f))
             and f.startswith(self.vid_name) 
             and f.endswith(self.vid_ftype)]
        
        if len(existing_vid_names) == 0:
            vid_name_unique = self.vid_name
        else:
            curr_highest = med.get_highest_strings_int(existing_vid_names, 
                                                       self.vid_name,
                                                       self.vid_ftype)
            
            vid_name_unique = f"{self.vid_name}" \
                f"{'' if curr_highest == -1 else curr_highest+1}"
            
        vid_path = os.path.join(self.vid_dir, vid_name_unique + self.vid_ftype)
        error = med.frames2vid(self.frame_dir, vid_path, framerate=self.fps)

        if error:
            raise RuntimeError("No video saved")

        print(f"Video saved successfully: {vid_path}")
        self.delete_frames()
    
    def delete_frames(self):
        if not self.frame_dir.startswith(".cache/"):
            warnings.warn(f"Directory {self.frame_dir} not deleted. " + \
                          "Must be in .../.cache/ for safety reasons.")
            return 1
        
        med.delete_all_files_in_directory(self.frame_dir)
        return 0
    
