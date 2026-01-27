import json

provinces = [
    'he', 'sx', 'ln', 'jl', 'hl', 'js', 'zj', 'ah', 'fj', 'jx', 'sd', 'ha', 
    'hb', 'hn', 'gd', 'hi', 'sc', 'gz', 'yn', 'sn', 'gs', 'qh', 'nm', 'gx', 
    'xz', 'nx', 'xj', 'bj', 'tj', 'sh', 'cq'
]

isps = {
    'cu': 'Unicom',
    'cm': 'Mobile',
    'ct': 'Telecom'
}

proxies = {
    'Unicom': [],
    'Mobile': [],
    'Telecom': []
}

for prov in provinces:
    for isp_code, isp_name in isps.items():
        url = f"http://{prov}-{isp_code}-v4.ip.zstaticcdn.com:80"
        proxies[isp_name].append(url)

with open('data/proxies.json', 'w') as f:
    json.dump(proxies, f, indent=2)

print(f"Generated {sum(len(v) for v in proxies.values())} proxies.")
