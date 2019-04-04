import numpy as np
import pvlib
import nsrdbtools
import socket
import boto3
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import pandas as pd

# Parameters entering into Voc calculation:
# surface_azimuth
# surface_tilt
# Bvoco
# weather
# Voco
# Cells_in_Series
# N (Diode ideality factor)
# Latitude
# Longitude
# Air mass coefficients.


def calculate_max_voc(weather,info, module_parameters=None,system_parameters=None):


    cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
    inverter_parameters = cec_inverters['Power_Electronics__FS1700CU15__690V__690V__CEC_2018_']

    # Set location
    location = pvlib.location.Location(latitude=info['lat'],
                                       longitude=info['lon'])

    # Weather must have field dni, dhi, ghi, temp_air, and wind_speed.

    # Make pvsystem

    if system_parameters['mount_type'].lower() == 'fixed_tilt':
        system = pvlib.pvsystem.PVSystem(
            module_parameters=module_parameters,
            inverter_parameters=inverter_parameters,
            surface_tilt=system_parameters['surface_tilt'],
            surface_azimuth=system_parameters['surface_azimuth'],
             )
    elif system_parameters['mount_type'].lower() == 'single_axis_tracker':
        system = pvlib.tracking.SingleAxisTracker(
            module_parameters=module_parameters,
            inverter_parameters=inverter_parameters,
            axis_tilt=system_parameters['axis_tilt'],
            axis_azimuth=system_parameters['axis_azimuth'],
            max_angle=system_parameters['max_angle'],
            backtrack=system_parameters['backtrack'],
            gcr=system_parameters['ground_coverage_ratio']
        )

    # print(system_parameters['surface_tilt'])

    mc = pvlib.modelchain.ModelChain(system, location)
    mc.system.racking_model = system_parameters['racking_model']

    # mc.complete_irradiance(times=weather.index, weather=weather)
    mc.run_model(times=weather.index, weather=weather)


    df = weather
    df['v_oc'] = mc.dc.v_oc
    df['temp_cell'] = mc.temps['temp_cell']

    return (df, mc)



# sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')


# Get filedata for
if socket.gethostname()[0:6]=='guests':
    filedata = nsrdbtools.inspect_pickle_database('/Users/toddkarin/Documents/NSRDB_pickle/')
    # filedata = nsrdbtools.inspect_pickle_database('NSRDB_pickle')
else:
    filedata = nsrdbtools.inspect_pickle_database('NSRDB_pickle')

def get_sandia_module_dropdown_list():
    sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')

    sandia_module_dropdown_list = []
    for m in list(sandia_modules.keys()):
        sandia_module_dropdown_list.append(
            {'label': m.replace('_', ' '), 'value': m})

    return sandia_module_dropdown_list


