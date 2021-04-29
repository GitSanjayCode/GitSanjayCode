import boto3
s3 = boto3.resource('s3')

my_bucket = s3.Bucket('coderbytechallengesandbox')

for file in my_bucket.objects.all():
    filename=file.key
    if filename.startswith('_cb_'):
        print(filename)
