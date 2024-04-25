import requests
import arseeding

SDK = 'ao.py'
MU = 'https://mu.ao-testnet.xyz'
CU = 'https://cu.ao-testnet.xyz'
SCHEDULER = '_GQ33BkPtZrqxA84vM8Zk-N2aO0toNNu_C-l-rawrBA'

def send_message(singer, pid, anchor, tags, data='', mu=MU):
    default_tags = {
        'Data-Protocol': 'ao',
        'Variant': 'ao.TN.1',
        'Type': 'Message',
        'SDK': SDK,
    }
    default_tags.update(tags)
    b = arseeding.BundleItem(singer, pid, anchor, default_tags, data)
    return b.id, requests.post(mu, data=b.binary, headers={'Content-Type': 'application/octet-stream'}).json()

def dry_run(signer, pid ,anchor, tags, data='', cu=CU):
    default_tags = {
        'Data-Protocol': 'ao',
        'Variant': 'ao.TN.1',
        'Type': 'Message',
        'SDK': SDK,
    }
    default_tags.update(tags)
    tags = [{'name':k, 'value':v} for k,v in tags.items()]
    url = '%s/dry-run?process-id=%s' % (cu, pid)
    payload = {
        'Target': pid,
        'Owner': signer.address,
        'Anchor': anchor,
        'Data': data,
        'Tags': tags,
    }
    print(payload)
    return requests.post(url, json=payload).json()
    
def spawn_process(singer, module, anchor, tags, data='', mu=MU, scheduler=SCHEDULER):
    default_tags = {
        'Data-Protocol': 'ao',
        'Variant': 'ao.TN.1',
        'Type': 'Process',
        'Scheduler':scheduler,
        'Module':module,
        'SDK': SDK,
    }
    default_tags.update(tags)
    b = arseeding.BundleItem(singer, '', anchor, default_tags, data)
    return b.id, requests.post(mu, data=b.binary, headers={'Content-Type': 'application/octet-stream'}).json()

def get_result(pid, message_id, cu=CU):
    return requests.get(f'{cu}/result/{message_id}?process-id={pid}').json()

def send_and_get(singer, pid, anchor, tags, data='', mu=MU, cu=CU):
    mid, _ = send_message(singer, pid, anchor, tags, data, mu)
    return get_result(pid, mid, cu)
       