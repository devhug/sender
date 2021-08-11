import sys
sys.path.insert(0, 'privbin')
import boto3
region = 'ap-northeast-2'
aws_key = 'AKIAYTMGNQUILZVR5S6M'
aws_secret = '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'

client = boto3.client('sts', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret, region_name=region)
print(client.get_caller_identity())