from retry import retry
# from tqdm import tqdm
import requests


@retry(tries=3, delay=3, backoff=2)
def raw_request(raw_url):
    response = requests.get(raw_url, timeout=5)
    if response.status_code != 200:
        print('error', response.text)
    return response.json()


@retry(tries=3, delay=3, backoff=2)
def raw_request_f2pool(raw_url):
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = requests.get(raw_url, headers=headers, timeout=5)
    if response.status_code != 200:
        print('error')
    return response.json()


def data_antpool(url_hs: str, url_machines: str, access_key, user_id):
    response_hs = raw_request(url_hs.format(page_num=1, page_size=10, access_key=access_key, user_id=user_id))
    response_machines = raw_request(url_machines.format(page_num=1, page_size=10, access_key=access_key, user_id=user_id))
    hs_now = float(response_hs['data']['hsNow'])
    count_online = int(response_machines['data']['workerStatus']['onlineWorkerNum'])
    count_total = int(response_machines['data']['workerStatus']['totalWorkerNum'])
    return [count_online, hs_now, count_total]


def avg_hs(all_hs):
    return sum(all_hs) / len(all_hs)


def data_f2pool(url: str, access_key):
    response = raw_request_f2pool(url.format(access_key=access_key))
    count_online = response['originData']['tagsOverview'][0]['online']
    count_total = response['originData']['tagsOverview'][0]['total']
    hs_now = ('{:.2f}'.format(float(response['originData']['summary']['hash_rate']) / 1000000000000000))
    return [count_online, hs_now, count_total]


def data_binance(url: str, access_key):
    response = raw_request(url.format(access_key=access_key))
    hs_now = response['data']['hashRate']
    count_online = response['data']['validNum']
    return [count_online, hs_now]