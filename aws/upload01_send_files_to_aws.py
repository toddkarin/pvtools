"""
This script uploads the pickled NSRDB files to AWS.
"""

import boto3
import os
import nsrdbtools
s3 = boto3.client('s3')
import glob

filename_list = glob.glob('/Users/toddkarin/Documents/NSRDB_compressed/*')

bucket = 'pvtools-nsrdb-pickle'

client = boto3.client('s3')

for j in range(len(filename_list)):
# for j in [0,1,2]:
    print('Iteration: {:.0f}, Complete: {:.3f}%'.format(j, j / len(filename_list) * 100))
    filename_to_upload = filename_list[j]
    filename_on_server = os.path.split(filename_list[j])[-1]

    client.upload_file(filename_to_upload, bucket, filename_on_server)

    #
    # try:
    #     client.upload_file(filename_to_upload, bucket, filename_on_server)
    # except Exception as e:
    #     print(e)
    # else:
    #     print("Successful upload to S3 bucket " + str(
    #         bucket) + " of file " + filename_to_upload)



print('--------')
print('files on server:')
# List files on server
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucket)

# Loop through items and print
for item in my_bucket.objects.all():
    print(item.key)
