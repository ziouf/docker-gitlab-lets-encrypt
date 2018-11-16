#! /usr/bin/env python3

import os
import boto3
import logging

_bucket   = os.getenv('AWS_BUCKET', 'gitlab-backups')
_region   = os.getenv('AWS_DEFAULT_REGION', 'nl_ams')
_endpoint = os.getenv('AWS_ENDPOINT', 'https://s3.{}.scw.cloud'.format(_region))
_keepLast = int(os.getenv('KEEP_LAST', 5))


logging.basicConfig(level=logging.INFO)

bucket = boto3.resource('s3', endpoint_url=_endpoint).Bucket(_bucket)
unsorted = [file.Object() for file in bucket.objects.all()]
toBeDeleted = sorted(unsorted, key=lambda o: o.last_modified, reverse=True)[_keepLast:]

if len(toBeDeleted) > 0:
  for obj in toBeDeleted:
    logging.info('Deleting {}'.format(obj.key))
    obj.delete()

else:
  logging.info('Nothing to delete. Exiting')


