"""
This script checks the files on the AWS server and builds an index. 
"""

import boto3
import nsrdbtools
import numpy as np
import pandas as pd
import pvtoolslib
import vocmaxlib

file_list = pvtoolslib.get_s3_files()

for j in range(10):
    print(file_list[j])
# filedata = vocmaxlib.build_nsrdb_database()

# filedata.to_pickle('aws_file_list.pkl')



# filedata = pd.read_pickle('aws_file_list.pkl')

