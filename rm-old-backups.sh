#! /usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 
source ${__dir}/credentials.env

# Build image
docker build -q -t scaleway/s3-cleanup:latest ${__dir}/backup-cleanup/
# Run script
docker run --rm \
  -e "AWS_ACCESS_KEY_ID=${GITLAB_S3_KEY_ID}"      \
  -e "AWS_SECRET_ACCESS_KEY=${GITLAB_S3_SECRET}"  \
  -e "AWS_DEFAULT_REGION=${GITLAB_S3_REGION}"     \
  -e "AWS_ENDPOINT=${GITLAB_S3_ENDPOINT}"         \
  -e "KEEP_LAST=10"                               \
  scaleway/s3-cleanup
# Cleanup docker images
docker image prune -f > /dev/null

