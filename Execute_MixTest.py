#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Execute_MixTest.py
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
import logging
import traceback
import shutil
import time, datetime
import math
import glob
import subprocess
import re
import os

SummaryResultCSVFile   = 'ResultsSummary.csv'
DetailResultsFileHead  = 'ResultsDetail'
COMMAND_AssociatedFile = './CopyAssociatedFiles.py'

# ---------------------------
# Initialize Section
# ---------------------------
def get_args():
    parser = argparse.ArgumentParser(
        description='Execute tool')

    parser.add_argument('-D', '--dest',
        action='store',
        type=str,
        required=True,
        help='Specify destination folder path.')

    parser.add_argument('-p', '--PreReadDir',
        action='store',
        default='NA',
        type=str,
        required=True,
        help='Specify a pre-read directory path.')

    parser.add_argument('-a', '--AssociatedFileListCSV',
        action='store',
        default='AssociatedFileList.csv',
        type=str,
        required=False,
        help='Specify a csv file name that is associated files list.')

    parser.add_argument('-P', '--PatternToExtract',
        action='store',
        default='test-001000KB_',
        type=str,
        required=False,
        help='Specify a pattern to extract specific size files in associated files')

    parser.add_argument('UnassociatedFileList',
        action='store',
        help='Specify a csv file name that is "unassociated" files list.')

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

    # detect file path delimiter.
    if os.name == "nt":
        delimiter = "\\"
    else:
        delimiter = "/"

    # Pre-Read a directory recursively,
    # and create associated files list
    #try:
    #    fp = open(args.AssociatedFileListCSV, "w")
    #    writer = csv.writer(fp, lineterminator='\n')
    #except:
    #    e = sys.exc_info()
    #    logging.error("{}".format(e))
    #    return(-1)
    #else:
    #    print("Pre-Read a directory(2-3 minutes): {}".format(args.PreReadDir))
    #    if not os.path.isdir(args.PreReadDir):
    #        print( "Invalid directory: {}\n".format(args.PreReadDir) )
    #        return(-1)
    #
    #    for dirpath, dirnames, filenames in os.walk(args.PreReadDir):
    #        for fileName in filenames:
    #            if args.PatternToExtract in fileName:
    #                row = [ "{0}{1}{2}".format(dirpath, delimiter, fileName) ]
    #                writer.writerow( row )
    #
    #                if args.debug:
    #                    print( "{}\n".format(row[0]) )
    #
    #    fp.close

    # Read the Copy File List
    print("Read unassociated files list")
    copylist = []
    with open( args.UnassociatedFileList, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            copylist.append(row)


    # Run Test
    print( "Run CopyFile programs." )
    StartTime = time.time()
    BaseTime = time.monotonic_ns()

    # execute job that is copying associated files
    cmd = [ 'python', COMMAND_AssociatedFile, '--basetime', str(BaseTime), '--dest', args.dest ]
    CopyAssociatedFileProcess = subprocess.Popen(cmd)


    time.sleep(3)

    print("kill")
    try:
        CopyAssociatedFileProcess.wait(timeout=0.001)
    except:
        CopyAssociatedFileProcess.terminate()


    return


    process = []
    idx = 0
    for row in copylist:
        cmd = [ 'python', ExecCommand, '--basetime', str(BaseTime), '--output', "temp_result_{0:04d}.csv".format(idx), row[0], row[1], row[2] ]
        process.append( subprocess.Popen(cmd) )
        idx += 1

    # Wait for process to finish
    for p in process:
        print("wait")
        p.wait()

    # Finish
    EndTime = time.time()
    print( "Done all test programs." )

    # Calculate the result
    time_delta = EndTime - StartTime
    StartDate = datetime.datetime.fromtimestamp( StartTime ).strftime("%Y/%m/%d %H:%M:%S")
    EndDate   = datetime.datetime.fromtimestamp( EndTime ).strftime("%Y/%m/%d %H:%M:%S")

    # Check results and Marge result file
    total = 0
    success = 0
    failed = 0
    unknown = 0
    repatter_success = re.compile(r"Success")
    repatter_failed  = re.compile(r"Failed")
    with open( "{0}_{1:04d}_{2}.csv".format(DetailResultsFileHead, NumOfFile, datetime.datetime.fromtimestamp( StartTime ).strftime("%Y%m%d_%H%M%S")), "w" ) as MargedFiled:
        for i in range(0,NumOfFile):
            try:
                fp = open( "temp_result_{0:04d}.csv".format(i), 'r')
                for line in fp:
                    if repatter_success.search(line):
                        success += 1
                    elif repatter_failed.search(line):
                        failed += 1
                    else:
                        unknown += 1
                    total += 1
                    MargedFiled.write(line)
                MargedFiled.flush()
                fp.close()
            except:
                e = sys.exc_info()
                logging.error("{}".format(e))
            
        MargedFiled.close()

    # Write to the summary file  
    with open(SummaryResultCSVFile, "a") as FpSummary:
        writer = csv.writer(FpSummary, lineterminator='\n')

        print( "NumOfFiles, NumOfParallels, ExeTime(sec), StartTime, EndTime, SuccessedFiles, FailedFiles, UnknownFIles, TotalFiles" )
        row = [ NumOfFile, NumOfFile, time_delta, StartDate, EndDate, success, failed, unknown, total ]
        print (row)
        writer.writerow( row )


    # Delete temporary files
    for fn in glob.glob( "temp_result_*.csv" ):
            os.remove(fn)

    # Finish
    return

if __name__ == "__main__":
    sys.exit(main())