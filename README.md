# home-cron
This is a docker image I use to run scheduled tasks at home on my Raspberry Pi.

- `update-home-dns.py` - this monitors the connected network's public IP address and ensures it matches the value of a specific A record in a CloudFlare DNS zone - DIY dynamic DNS in other words :smile:
