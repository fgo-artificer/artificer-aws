import boto3
import requests
import json

s3_client = boto3.client('s3')

API_URL = 'https://gamepress.gg/sites/default/files/aggregatedjson/calc-material-images-FGO.json'
S3_BUCKET = 'artificer-extract'
FILE_NAME = 'materials.json'

def download_json_from_url(url):
    response = requests.get(url)
    dict_response = dict()
    dict_response['data'] = response.json()
    return json.dumps(dict_response)

def write_json_to_local(json, local_fpath):
    with open(local_fpath, "w+") as f:
        f.write(json)
        f.close()

def upload_json_to_s3(json, local_file_name, bucket_name, remote_file_name):
    s3_client.put_object(Body=str(open(local_file_name, 'r').readline()).encode('utf-8'), Bucket=bucket_name, Key='{}/{}'.format(bucket_name, remote_file_name))

def lambda_handler(event, context):
    json_materials = download_json_from_url(API_URL)
    upload_json_to_s3(json_materials, S3_BUCKET, FILE_NAME)

def main():
    json_materials = download_json_from_url(API_URL)
    write_json_to_local(json_materials, '/tmp/' + FILE_NAME)
    #print('json_materials: ' + str(json_materials))
    resp = upload_json_to_s3(json_materials, '/tmp/' + FILE_NAME, S3_BUCKET, FILE_NAME)
    print('upload_json_to_s3: ' + str(resp))

main()
