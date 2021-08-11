import sys
sys.path.insert(0, 'privbin')
import boto3
import configuration
sets = configuration.Sets()
ses = boto3.client('ses', aws_access_key_id=sets.aws_key, aws_secret_access_key=sets.aws_secret, region_name=sets.region)

alldomain = ses.list_identities()
alldomain = alldomain['Identities']
cd = 0
for domain in alldomain:
    cd += 1
    print('{}. {}'.format(cd, domain))
inp = raw_input('Pilih yang mau di hapus? ')
try:
    inp = int(inp)
except:
    print("You have to input a number")
    exit()
deld = alldomain[inp - 1]
verify = raw_input('Are you sure wanna delete {} ? (y/yes): '.format(deld))
if verify.upper() == 'Y' or verify.upper() == 'YES':
    response = ses.delete_identity(Identity = deld)
    print(response)
    print("{} deleted".format(deld))
    