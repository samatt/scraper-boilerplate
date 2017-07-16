import boto3, time
from io import StringIO
from log import log
from config import config


def upload_file(filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id=config['s3']['access_key_id'],
        aws_secret_access_key=config['s3']['secret_access_key']
        )
    s3.upload_file(filename, config['s3']['bucket'], filename)


def upload_strings(data, filename):
    bucket = config['s3']['bucket']
    key = "%s/%s" % (config['scrape_info']['name'], filename)
    s3 = boto3.client(
        's3',
        aws_access_key_id=config['s3']['access_key_id'],
        aws_secret_access_key=config['s3']['secret_access_key']
        )
    t1 = time.time()
    s3.put_object(Body=str.encode(data), Bucket=bucket, Key=key)
    t2 = time.time() - t1
    log.info(" 🗄  --> finished uploading %s to %s in %0.2fs " % (key, bucket, t2))


def load_data_from_bucket():
    s3 = boto3.resource(
            's3',
            aws_access_key_id=config['s3']['access_key_id'],
            aws_secret_access_key=config['s3']['secret_access_key']
          )
    bucket = s3.Bucket(config['s3']['bucket'])
    data = []
    for obj in bucket.objects.filter(Prefix=config['scrape_info']['name']):
        if 'html' in obj.key:
            key = obj.key
            body = obj.get()['Body'].read()
            data.append((key, body))
    return data
