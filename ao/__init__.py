import requests
import arseeding

MU = 'https://mu.ao-testnet.xyz'
CU = 'https://cu.ao-testnet.xyz'

def send_message(singer, pid, anchor, tags, data='', mu=MU):
    default_tags = {
        'Data-Protocol': 'ao',
        'Variant': 'ao.TN.1',
        'Type': 'Message',
        'SDK': 'ao.py',
    }
    default_tags.update(tags)
    b = arseeding.BundleItem(singer, pid, anchor, default_tags, data)
    return b.id, requests.post(mu, data=b.binary, headers={'Content-Type': 'application/octet-stream'}).json()

def get_result(pid, message_id, cu=CU):
    return requests.get(f'{cu}/result/{message_id}?process-id={pid}').json()

def send_and_get(singer, pid, anchor, tags, data='', mu=MU, cu=CU):
    mid, _ = send_message(singer, pid, anchor, tags, data, mu)
    return get_result(pid, mid, cu)
       