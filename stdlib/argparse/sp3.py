#!/usr/bin/env python3
"""
Mualif: Python & Network Script (Pro Version)
Tavsif: Python'ning 'ipaddress' moduli imkoniyatlaridan to'liq foydalangan holda 
        IPv4 tarmoqlarini kengaytirilgan tahlil qilish va xossalarini tekshirish scripti.

Misollar:
    # Barcha ma'lumotlar va xossalar (default):
    python3 ipcalc_pro.py 192.168.1.0/24

    # Faqat tarmoq manzili:
    python3 ipcalc_pro.py 10.0.0.0/8 --network-address

    # Tarmoq xossalarini tekshirish (masalan, private yoki loopback ekanligini bilish):
    python3 ipcalc_pro.py 127.0.0.1/32 --properties
"""

import argparse
import ipaddress
import sys


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Kengaytirilgan IPv4 tarmoq va IP tahlil qilish vositasi.\n"
            "ipaddress kutubxonasidagi barcha xossalar (private, loopback, multicast va h.k.) "
            "va hisob-kitoblarni qo'llab-quvvatlaydi."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Qo'shimcha misollar:\n"
            "  %(prog)s 192.168.1.10/24\n"
            "  %(prog)s 10.0.0.5/8 --properties\n"
            "  %(prog)s 192.168.1.0/24 -f\n"
            "  %(prog)s 224.0.0.1/4 -m\n"
        ),
    )

    # Majburiy pozitsion argument
    parser.add_argument(
        "ipv4",
        type=str,
        help="IPv4 tarmoq yoki IP manzil (masalan: 192.168.1.0/24 yoki 127.0.0.1)",
    )

    # O'zaro istisno qiluvchi bayroqlar guruhi (Faqat bittasini tanlash mumkin)
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-n",
        "--network-address",
        action="store_true",
        help="Faqat tarmoq manzilini chiqarish",
    )
    group.add_argument(
        "-m",
        "--network-mask",
        action="store_true",
        help="Faqat subnet niqobini (Netmask) chiqarish",
    )
    group.add_argument(
        "-b",
        "--broadcast-address",
        action="store_true",
        help="Faqat broadcast manzilini chiqarish",
    )
    group.add_argument(
        "-p",
        "--prefix",
        action="store_true",
        help="Faqat prefix uzunligini (masalan: 24) chiqarish",
    )
    group.add_argument(
        "-w",
        "--wildcard",
        action="store_true",
        help="Faqat wildcard maskasini chiqarish",
    )
    group.add_argument(
        "-f",
        "--first-host",
        action="store_true",
        help="Tarmoqdagi birinchi foydalaniladigan IP manzilni chiqarish",
    )
    group.add_argument(
        "-l",
        "--last-host",
        action="store_true",
        help="Tarmoqdagi oxirgi foydalaniladigan IP manzilni chiqarish",
    )
    group.add_argument(
        "--host-count",
        action="store_true",
        help="Tarmoqdagi mavjud xostlar (host) sonini chiqarish",
    )
    group.add_argument(
        "--properties",
        action="none_or_all" if hasattr(argparse, "none_or_all") else "store_true",
        help="IP/Tarmoqning barcha xossalarini (private, loopback, multicast va h.k.) chiqarish",
    )

    # Agar argument berilmagan bo'lsa, avtomatik help chiqarish
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        # strict=False orqali host qismidagi ortiqcha bitlar xato bermasligini ta'minlaymiz
        network = ipaddress.ip_network(args.ipv4, strict=False)
        
        # Alohida bayroqlar tekshiruvi
        if args.network_address:
            print(network.network_address)
        elif args.network_mask:
            print(network.netmask)
        elif args.broadcast_address:
            print(network.broadcast_address)
        elif args.prefix:
            print(network.prefixlen)
        elif args.wildcard:
            print(network.hostmask)
        elif args.first_host:
            # Agar tarmoq 30 yoki 32-bit bo'lsa hostlar farq qilishi mumkin
            hosts = list(network.hosts())
            print(hosts[0] if hosts else "Mavjud emas")
        elif args.last_host:
            hosts = list(network.hosts())
            print(hosts[-1] if hosts else "Mavjud emas")
        elif args.host_count:
            # Haqiqiy foydalanish mumkin bo'lgan hostlar soni (tarmoq va broadcastni ayirib tashlaganda)
            num_hosts = max(0, network.num_addresses - 2) if network.prefixlen < 31 else network.num_addresses
            print(num_hosts)
        elif args.properties:
            # ipaddress kutubxonasining barcha asosiy boolean xossalari
            print(f"{'Address:':<25} {network.network_address}")
            print(f"{'Is Private:':<25} {network.is_private}")
            print(f"{'Is Loopback:':<25} {network.is_loopback}")
            print(f"{'Is Multicast:':<25} {network.is_multicast}")
            print(f"{'Is Global:':<25} {network.is_global}")
            print(f"{'Is Unspecified:':<25} {network.is_unspecified}")
            print(f"{'Is Reserved:':<25} {network.is_reserved}")
            print(f"{'Is Link Local:':<25} {network.is_link_local}")
        else:
            # Default holatda ipcalc uslubidagi to'liq hisobot va xossalar jamlanmasi
            hosts = list(network.hosts())
            first_h = hosts[0] if hosts else "N/A"
            last_h = hosts[-1] if hosts else "N/A"
            usable_hosts = max(0, network.num_addresses - 2) if network.prefixlen < 31 else network.num_addresses

            print("=" * 45)
            print(f"{'IPv4 NETWORK INFORMATION':^45}")
            print("=" * 45)
            print(f"{'Address:':<20} {network.network_address}")
            print(f"{'Netmask:':<20} {network.netmask}")
            print(f"{'Wildcard:':<20} {network.hostmask}")
            print(f"{'Network:':<20} {network.with_prefixlen}")
            print(f"{'Broadcast:':<20} {network.broadcast_address}")
            print(f"{'First Host:':<20} {first_h}")
            print(f"{'Last Host:':<20} {last_h}")
            print(f"{'Total Addresses:':<20} {network.num_addresses}")
            print(f"{'Usable Hosts:':<20} {usable_hosts}")
            print("-" * 45)
            print(f"{'IP PROPERTIES (ipaddress module)':^45}")
            print("-" * 45)
            print(f"{'Private:':<20} {network.is_private}")
            print(f"{'Loopback:':<20} {network.is_loopback}")
            print(f"{'Multicast:':<20} {network.is_multicast}")
            print(f"{'Global:':<20} {network.is_global}")
            print(f"{'Reserved:':<20} {network.is_reserved}")
            print(f"{'Link Local:':<20} {network.is_link_local}")
            print("=" * 45)

    except ValueError as e:
        print(f"Xatolik: Noto'g'ri format kiritildi -> {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()