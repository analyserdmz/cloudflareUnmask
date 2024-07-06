import dns.resolver
import dns.exception
import ipaddress
import threading
import queue
import argparse

def resolve_domain(domain, server, result_queue):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [str(server)]
    resolver.lifetime = 1
    try:
        answer = resolver.resolve(domain)
        for rdata in answer:
            result_queue.put((server, rdata.to_text()))
            return
    except dns.exception.DNSException:
        pass
    result_queue.put((server, None))

def check_servers(domain, servers):
    result_queue = queue.Queue()
    threads = []

    for server in servers:
        thread = threading.Thread(target=resolve_domain, args=(domain, server, result_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while not result_queue.empty():
        server, result = result_queue.get()
        if result:
            return server, result

    return None, None

def generate_ips_from_cidr(cidr):
    return ipaddress.ip_network(cidr).hosts()

def main():
    parser = argparse.ArgumentParser(description="DNS resolver that checks a domain against a range of DNS servers specified by a CIDR, potentially unmasking Cloudflare-protected domains.")
    parser.add_argument('--domain', required=True, help="The domain name to resolve.")
    parser.add_argument('--cidr', required=True, help="The CIDR range to generate DNS server IP addresses from.")
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    args = parser.parse_args()

    domain = args.domain
    cidr = args.cidr

    servers = generate_ips_from_cidr(cidr)
    server, result = check_servers(domain, servers)

    if server and result:
        print(f"Domain {domain} resolved to {result} by DNS server {server}")
    else:
        print(f"Domain {domain} could not be resolved by any DNS server in the CIDR range {cidr}")

if __name__ == "__main__":
    main()
