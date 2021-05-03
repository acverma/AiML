import json
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin, SFType

#which has username,password & token info and avail in the same venf folder
with open("login.json", "r") as login_file:
    creds = json.load(login_file)
#loginInfo = json.load(open('login.json'))
username = creds['login']['username']
password = creds['login']['password']
security_token = creds['login']['security_token']
# two types of domain type
# if use Production/ Devloper edition - login domain type
# if use UAT/DAV/ env - Test domain
#domain = 'login'
domain = 'Test'

## Connect Salesforce
# A Salesforce object is a salesforce session to access Salesforce REST API
# 1 method to connect but throughthis method possiblity that our crucial credentials would be exposed 
# sf = Salesforce(username=username,password=password,security_token=security_token,domain=domain)

# 2nd Method to pass only instance & session ID
session_id, instance = SalesforceLogin(username=username,password=password,security_token=security_token,domain=domain)
#sf = Salesforce(instance_url=instance,session_id=session_id)
sf = Salesforce(instance=instance,session_id=session_id)
print(sf)

for element in dir(sf):
    if not element.startswith('_'):
        if isinstance(getattr(sf,element),str):
            print('Property Name:{0} ;Value:{1}'.format(element,getattr(sf,element)))
#to know instance
instance
# for getting Salesforce Metadata 
metadata_org = sf.describe()
type(metadata_org)
metadata_org.keys()
print(metadata_org['encoding'])
print(metadata_org['maxBatchSize'])
#print(metadata_org['sobjects'])
print(type(metadata_org['sobjects']))

# to store the huge list in pandas
df_sobjects = pd.DataFrame(metadata_org['sobjects'])
print(df_sobjects)

#pd.set_option('display.max_columns',100)
#pd.set_option('display.max_rows',500)
#pd.set_option('display.min_rows',500)
#pd.set_option('display.max_colwidth',150)
#pd.set_option('display.width',120)
#pd.set_option('expand_frame_repr',True)

df_sobjects.to_csv('Org Metadata info Salesforce.csv',index=False)

# To get extract SALESFORCE Meta data objects Value & API
# Method 1
accounts = sf.account
type(accounts)
accounts_metadata = accounts.describe()
df_account_metadata = pd.DataFrame(accounts_metadata.get('fields'))
df_account_metadata.to_csv('Account Object Metadata.csv',index=False)

# Method 2

project = SFType('Project__c',session_id,instance)
project_metadata = project.describe()
df_project_metadata = pd.DataFrame(project_metadata.get('fields'))
df_project_metadata.to_csv('Project Object Metadata.csv',index=False)