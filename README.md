
# DNS Resolver Script for Cloudflare unmasking

This DNS resolver script checks a domain against a range of DNS servers specified by a CIDR, potentially unmasking Cloudflare-protected domains.

## Features

- Resolves domain names using a specified range of DNS servers
- Generates IP addresses from a given CIDR range
- Utilizes multithreading for efficient DNS resolution
- Provides command-line arguments for flexibility and ease of use

## Installation

To install the required dependencies, run:

```sh
pip install dnspython
```

## How-To

1. Navigate to [dnsdumpster.com](https://dnsdumpster.com/) and check if there is a subdomain of the target domain that is not behind Cloudflare.
2. Copy the IP address of the uncovered subdomain.
3. Navigate to [hackertarget.com/as-ip-lookup/](https://hackertarget.com/as-ip-lookup/) and paste the IP address to find the "AS Range".
4. Run the script by providing the domain name and the CIDR (AS Range) and wait for it to finish.

## Syntax Example

To run the script, use the following command:

```sh
python script.py --domain example.com --cidr 192.168.1.0/24
```

## Detailed Explanation

When hosting websites in managed environments, such as CPanel and Plesk, there is typically a port 53 open by default. When these environments are asked "where is that site," they often prefer their own records over Cloudflare's and will respond by looking up their own records. The key is to find the correct DNS server, which can lead to unmasking a Cloudflare-protected domain. This script aids in identifying such DNS servers by checking a domain against a specified range of DNS servers.

---

By following the steps above, you can effectively use this script to potentially unmask domains protected by Cloudflare, leveraging the DNS records available in managed hosting environments.
