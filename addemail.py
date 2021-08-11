import sys
sys.path.insert(0, 'privbin')

import boto3
import configuration

sets = configuration.Sets()
ses = boto3.client('ses', aws_access_key_id=sets.aws_key, aws_secret_access_key=sets.aws_secret, region_name=sets.region)
response = ses.verify_email_identity(EmailAddress = 'noreply@unitedsecurity609.com')
print(response)