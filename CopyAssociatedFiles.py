#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  CopyAssociatedFiles.py
#  ======
#  Copyright (C) 2019 n.fujita
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from __future__ import print_function

import sys
import argparse
import csv
import random
import time
import subprocess

ExecCommand = './_do_FileCopy.py'

# ---------------------------
# Initialize Section
# ---------------------------
def get_args():
    parser = argparse.ArgumentParser(
        description='Execute tool')

    parser.add_argument('-p', '--parallel',
        action='store',
        default='5',
        type=int,
        required=False,
        help='Specify number of parallel.')

    parser.add_argument('-a', '--AssociatedFileListCSV',
        action='store',
        default='AssociatedFileList.csv',
        type=str,
        required=False,
        help='Specify a csv file name that is a ssociated files list.')

    parser.add_argument('-D', '--dest',
        action='store',
        type=str,
        required=True,
        help='Specify destination folder path.')

    parser.add_argument('-b','--basetime',
        action='store',
        type=int,
        default="0",
        required=False,
        help='Set the base time(monotonic clock as nanoseconds)')

    parser.add_argument('-d','--debug',
        action='store_true',
        default=False,
        required=False,
        help='Enable dry-run')

    return( parser.parse_args() )

# ---------------------------
# Main function
# ---------------------------
def main():

    # Initialize
    args = get_args()

    # Set base time
    if args.basetime <= 0:
        basetime = time.monotonic_ns()
    else:
        basetime = int(args.basetime)

    # Read the Copy File List
    filelist = []
    with open( args.AssociatedFileListCSV, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            filelist.append(row)
    NumOfFile = len(filelist)

    # Set Poll and process status array
    # Kill itself process and end, because it is an infinite loop.
    process = []
    index = 0
    while True:

        # Check Process status
        new_array = []
        for i in process:
            # Check wait
            try:
                i.wait(timeout=0.001)
            except subprocess.TimeoutExpired:
                pass
            # debug message
            if args.debug:
                print("pid={}  ret={}".format(i.pid, i.returncode))
            # check chiled process status
            if i.returncode is None:
                new_array.append(i)
        
        #reflesh process array
        process = new_array

        # run a copy process, if number of processes has not reached the upper limit.
        while len(process) < args.parallel:

            # choise 2 souce files.
            src = random.sample(filelist, 2)

            # run process
            cmd = [ 'python', ExecCommand, '--basetime', str(basetime), '--output', "temp_result_associated_{0:04d}.csv".format(index), src[0][0], src[1][0], args.dest ]
            process.append( subprocess.Popen(cmd) )
            index += 1
            time.sleep(0.1)

        # Wait
        if args.debug:
            print("running process={}".format(len(process)))
        time.sleep(0.1)

if __name__ == "__main__":
    sys.exit(main())

