import json
import os
import datetime
import random
from probe import NetworkProbe

def generate_proxies():
    provinces = [
        'he', 'sx', 'ln', 'jl', 'hl', 'js', 'zj', 'ah', 'fj', 'jx', 'sd', 'ha', 
        'hb', 'hn', 'gd', 'hi', 'sc', 'gz', 'yn', 'sn', 'gs', 'qh', 'nm', 'gx', 
        'xz', 'nx', 'xj', 'bj', 'tj', 'sh', 'cq'
    ]
    isps = {'cu': 'Unicom', 'cm': 'Mobile', 'ct': 'Telecom'}
    
    proxies = {'Telecom': [], 'Unicom': [], 'Mobile': []}
    
    for prov in provinces:
        for isp_code, isp_name in isps.items():
            # Construct the proxy URL
            url = f"http://{prov}-{isp_code}-v4.ip.zstaticcdn.com:80"
            proxies[isp_name].append(url)
    return proxies

def load_domains(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_history(history_file, result):
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            pass
    
    # Add timestamp to result if not present
    if 'timestamp' not in result:
        result['timestamp'] = str(datetime.datetime.now())
        
    history.append(result)
    start_index = max(0, len(history) - 200) # Keep 200 records
    
    with open(history_file, 'w') as f:
        json.dump(history[start_index:], f, indent=2)

def generate_readme(results, readme_file):
    # Use Beijing time for display (UTC+8)
    utc_now = datetime.datetime.utcnow()
    cst_now = utc_now + datetime.timedelta(hours=8)
    timestamp = cst_now.strftime("%Y-%m-%d %H:%M:%S (CST)")
    
    md = f"# Cloudflare 优选域名监控系统\n\n更新时间: {timestamp}\n\n"
    md += "| 域名 | 电信 | 联通 | 移动 | 状态 | 详情 |\n"
    md += "|---|---|---|---|---|---|\n"
    
    for r in results:
        domain = r['domain']
        ct = r['details']['Telecom']['latency']
        cu = r['details']['Unicom']['latency']
        cm = r['details']['Mobile']['latency']
        status = r['status']
        
        # Color coding
        status_icon = "🟢" if status == "优" else "🟡" if status == "良" else "🔴"
        
        # Formatting latency
        def fmt_lat(l): return "❌" if l > 5000 else f"{l}ms"
        
        md += f"| {domain} | {fmt_lat(ct)} | {fmt_lat(cu)} | {fmt_lat(cm)} | {status_icon} {status} | [历史](data/history.json) |\n"
        
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(md)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domains_file = os.path.join(base_dir, 'data', 'domains.txt')
    history_file = os.path.join(base_dir, 'data', 'history.json')
    readme_file = os.path.join(base_dir, 'README.md')
    
    domains = load_domains(domains_file)
    proxies = generate_proxies()
    probe = NetworkProbe()
    current_results = []
    
    print(f"Loaded {len(domains)} domains. Generated {sum(len(v) for v in proxies.values())} proxies.")
    
    for domain in domains:
        print(f"Monitoring {domain}...")
        domain_result = {'domain': domain, 'details': {}}
        total_latency = 0
        valid_count = 0
        
        for provider in ['Telecom', 'Unicom', 'Mobile']:
            # Pick a random proxy for this provider to avoid single point of failure
            # Try up to 3 times with different proxies if one fails
            provider_proxies = proxies.get(provider, [])
            random.shuffle(provider_proxies)
            
            best_res = {'latency': 9999, 'packet_loss': 100}
            
            # Try 3 random proxies
            for proxy in provider_proxies[:3]:
                print(f"  - Probing {provider} via {proxy}...")
                res = probe.ping(domain, provider, proxy)
                if res['status'] == 'success':
                    best_res = res
                    break # Success, move to next provider
                
            domain_result['details'][provider] = best_res
            if best_res['latency'] < 5000:
                total_latency += best_res['latency']
                valid_count += 1
                
        # Determine status
        if valid_count == 0:
            avg_latency = 9999
        else:
            avg_latency = total_latency / valid_count
            
        if avg_latency < 150 and valid_count == 3:
            status = "优"
        elif avg_latency < 250 and valid_count >= 2:
            status = "良"
        else:
            status = "差"
            
        domain_result['status'] = status
        current_results.append(domain_result)
        save_history(history_file, domain_result)
        
    generate_readme(current_results, readme_file)
    print("Monitor run complete.")

if __name__ == "__main__":
    main()
