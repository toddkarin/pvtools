

import boto3
import botocore
import pandas as pd
import numpy as np
import pvtoolslib
import io
import resource
import pytz

filename = '1000030_43.77_-82.98.npz'

data = pvtoolslib.get_s3_npz(filename)

weather, info = pvtoolslib.get_s3_weather_data(filename)


print(info)