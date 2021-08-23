import pvtoolslib

# Build the s3 filename database and save to file.
pvtoolslib.build_s3_filename_list()

filedata = pvtoolslib.get_s3_filename_df()

print(filedata)