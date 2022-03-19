import requests

base_url = "http://fdac-125-227-128-246.ngrok.io/api/status"

def update_status(name, field, status):
    requests.get(f'{base_url}/{name}/{field}/{status}')

update_status('BIN_1', "CanFull", "true")