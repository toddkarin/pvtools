"""
pvtoolslib

This module has functions specific for running the pvtools.lbl.gov website.

Todd Karin
04/24/2019
"""


import numpy as np
import pvlib
import nsrdbtools
# import socket
import boto3
import botocore
import io
import pandas as pd
import pytz
import glob
import pvcz

# try:
#     import cPickle as pickle
# except:
#     import pickle
#

version = '1.0.1'
contact_email = 'pvtools.lbl@gmail.com'

# sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')


# List of modules in the CEC database.
cec_modules = pvlib.pvsystem.retrieve_sam('CeCMod')
cec_module_dropdown_list = []
for m in list(cec_modules.keys()):
    cec_module_dropdown_list.append(
        {'label': m.replace('_', ' '), 'value': m})

# Bucket for storing s3
bucket = 'pvtools-nsrdb-pickle'

# Get pvcz data
pvcz_df = pvcz.get_pvcz_data()
pvcz_info = pvcz.get_pvcz_info()

pvcz_legend_str = {
    'lat': 'Latitude (degrees)',
    'lon': 'Longitude (degrees)',
    'T_equiv_rack': 'Equivalent Temperature, Rack Mount (C)',
    'T_equiv_roof': 'Equivalent Temperature, Roof Mount (C)',
    'specific_humidity_mean': 'Mean Specific Humidity (g/kg)',
    'T_velocity': 'Mean Temperature Velocity, Rack Mount (C/hr)',
    'GHI_mean' : 'GHI (kWh/m2/day)',
    'wind_speed': '25-year Mean Recurrence Interval wind speed (m/s)',
    'T_ambient_min': 'Min ambient temperature (C)',
    'KG_zone': 'Koppen-Geiger Zone',
    'T_equiv_rack_zone': 'Equivalent Temperature Zone, Rack',
    'T_equiv_roof_zone': 'Equivalent Temperature Zone, Roof',
    'specific_humidity_mean_zone': 'Mean Specific Humidity Zone',
    'wind_speed_zone': 'Wind Speed Zone',
    'pvcz': 'Photovoltaic Climate Zone',
    'pvcz_labeled': 'Photovoltaic Climate Zone (text)',
}
# Make list of options
pvcz_stressor_dropdown_list = []
for p in ['T_equiv_rack', 'T_equiv_roof', 'specific_humidity_mean',
                    'T_velocity', 'GHI_mean', 'wind_speed', 'T_ambient_min',
                    'T_equiv_rack_zone', 'T_equiv_roof_zone', 'specific_humidity_mean_zone',
                    'wind_speed_zone', 'pvcz']:
    pvcz_stressor_dropdown_list.append({'label': pvcz_legend_str[p], 'value': p})


def get_s3_files():
    """

    Gets files in the s3 bucket and returns a list.

    Returns
    -------
    files : list
        list of filenames in the s3 bucket.
    """



    # List files on server
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)

    files = []
    for item in my_bucket.objects.all():
        files.append(item.key)

    return files


def build_s3_filename_list():
    """
    Build filename list from s3.

    Returns
    -------
    filedata : dataframe

        Pandas dataframe providing information on files in database. Files
        must end with '.npz'. Dataframe has fields:

        'location_id' - NSRDB location ID (integer)

        'lat' - latitude in degrees.

        'lon' - longitude in degrees

        'filename' - name of file.

    """

    location_id = []
    lat = []
    lon = []

    print('Getting s3 files...')
    filename = get_s3_files()
    print('done.')

    # Extract location id, lat and lon.
    for key in filename:
        if key.endswith('.npz'):
            filename_parts = key.split('_')

            location_id.append(int(filename_parts[0]))
            lat.append(float(filename_parts[1]))
            lon.append(float(filename_parts[2][0:-4]))


    # Create a DataFrame
    filedata = pd.DataFrame.from_dict({
        'location_id': location_id,
        'lat': lat,
        'lon': lon,
        'filename': filename,
    })

    # Redefine the index.
    filedata.index = range(filedata.__len__())

    # Save to file
    filedata.to_pickle('s3_filedata.pkl')

    return filedata


def get_s3_filename_df():
    """
    Get the list of files on AWS s3.

    filedata = pvtoolslib.get_s3_filename_list()

    Returns
    -------
    filedata: dataframe
    """
    return pd.read_pickle('s3_filedata.pkl')


def get_s3_npz(filename):
    """

    get_s3_npz(filename) gets the s3 file stored in the s3 bucket called
    filename.

    Parameters
    ----------
    filename

    Returns
    -------
    data : dict
        dictionary containing all fields in the npz file.

    """

    bucket = 'pvtools-nsrdb-pickle'

    # connect to AWS S3
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket, filename)

    data = {}

    with io.BytesIO(obj.get()["Body"].read()) as f:
        # rewind the file
        f.seek(0)
        arr = np.load(f)

        for var in list(arr.keys()):
            data[var] = arr[var]

    return data




def get_s3_weather_data(filename):
    """

    get_s3_weather_data(filename) gets the weather and info file from the s3
    file filename

    Parameters
    ----------
    filename

    Returns
    -------
    weather : dataframe
        Dataframe containing weather data.

    info : dict
        Dictionary containing information on the weather data.

    """

    # filename = '1000030_43.77_-82.98.npz'

    info = get_s3_npz(filename)

    return nsrdbtools.build_weather_info(info)

