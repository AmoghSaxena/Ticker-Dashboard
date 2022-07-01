"""
Created on 05-Sep-2019

@author: sumit-rathore
"""
from django.conf import settings
import requests


class CloudClient:

    @staticmethod
    def update_token():
        url = settings.DVP_HOST + "/dvp/auth/authenticate"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "email": settings.DVP_USERNAME,
            "password": settings.DVP_PASSWORD
        }
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            response = r.json()
            settings.DVP_TOKEN = response['data']['token']
            return True
        else:
            return False

    def make_get_request_stream(self, cloud_endpoint):
        url = cloud_endpoint
        headers = {
            'Authorization': 'Bearer ' + settings.DVP_TOKEN,
        }
        try:
            r = requests.get(url, headers=headers, stream=True)
            if r.status_code == 200:
                return r
            elif r.status_code == 401:
                if self.update_token():
                    return self.make_get_request(cloud_endpoint)
                else:
                    raise Exception("Username password are not correct in settings")
        except Exception as e:
            print(e)
            raise

    def make_get_request(self, cloud_endpoint, params=None):
        url = settings.DVP_HOST + cloud_endpoint
        self.update_token()
        headers = {
            'Authorization': 'Bearer ' + settings.DVP_TOKEN,
            'Content-Type': 'application/json'
        }
        try:

            if params:
                r = requests.get(url, headers=headers, params=params)
                print(r)
            else:
                r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return r
            elif r.status_code == 401:
                if self.update_token():
                    return self.make_get_request(cloud_endpoint, params=params)
                else:

                    raise Exception("Username password are not correct in settings")
            elif r.status_code == 404:
                raise Exception("Item not found")
            else:
                print(r)
                raise Exception("Error occured")
        except Exception as e:
            print(e)
            raise

    def make_post_request(self, data, cloud_endpoint):
        url = settings.DVP_HOST + cloud_endpoint
        headers = {
            'Authorization': 'Bearer ' + settings.DVP_TOKEN,
            'Content-Type': 'application/json'
        }
        try:
            r = requests.post(url, headers=headers, json=data)
            if r.status_code == 200:
                return r
            elif r.status_code == 401:
                if self.update_token():
                    return self.make_post_request(data, cloud_endpoint)
                else:
                    print(r)
                    raise Exception("Username password are not correct in settings")
            elif r.status_code == 404:
                raise Exception("Item not found")
        except Exception as e:
            print(e)
            raise
