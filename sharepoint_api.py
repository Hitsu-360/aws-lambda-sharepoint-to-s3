from datetime import datetime

import requests
import re
import json
import csv
import io
import xlrd
import pandas
import re

class sp_api():

    def __init__(self, credentials):

        self.credentials = credentials
        self.s = requests.Session()
        self.get_token()

    def get_token(self):

        # Set Authentication with Bearer Token
        self.s.headers.update({'Authorization':'Bearer'})

        r = self.s.get(f"https://{self.credentials['url']}/_vti_bin/client.svc/")

        #Extract tenetid and resource
        tenentid = re.findall('realm=\"(.*?)\"', r.headers['WWW-Authenticate'])[0]
        resourceinfoval = re.findall('client_id=\"(.*?)\"', r.headers['WWW-Authenticate'])[0]

        # Get token
        url = f'https://accounts.accesscontrol.windows.net/{tenentid}/tokens/OAuth/2'

        headers = {'Content-Type':'application/x-www-form-urlencoded'}

        payload = {
            'grant_type': 'client_credentials',
            'client_id': f"{self.credentials['client_id']}@{tenentid}",
            'client_secret': self.credentials['secret'],
            'resource': f"{resourceinfoval}/{self.credentials['url']}@{tenentid}"
        }

        # Request token
        r = self.s.post(url, headers = headers, data = payload)

        # Set Token
        self.token = re.findall('access_token\":\"(.*?)\"', r.text)[0]

        self.s.headers = {
            'Authorization':f'Bearer {self.token}',
            'Accept':'application/json;odata=verbose',
            'content-type':'application/json;odata=verbose'
        }

        print('Token Acquired')

    def get_file_as_csv(self, site, file, skip_lines, sheet):
        r = self.s.get(f"https://{self.credentials['url']}/sites/{site}/_api/web/GetFileByServerRelativeUrl('{file}')/$value?binaryStringResponseBody=false")

        if file.endswith('.xlsx'):
            toread = io.BytesIO()
            toread.write(r.content)
            toread.seek(0)
            rows_to_skip = list(range(0, skip_lines))
            excelDataFrame = pandas.read_excel(toread,sheet_name=sheet, skiprows=rows_to_skip, index_col=1)
            csv = excelDataFrame.to_csv()
            return csv

        elif file.endswith('.csv'):
            return r.text

        return ''

    def get_file_timestamp(self,f):
        return datetime.strptime(f['TimeCreated'], "%Y-%m-%dT%H:%M:%SZ")

    def get_files_by_folder(self, site, folder, regex, loaded_files):
        r = self.s.get(f"https://{self.credentials['url']}/sites/{site}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files")
        
        j = json.loads(r.text)

        files_matched = []

        files = j['d']['results']

        files.sort(key=self.get_file_timestamp, reverse=True)

        for x in files:
            if re.match(regex, x['ServerRelativeUrl']):

                # Check if file name already exists among the already loaded files
                if x['Name'].split('.')[0] not in loaded_files: 

                    file = {}
                    file['file_path'] = x['ServerRelativeUrl']
                    file['timestamp'] = x['TimeCreated']

                    files_matched.append(file)

        return files_matched