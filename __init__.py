import requests
import arseeding

MU = 'https://mu.ao-testnet.xyz'
CU = 'https://cu.ao-testnet.xyz'

def send_message(singer, process_id, anchor, tags, data, mu=MU):
    default_tags = {
        'Data-Protocol': 'ao',
        'Variant': 'ao.TN.1',
        'Type': 'Message',
        'SDK': 'ao.py',
    }
    default_tags.update(tags)
    b = arseeding.BundleItem(singer, process_id, anchor, default_tags, data)
    return b.id, requests.post(mu, data=b.binary, headers={'Content-Type': 'application/octet-stream'}).json()

def get_result(process_id, message_id, cu=CU):
    return requests.get(f'{cu}/result/{message_id}?process-id={process_id}').json()
    