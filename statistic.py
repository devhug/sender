import sys
sys.path.insert(0, 'privbin')
import boto3
import configuration
sets = configuration.Sets()
client = boto3.client('ses', aws_access_key_id=sets.aws_key, aws_secret_access_key=sets.aws_secret, region_name=sets.region)
response = client.get_send_statistics()['SendDataPoints']
for item in response:
    print("Time: {time}".format(time=item['Timestamp']))
    print("Bounces: {bounce}".format(bounce=item['Bounces']))
    print("Rejects: {reject}".format(reject=item['Rejects']))
    print("Complaint: {complaint}".format(complaint=item['Complaints']))
    print("attempt: {attemp}".format(attemp=item['DeliveryAttempts']))
    print("\n")