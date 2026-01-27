import urllib.request
import urllib.error
import time
import socket
import random

class NetworkProbe:
    def __init__(self):
        self.providers = ['Telecom', 'Unicom', 'Mobile']
        # User Agent validation is sometimes needed
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def ping(self, domain, provider, proxy_url=None):
        """
        Ping a domain via a specific proxy (representing a provider).
        Returns dict with latency and status.
        """
        # Ensure domain has protocol
        target_url = domain if domain.startswith('http') else f"http://{domain}"
        
        start_time = time.time()
        
        try:
            opener = urllib.request.build_opener()
            if proxy_url:
                opener.add_handler(urllib.request.ProxyHandler({'http': proxy_url}))
            
            # Set timeout to 5 seconds
            request = urllib.request.Request(target_url, headers=self.headers)
            with opener.open(request, timeout=5) as response:
                # Read a bit to ensure connection
                _ = response.read(1024)
                
            latency = int((time.time() - start_time) * 1000)
            return {
                'latency': latency,
                'packet_loss': 0,
                'status': 'success',
                'proxy': proxy_url
            }
            
        except Exception as e:
            # If proxy fails or target is down
            return {
                'latency': 9999,
                'packet_loss': 100,
                'status': 'error',
                'error': str(e),
                'proxy': proxy_url
            }
