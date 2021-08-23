"""
This script checks the files on the AWS server.
"""

import boto3
import nsrdbtools
import numpy as np
import pandas as pd
import pvtoolslib
import vocmaxlib

file_list = pvtoolslib.get_s3_files()

# Print the file list.
for j in range(10):
    print(file_list[j])
