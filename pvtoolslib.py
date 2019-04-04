import numpy as np
import pvlib
# import nsrdbtools
# import socket
import boto3
import botocore
import io
import pandas as pd
import pytz
import glob

# try:
#     import cPickle as pickle
# except:
#     import pickle
#

sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')

# Bucket for storing s3
bucket = 'pvtools-nsrdb-pickle'






def get_s3_files():



    # List files on server
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)

    files = []
    for item in my_bucket.objects.all():
        files.append(item.key)

    return files






def build_filename_list(base_dir):
    """
    Build filename list from directory, not working yet.

    Returns
    -------

    """

    location_id = []
    lat = []
    lon = []

    print('Getting s3 files...')
    # filename = get_s3_files()
    base_dir = '/Users/toddkarin/Documents/NSRDB_compressed/*'
    filename = glob.glob(base_dir)

    print(filename)
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



# build_filename_list('')



def build_s3_filename_list():
    """
    Build filename list from s3.

    Returns
    -------

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

#
# def build_nsrdb_database():
#
#
#     bucket = 'pvtools-nsrdb-pickle'
#     # List files on server
#     s3 = boto3.resource('s3')
#     my_bucket = s3.Bucket(bucket)
#
#     # filedata = pd.DataFrame(columns=['lat','lon','type','filepath'])
#     weather_filename = []
#     info_filename = []
#     filename = []
#     # weather_fullpath = []
#
#     # info_fullpath = []
#     location_id = []
#     lat = []
#     lon = []
#     type = []
#
#     # Cycle through files in directory, extract info from filename without opening file.
#     # Note this would break if NREL changed their naming scheme.
#
#     for item in my_bucket.objects.all():
#         key = item.key
#
#         if key.endswith('.pkl'):
#             temp = key.split('_')
#
#             # if key.find('weather')>=0:
#             #     weather_filename.append(key)
#             #     info_filename.append('')
#             # elif key.find('info')>=0:
#             #     weather_filename.append('')
#             #     info_filename.append(key)
#             #
#             filename.append(key)
#
#             # weather_fullpath.append(os.path.join(root, filename))
#             location_id.append(int(temp[0]))
#             lat.append(float(temp[1]))
#             lon.append(float(temp[2]))
#             type.append(temp[3][0:-4])
#             #     info_filename.append(filename[0:-11] + 'info.pkl')
#             # info_fullpath.append(os.path.join(root, filename)[0:-11] + 'info.pkl')
#
#     # Note that locations will already be sorted by default.
#     location_id_combined = np.array(location_id)[np.array(type) == 'weather']
#     location_id_combined_info = np.array(location_id)[np.array(type) == 'info']
#
#     # Double check hat all locations match:
#     if not np.all(location_id_combined == location_id_combined_info):
#         raise Exception('Not the same number of weather and info files.')
#
#     lat_combined = np.array(lat)[np.array(type) == 'weather']
#     lon_combined = np.array(lon)[np.array(type) == 'weather']
#     weather_filename = np.array(filename)[np.array(type) == 'weather']
#     info_filename = np.array(filename)[np.array(type) == 'info']
#
#     # Create a DataFrame
#     filedata = pd.DataFrame.from_dict({
#         'location_id': location_id_combined,
#         'lat': lat_combined,
#         'lon': lon_combined,
#         'weather_filename': weather_filename,
#         'info_filename': info_filename
#     })
#
#     # Redefine the index.
#     filedata.index = range(filedata.__len__())
#
#     return filedata


def get_s3_npz(filename):
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

    # filename = '1000030_43.77_-82.98.npz'

    info = get_s3_npz(filename)

    for f in info:
        if len(info[f]) == 1:
            info[f] = info[f][0]

    weather = pd.DataFrame.from_dict({
        'year': info['year'],
        'month': info['month'],
        'day': info['day'],
        'hour': info['hour'],
        'minute': info['minute'],
        'dni': info['dni'],
        'ghi': info['ghi'],
        'dhi': info['dhi'],
        'temp_air': info['temp_air'],
        'wind_speed': info['wind_speed'],
    }
    )

    weather.index = pd.to_datetime(
        pd.DataFrame.from_dict({
            'year': info['year'],
            'month': info['month'],
            'day': info['day'],
            'hour': info['hour'],
            'minute': info['minute'],
        })
    )

    weather.index = weather.index.tz_localize(
        pytz.FixedOffset(float(info['local_time_zone'] * 60)))

    return weather, info


def load_compressed_nsrdb_file(filename):
    """
    Load compressed file

    Example: load_compressed_nsrdb_file('1303017_41.57_-72.18.npz')


    Parameters
    ----------
    filename

    Returns
    -------

    """
    # fileanme = '1303017_41.57_-72.18.npz'

    info = {}

    # Load into a dictionary.
    with np.load(filename) as npfile:
        # rewind the file
        for var in list(npfile.keys()):
            info[var] = npfile[var]

    # Get rid of arrays for one-element long variables.
    for f in info:
        if len(info[f]) == 1:
            info[f] = info[f][0]

    weather = pd.DataFrame.from_dict({
        'dni': info['dni'],
        'ghi': info['ghi'],
        'dhi': info['dhi'],
        'temp_air': info['temp_air'],
        'wind_speed': info['wind_speed'],
    }
    )

    weather.index = pd.to_datetime(
        pd.DataFrame.from_dict({
            'year': info['year'],
            'month': info['month'],
            'day': info['day'],
            'hour': info['hour'],
            'minute': info['minute'],
        })
    )

    weather.index = weather.index.tz_localize(
        pytz.FixedOffset(float(info['local_time_zone'] * 60)))

    return weather, info





# def get_s3_obj(filename):
#     bucket = 'pvtools-nsrdb-pickle'
#     # connect to AWS S3
#     s3 = boto3.resource('s3')
#
#
#     # client = boto3.client('s3') #low-level functional API
#
#
#     try:
#         obj = s3.Object(bucket, filename).get()['Body'].read()
#         # df = pickle.loads(obj)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == "404":
#             print("The object does not exist.")
#     else:
#         print("File download successful")
#
#     return obj
#
# def load_weather_s3(filename):
#
#     obj = get_s3_obj(filename)
#     return pickle.loads(obj,compression='xz')
#
#
# def load_info_s3(filename):
#     obj = get_s3_obj(filename)
#     return pickle.loads(obj)
