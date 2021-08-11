import sys
sys.path.insert(0, 'privbin')
import boto3
import configuration
sets = configuration.Sets()
ses = boto3.client('ses', aws_access_key_id=sets.aws_key, aws_secret_access_key=sets.aws_secret, region_name=sets.region)
response = ses.verify_domain_identity(Domain = 'wongtuobisoopo.com')
print("Done:\nSet record to your domain")
print("Record Type: TXT")
print("Record Name: _amazonses")
print("Record Value: {}".format(response['VerificationToken']))
print(response)