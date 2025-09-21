{% from 's3.j2' import responsive_s3_img %}
---
Title: Blackholing tracking domains by running Pihole as a DHCP server
Date: 2025-08-24
Category: Programming
Description:  My new ISP provided router does not allow me to change the advertised DNS server IP. By running <a href=https://pi-hole.net>pihole</a> with a DHCP server, I can get around this limitation to ensure that tracking domains are blackholed for everyone at home.
Summary: My new ISP provided router does not allow me to change the advertised DNS server IP. By running <a href="https://pi-hole.net/">pihole</a> with a DHCP server, I can get around this limitation to ensure that tracking domains are blackholed for everyone at home.
Tags: DIY
Keywords: Pihole, adblock, self-hosting
---


My new ISP provided router does not allow me to change the advertised DNS server IP. This allows them to [DNS-lie](https://labs.ripe.net/author/stephane_bortzmeyer/dns-censorship-dns-lies-as-seen-by-ripe-atlas/) about certain domains the French government does not want you to visit.

For example, let's have a look at what both the Orange (`80.10.246.2`) and Coudflare DNS servers (`1.1.1.1`) have to say about The Pirate Bay.

```bash
~ ❯ dig +short thepiratebay.org @80.10.246.2
127.0.0.1  # well, that's a lie.
~ ❯ dig +short thepiratebay.org @1.1.1.1
162.159.137.6
162.159.136.6
```

While I don't particularly enjoy being lied to for my own good, I actually wanted to use the same technique to block ads and tracking domains from being resolved within my LAN in the first place, using [pihole](https://pi-hole.net/). However, that involves being able to manually set the IP address of the DNS server in the router's DHCP settings. This not being an option, I could go around this by _disabling_ the DHCP server from the ISP router, and enabling it [in pihole](https://docs.pi-hole.net/docker/DHCP/) instead.

The first thing I need to do is make sure that the RaspberryPi on which pihole will run gets a statically assigned IP, instead of getting it via DHCP. This guarantees the stability of the DNS server IP.

```bash
br@retropie:~ $ cat /etc/network/interfaces.d/eth0
auto eth0
iface eth0 inet static
  address 192.168.1.17
  netmask 255.255.255.0
  gateway 192.168.1.1
  dns-nameservers 1.1.1.1
  dns-nameservers 8.8.8.8
br@retropie:~ $ sudo systemctl restart networking.service
br@retropie:~ $ ifconfig eth0
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.17  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 2a01:cb14:189b:5a00:ba27:ebff:feed:b950  prefixlen 64  scopeid 0x0<global>
```

I then run [`cloudflared`](https://docs.pi-hole.net/guides/dns/cloudflared/), acting as a DNS proxy to some upstream resolver over HTTPs. Instead of relying on the Cloudflare or Google upstreams, as is common, I decided to integrate with [Wikimedia DNS](https://meta.wikimedia.org/wiki/Wikimedia_DNS). I'm employed by the Foundation, and know and trust the engineers in charge of the service.

`cloudflared` runs via systemd and listens on `127.0.0.1:5053`:

```bash
br@retropie:~ $ sudo systemctl cat cloudflared.service
# /etc/systemd/system/cloudflared.service
[Unit]
Description=cloudflared DNS over HTTPS proxy
After=syslog.target network-online.target

[Service]
Type=simple
User=cloudflared
EnvironmentFile=/etc/default/cloudflared
ExecStart=/usr/local/bin/cloudflared proxy-dns --address 127.0.0.1 --port 5053 --upstream https://wikimedia-dns.org/dns-query
Restart=always
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
```

With that setup, I can then deploy `pihole` with the DNS server IP advertised as its own (`192.168.1.17` in my case), through the [DHCP option 6 field](https://efficientip.com/glossary/dhcp-option/).

```bash
br@retropie:~ $ cat /etc/default/pihole
FTLCONF_database_maxDBdays=30
FTLCONF_dhcp_active=True
FTLCONF_dhcp_end=192.168.1.150
FTLCONF_dhcp_start=192.168.1.10
FTLCONF_dns_dnssec=false
FTLCONF_dns_listeningMode=ALL
FTLCONF_dns_upstreams=127.0.0.1#5053  # cloudflared
FTLCONF_misc_dnsmasq_lines=dhcp-option=6,192.168.1.17  # advertise the DNS server IP as itself
FTLCONF_webserver_api_password=[REDACTED]
FTLCONF_webserver_port=80
PIHOLE_GID=1000
PIHOLE_UID=1000
TZ=UTC
br@retropie:~ $ docker run \
  --name pihole \
  --detach \
  --env-file /etc/default/pihole \
  --volume /etc/pihole:/etc/pihole/ \
  --network host \ #  because DHCP works by broadcasting on the network
  --cap-add NET_ADMIN \
  --cap-add CAP_SYS_TIME \
  --cap-add CAP_SYS_NICE \
  pihole/pihole
```

With that in place, I can check that the DNS server IP is indeed advertised as expected.

{{ responsive_s3_img("pihole-dhcp", "wifi-dhcp-dns") }}

After a couple of days of that setup running, I can see that about 5% of my DNS traffic is being blackholed, thus benefiting everyone at home. The rest of the traffic is resolved via a privacy-respecting DNS server.

{{ responsive_s3_img("pihole-dhcp", "pihole-stats") }}

And as an extra, the French government gets to stay out of my buisness as well.

```bash
~ ❯ dig +short thepiratebay.org
162.159.136.6
162.159.137.6
```
