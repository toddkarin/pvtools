import nsrdbtools
import pandas as pd
import numpy as np

filedata = nsrdbtools.inspect_pickle_database('/Users/toddkarin/Documents/NSRDB_pickle/')

filedata

filename = filedata['weather_fullpath'].iloc[0]

df = pd.read_pickle(filename,compression='xz')

df.to_pickle('test_pandas_pickle.pkl',compression='xz')

np.savez_compressed('test_numpy.npz',df=df,time=df.index)

dfn = np.load('test_numpy.npz')