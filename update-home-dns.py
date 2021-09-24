from datetime import datetime
from re import M
import CloudFlare
import ipaddress
from CloudFlare import cloudflare
import requests

def get_host_zone_name(host_name: str) -> str:
    return host_name.split(".", 1)[1]

def get_cf_dns_zone_id(cf: CloudFlare.CloudFlare, host_name: str) -> str:
    try:
        zone_name = get_host_zone_name(host_name)
        zones = cf.zones.get(params={'name':zone_name})
        if (len(zones) != 1):
            raise Exception(f'/zones.get - returned more or less than one zone: {len(zones)}')
        zone = zones[0]
        return zone['id']
    except Exception as e:
        exit(f'Unable to retrieve DNS zone {zone_name} from CloudFlare API: {e}')

def get_cf_dns_record(cf: CloudFlare, zone_id: str, host_name: str) -> ipaddress.IPv4Address:
    try:
        records = cf.zones.dns_records.get(zone_id, params={'name':host_name})
        if (len(records) != 1):
            raise Exception(f'/dns_records.get - %s - returned more or less than one zone: {len(records)}')
        record = records[0]
        return record
    except Exception as e:
        exit(f'Unable to retrieve DNS record {host_name} from CloudFlare API: {e}')

def get_public_ip() -> ipaddress.IPv4Address:
    url = 'http://ifconfig.me/ip'
    address = requests.get(url).text
    log(f'Current public IP address is {address}')
    return ipaddress.ip_address(address)

def update_dns_record(cf: CloudFlare, zone_id: str, old_dns_record: object, new_ip: ipaddress.IPv4Address):
    try:
        host_name = old_dns_record['name']
        log(f'Updating DNS record {host_name} to {new_ip} via the CloudFlare API')
        new_dns_record = {
            'name':old_dns_record['name'],
            'type':'A',
            'content':str(new_ip),
            'proxied':old_dns_record['proxied']
        }
        new_dns_record = cf.zones.dns_records.put(zone_id, old_dns_record['id'], data=new_dns_record)
    except Exception as e:
        exit(f'Unable to update the DNS record {host_name} to {new_ip} via the CloudFlare API: {e}')

def log(message: str):
    now = datetime.now()
    print(f'{now} - {message}')


def main():
    host_name = 'ENTER HOSTNAME'
    cf = CloudFlare.CloudFlare(token='ENTER TOKEN')
    current_ip = get_public_ip()
    cf_dns_zone_id = get_cf_dns_zone_id(cf, host_name)
    cf_dns_record = get_cf_dns_record(cf, cf_dns_zone_id, host_name)
    cf_dns_record_ip = ipaddress.ip_address(cf_dns_record['content'])
    log(f'Current value of DNS record {host_name} is {cf_dns_record_ip}')
    
    if (current_ip != cf_dns_record_ip):
        update_dns_record(cf, cf_dns_zone_id, cf_dns_record, current_ip)
    else:
        print("No update required")

    
    

if __name__ == '__main__':
    main()