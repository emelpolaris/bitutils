import bittensor as bt
import time
from fastapi import FastAPI
import argparse

app = FastAPI()

name_s58_emission_rank_old = {}
name_s58_emission_rank_new = {}
result = {}
my_hotkeys = {
    'JJhot': '5F97aEdNArw3eDrpsXqtukxgzoQT6yxiVArf4RiceNKGYh71', 'JJwarm': '5EboAn9c92EhYrU12Cp31EavaJ4PLroZiJfujwDyzhQqxL1K',
    'JJa': '5DCx43cgGoPUW8p8zMB7JzQzfsFRi2PRULdVYkdySjb88wRM', 'JJb': '5GRUxyJAowgfjj8Kj66vMqbY1DScMNu2YWvqfNZ5smzmZ5G7',
    'JJc': '5GYouwrtN6xkAunj3GQth1XWooUaGzoGhrDHk54SUp4G7fTn', 'JJd': '5DP8ZMw1YhYC6xgZa4UfLhQhkBXoXuzPwnNUAX9GkjPQrrEv',
    'JJe': '5FBf4z4EugbogeL32DX5d5KQZLwZmjWsQfXn9GtNGkc8JKmy', 'JJf': '5Cf18GoJRXz6EL5gWXdHbgZ37d1rKCZ6oxdAxZ9hJvSW8k6s',
    'JJg': '5Hfw3kGpMTP8YjGiBNHWk7vQ5tLrLDH4v8qCkmvMRmAUVjmc', 'JJh': '5DvpCQ7UhUKKUBHSeTkS2WX6RnkA8PeVAEQS2Y8KrkPVGdaA',
    'JJi': '5CFZKUrqJZS1GiEzknYv41rQDVX6EuctqgJDp1B7gZRpk1xT', 'JJj': '5HH7RFA4m7e8xvnKhUFBsqj2QRyypD9YAv38FUqE596VRFWs',
    'JJk': '5HK1f5ntzXYeSWEgEGexj4JGnMv9WyUXKJ3p1a64LGJ3Ptja', 'Za': '5FvWSyLNzHBkW8ngfY6TWxGJMmW1sci9zkguadxDBsJCJqEr',
    'Zb': '5DV7ykzp1ianL33nvgj5bEufe77asDzUDMqqHjrhUCtcACFZ', 'Zc': '5F2Hd7LmyJ4Q1c1ATQ1UP6TErZTiCRcjRMiExptHC7BwN7XW',
    'Zd': '5CFW1vhgcsHU4AG4nqArqc6omQsAJWJqe41aHNpWUHPxQEpa', 'Ze': '5G9JHYtFiyU7dCM4HY2S3WnYgWhhGBq7MKdN59DnyhuvXa74',
    'Zf': '5EHkZPvGjy78PZ7jDQDHW5HqMJNq65fqgRT8x7BSmKae6Pdg', 'Zg': '5GNTpdkRCFNG4qadYa9jbPVgcGKFhx3RK7ZEJPGYZWuUrw4C',
    'Zh': '5HNgG2DaP5jeHdRacLKCz2m2r6F5tQnyNy7uNz7ESzZZ6u87', 'TTa' : '5DCUmErSWGmLAyvGDJqqZZenCVSueAyBpWoYPQ38znRNagFu',
    'TTb' : '5DJ62zL2Vs2Lb6tdGqAy2wk7oq7sWzvmHvtxiSxqwq6EDktk', 'TTc' : '5F2CidPunAY6DY3PLFS4mAKkAYKbxA428PwZ8546ruLfkGMd',
    'TTd' : '5DtPa5A7VQ4h99RonVajkh1hKv8DkTTAiG14gJCuwYKShsC7', 'TTe' : '5CBA4DgGXfKUeHLJeHgo6SSHdmyLiNTfAF8TifsgRo7bYkBM',
    'TTf' : '5CZyJ7D1CZ1pvDFAXJr2YRjRK5Y4XbmSwUMMfyWkNY6otUix', 'TTg' : '5GYtaFxVgnoEpo1mVSYeBs8gCCca8ptN6oszJ7quDpDBE5sn',
    'TTh' : '5CUeakYTrjoQMFgdRfYc5vwJ4ZZVriPF2RGZdnVhBFyM6GZC', 'TTi' : '5FRCkb2CJxUw9mDhX25TrbftYCEvcZE1BTugCU7EkNgRCzHR',
    'TTj' : '5HiaLLDs16yPMnSzC46G6Q9SwTVkjkWDzJg1vpJJevZXusfw', 'TTk' : '5FcARLVRrVWw9GA2NEE4x4XRDfXdMgwRahKasD2Kx7kyVeLf',
    'TTl' : '5EcEk9FCMo7Y8mGUeciSbHjVHbDfCrCUkZkumfnc83VAuRPf', 'TTm' : '5CULoekifcMWh7vK9VVvg6a1KB9hqcUokon5b8Z6z8Jd85vR',
    'TTn' : '5GKoPvsEmw9HRRMH1d1p5yNjHAeq1C6f8TBb7QChwbwMbJoy', 'TTo' : '5G9y3wdnsASwd5xMYipLnk9Qj46JwbywyyTpNFvMGb8bXdGX', 
}

@app.get("/")
def show():
    return "hello world"
def fetch(netuid: int):
    global name_s58_emission_rank_old, name_s58_emission_rank_new, result

    metagraph = bt.subtensor('finney').metagraph(netuid=netuid)
    emissions = metagraph.E.tolist()
    hotkeys = metagraph.hotkeys


    emission_ranks = []
    for emission in emissions:
        rank = sorted(emissions).index(emission) + 1
        emission_ranks.append([emission, rank])
    # print(emissions)
    # print(emission_ranks)

    hotkey_emission_ranks = {}
    for i in range(len(emissions)):
        hotkey_emission_ranks[hotkeys[i]] = [emission_ranks[i][0], emission_ranks[i][1]]
    # print(hotkey_emission_ranks)

    name_s58_emission_rank_new = {}
    for key, val in my_hotkeys.items():
        if val in hotkey_emission_ranks:
            name_s58_emission_rank_new[key] = [val, hotkey_emission_ranks[val][0], hotkey_emission_ranks[val][1]]
    
    print(name_s58_emission_rank_new)
    result = {}
    for key, val in name_s58_emission_rank_new.items():
        if key not in name_s58_emission_rank_old:
            print(f"New miner registered: {key}")
            result[key] = [name_s58_emission_rank_new[key][2], '-']    
            continue
        rank_diff = name_s58_emission_rank_new[key][2] - name_s58_emission_rank_old[key][2]
        result[key] = [name_s58_emission_rank_new[key][2], rank_diff]
    print(result)
    try:
        log_file = open('logs.txt', 'a')
    except FileNotFoundError:
        log_file = open('logs.txt', 'w')
    log_file.write('------------\n')
    log_file.write(str(result))
    log_file.close()
    name_s58_emission_rank_old = name_s58_emission_rank_new

if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run(app, host="24.83.20.198", port=80)
    argp = argparse.ArgumentParser(description="config")
    argp.add_argument("--netuid", type=int, default=31)
    args  = argp.parse_args()
    netuid = args.netuid
    while True:
        fetch(netuid)
        time.sleep(600)
