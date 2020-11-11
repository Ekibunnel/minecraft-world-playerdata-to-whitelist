import os
from requests import Session
import json
import sys
import warnings

List_uuid = [];

for file in os.listdir("./"):
    if file.endswith(".dat"):
        List_uuid.append(os.path.splitext(file)[0])

session = Session()
session.head('https://api.mojang.com')

white_list = []

#  Get name from uuid
with open("generated.whitelist.json", "w") as f :
    for uuid in List_uuid:
        response = session.get(
            url='https://api.mojang.com/user/profiles/'+str(uuid.replace('-', ''))+'/names',
        )
        if response.ok :
            try:
                api_response = json.loads(response.text)
                uuid_name = api_response[-1]["name"]
            except ValueError:
                warnings.warn(" Can't get name for uuid "+str(uuid)+" .")
                sys.exit()
            print(uuid+" is "+uuid_name)
            uuid_dict = {"uuid" : uuid , "name" : uuid_name}
            dictionary_copy = uuid_dict.copy()
            white_list.append(uuid_dict)
        else:
            warnings.warn(" Mojang API returned an error for uuid "+str(uuid)+" : status "+str(response.status_code))
            print(response.text)
            sys.exit()
    #f.write(str(white_list).replace("'", '"'))
    f.write(json.dumps(white_list, sort_keys=True, indent=4))
    f.close()
