import requests
import sys

def get_subdomains(domain):
    """Fetch subdomains from crt.sh"""
    print(f"[*] Searching subdomains for {domain}...")
    
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        
        subdomains = set()
        for entry in data:
            names = entry.get('name_value', '').split('\n')
            for name in names:
                name = name.strip().lower()
                if name.startswith('*.'):
                    name = name[2:]
                if name:
                    subdomains.add(name)
        
        return subdomains
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return set()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <domain>")
        print("Example: python3 script.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    subdomains = get_subdomains(domain)
    
    if subdomains:
        print(f"\n[+] Found {len(subdomains)} subdomains:\n")
        for sub in sorted(subdomains):
            print(sub)
        
        # Save to file
        filename = f"{domain}_subdomains.txt"
        with open(filename, 'w') as f:
            f.write('\n'.join(sorted(subdomains)))
        print(f"\n[+] Saved to {filename}")
    else:
        print("[!] No subdomains found")

if __name__ == "__main__":
    main()