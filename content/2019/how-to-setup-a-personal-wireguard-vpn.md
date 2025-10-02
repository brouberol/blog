{% from 's3.j2' import s3_img %}
---
Title: How to setup a personal wireguard VPN
Date: 2019-12-11
Category: Programming
Description: How to setup a wireguard VPN to stay safe when traveling
Summary: This article will provide guidance about how to setup a Wireguard VPN between a server and your phone, allowing you to avoid being snooped on while you travel.
Tags: DIY
Image: https://www.cactusvpn.com/wp-content/uploads/2019/02/what-is-wireguard.gif
---

My work takes me to the United-States multiple times a year, and I've never been comfortable using the hotel Wi-Fi, or even my company VPN for that matter, when I'm there. I want to be assured that what I do online is my business and my business alone.

I had heard about [Wireguard](https://wireguard.com) multiple times, how performant and simple it was compared to OpenVPN (I'd like to have a talk with whomever came up with the OpenVPN config file...). I decided to jump in and give it a try. The idea was to setup a VPN access point on my VPS, hosted in Paris, to which I could connect when I travel.

---

## Installing wireguard

I followed Wireguard's [official install instructions](https://www.wireguard.com/install). However, I also needed to install the headers files for the kernel I was running so that `dkms` could compile the `wiregard` kernel module.

```console
% apt-get install linux-headers-$(uname -r)
% add-apt-repository ppa:wireguard/wireguard
% apt-get update
% apt-get install wireguard
```

If everything is going according to plan, you should see the `wireguard` kernel module being compiled by `dkms` at install time:

```console
...
DKMS: build completed.wireguard.ko:
Running module version sanity check.
 - Original module
   - No original module exists within this kernel
 - Installation
   - Installing to /lib/modules/X.Y.Z-ABC-generic/updates/dkms/
...
```

At that point, you should be able to see the module in the `lsmod` output and load it.

```console
% lsmod | grep wireguard
wireguard             204800  0
ip6_udp_tunnel         16384  1 wireguard
udp_tunnel             16384  1 wireguard
% modprobe wireguard
```


## Configuring the server peer

First off, we create the server `wireguard` peer's public and private keys.

```console
% cd /etc/wireguard
% umask 077  # disable public access
% wg genkey | tee privatekey | wg pubkey > publickey
```

We now configure the server peer, assuming that the VPS public network interface is `ens2`. We'll use the `192.168.2.0/24` subnet for all `wireguard`-related addresses, and assign `192.168.2.1` IP to the server peer.

```console
% cat <<EOF > /etc/wireguard/wg0.conf
[Interface]
# The IP assigned to the wg0 interface
Address = 192.168.2.1/24

# The port wireguard will listen on
ListenPort = <public port>

# The private key used by the local peer
PrivateKey = $(cat /etc/wireguard/privatekey)

# Accept traffic to the wg0 interface and allow NATing traffic from ens2 to wg0
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o ens2 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o ens2 -j MASQUERADE

EOF
% rm /etc/wireguard/privatekey
```

We also need to authorize UDP traffic on the `<public port>` port.

```console
% iptables -i ens2 -p udp --dport <public port> -j ACCEPT
```

Once that's done, we're now able to use `wg-quick` to setup the `wg0` network interface, as well as the `MASQUERADE` iptables rules that will NAT the traffic between the public `ens2` interface to `wg0`. We can actually use systemd for that, as we're assured that the `wg0` interface is re-created in case of a reboot.

```console
% systemctl start wg-quick@wg0
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 192.168.2.1/24 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o ens2 -j MASQUERADE

% systemctl enable wg-quick@wg0
Created symlink from /etc/systemd/system/multi-user.target.wants/wg-quick@wg0.service to /lib/systemd/system/wg-quick@.service.
```


## Configuring the phone peer

I use the Wireguard [Android app](https://play.google.com/store/apps/details?id=com.wireguard.android), and assign the `192.168.2.2/32` address to my phone, as well as add the server peer details (as Wireguard is a point-to-point VPN without a client/server architecture).

The server peer public key is set to the content of the remote `/etc/wireguard/publickey` file, on my VPS. As I want to route all my phone traffic through `wireguard`, I set the `Allowed IPs` field to `0.0.0.0/0`, and the peer endpoint to `<server public ens2 IP>:<public port>`.

{{ s3_img("wireguard", "android-wg.jpg", "screenshot") }}

## Authorizing the phone peer
After having generated a public key for the phone peer, we also need to authorize it on the server peer and restart `wireguard`.

```console
% cat <<EOF >> /etc/wireguard/wg0.conf

[Peer]
# Phone peer
PublicKey = <phone peer public key generated in app>
AllowedIPs = 192.168.2.2/32
EOF
% systemctl restart wg-quick@wg0
```

## Testing the whole thing

My phone disconnected from the server `wireguard` peer, I'm now able to inspect the state of the `wg0` server network interface:

```console
% ifconfig wg0
wg0       Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
          inet addr:192.168.2.1  P-t-P:192.168.2.1  Mask:255.255.255.0
          UP POINTOPOINT RUNNING NOARP  MTU:1420  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

I then connect my phone to the server peer, open a random webpage, and _voila_, we can see traffic going through the server `wg0` interface.

```console
$ ifconfig wg0
wg0       Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
          inet addr:192.168.2.1  P-t-P:192.168.2.1  Mask:255.255.255.0
          UP POINTOPOINT RUNNING NOARP  MTU:1420  Metric:1
          RX packets:4084 errors:0 dropped:132 overruns:0 frame:0
          TX packets:4895 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:452436 (452.4 KB)  TX bytes:2954188 (2.9 MB)
```

A quick `tcpdump` shows that the data flowing to `wg0` is indeed encrypted.
```console
$ tcpdump -i wg0 -vv -c 100 -X
tcpdump: listening on wg0, link-type RAW (Raw IP), capture size 262144 bytes
15:14:05.096356 IP (tos 0x0, ttl 105, id 47301, offset 0, flags [none], proto TCP (6), length 332)
    wq-in-f188.1e100.net.5228 > 192.168.2.2.46641: Flags [P.], cksum 0x8308 (correct), seq 1867855144:1867855424, ack 229885280, win 253, options [nop,nop,TS val 426814177 ecr 2017832], length 280
    0x0000:  4500 014c b8c5 0000 6906 fe02 4a7d 8cbc  E..L....i...J}..
    0x0010:  c0a8 0202 146c b631 6f55 3528 0db3 c560  .....l.1oU5(...`
    0x0020:  8018 00fd 8308 0000 0101 080a 1970 aae1  .............p..
    0x0030:  001e ca28 1703 0301 13e7 c1f4 5089 ed04  ...(........P...
    0x0040:  aba6 ef67 2cbe a7b3 f0cc 02d0 caaa d675  ...g,..........u
...
```

I now have have a personal VPN I can use whenever I travel abroad.

---
Thanks to Thomas for being patient with me while answering networking questions at 11pm, and for proof-reading this article. Any remaining mistake is my own.
