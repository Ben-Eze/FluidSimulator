################################################################################
##
##  File: Log.py
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
##  Description:  Implements the Log class, a simple wrapper around the logging
##                library for the functionality needed
##
################################################################################


import logging


class Log:
    log = None

    def __init__(self, log_spec):
        # Create a custom logger
        self.logger = logging.getLogger('simple_logger')
        self.logger.setLevel(logging.DEBUG)

        # Create handlers based on the provided configuration
        if log_spec["verbose"]:
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.DEBUG)
            c_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m %H:%M:%S')
            c_handler.setFormatter(c_format)
            self.logger.addHandler(c_handler)
        
        if log_spec["log_file"]:
            f_handler = logging.FileHandler("out/.log")
            f_handler.setLevel(logging.DEBUG)
            f_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m %H:%M:%S')
            f_handler.setFormatter(f_format)
            self.logger.addHandler(f_handler)
        
        Log.log = self

    def __call__(self, *args, warning=False, error=False):
        message = ", ".join(str(arg) for arg in args)
        if error:
            self.logger.error(message)
        elif warning:
            self.logger.warning(message)
        else:
            self.logger.info(message)

    # # Example usage
    # log = Log(console_log=True)
    # x = "This is a test"
    # y = "Another message"
    # log(x)  # Logs as INFO
    # log(x, y)  # Logs as INFO
    # log(x, warning=True)  # Logs as WARNING
    # log(x, y, error=True)  # Logs as ERROR
