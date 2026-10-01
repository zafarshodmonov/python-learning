#!/usr/bin/env python3
"""
Mualif: Python & Network Script
Tavsif: Berilgan IPv4 tarmoq manzili (CIDR formatida) bo'yicha tarmoq,
        subnet mask, broadcast va boshqa ma'lumotlarni ipcalc kabi chiqarib beradi.

Misollar:
    # Barcha ma'lumotlarni chiqarish (default):
    python3 ipcalc_lite.py 127.0.0.0/8

    # Faqat network addressni chiqarish:
    python3 ipcalc_lite.py 192.168.1.0/24 --network-address

    # Faqat subnet maskni chiqarish (-m qisqartmasi):
    python3 ipcalc_lite.py 10.0.0.0/16 -m
"""

import argparse
import ipaddress
import sys


def main():
    # Argumentlar parserini yaratamiz
    parser = argparse.ArgumentParser(
        description=(
            "IPv4 tarmoqlarini tahlil qilish uchun yengil yordamchi script.\n"
            "Berilgan CIDR tarmoq uchun IP, tarmoq manzili, subnet mask va "
            "broadcast ma'lumotlarini ko'rsatadi."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Misollar:\n"
            "  %(prog)s 192.168.1.0/24\n"
            "  %(prog)s 10.0.0.0/8 --network-address\n"
            "  %(prog)s 172.16.0.0/12 -m\n"
            "  %(prog)s 192.168.1.50/24 -b\n"
        ),
    )

    # 1 va 2-shart: IPv4 argumenti majburiy pozitsion argument sifatida
    parser.add_argument(
        "ipv4",
        type=str,
        help="IPv4 tarmoq manzili (masalan: 127.0.0.0/8 yoki 192.168.1.0/24)",
    )

    # 4, 5, 6-shartlar: Maxsus bayroqlar (argumentlar bir-birini istisno qilishi uchun mutually_exclusive_group)
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-n",
        "--network-address",
        action="store_true",
        help="Faqat tarmoq manzilini (Network Address) chiqarish",
    )

    group.add_argument(
        "-m",
        "--network-mask",
        action="store_true",
        help="Faqat subnet niqobini (Subnet Mask) chiqarish",
    )

    group.add_argument(
        "-b",
        "--broadcast-address",
        action="store_true",
        help="Faqat broadcast manzilini (Broadcast Address) chiqarish",
    )

    group.add_argument(
        "-p",
        "--prefix",
        action="store_true",
        help="Faqat prefix uzunligini (masalan: 24) chiqarish",
    )

    # Agar argument berilmagan bo'lsa, avtomatik help chiqarish
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        # IPv4 tarmoq obyektini yaratish (strict=False tarmoqosti xatolarini oldini oladi)
        network = ipaddress.ip_network(args.ipv4, strict=False)

        # Agar faqat bitta narsa so'ralgan bo'lsa, shuni chiqaramiz
        if args.network_address:
            print(network.network_address)
        elif args.network_mask:
            print(network.netmask)
        elif args.broadcast_address:
            print(network.broadcast_address)
        elif args.prefix:
            print(network.prefixlen)
        else:
            # 3-shart: Default holatda ipcalc kabi to'liq ma'lumot chiqarish
            print(f"{'Address:':<20} {network.network_address}")
            print(f"{'Netmask:':<20} {network.netmask}")
            print(f"{'Wildcard:':<20} {network.hostmask}")
            print(f"{'Network:':<20} {network.with_prefixlen}")
            print(f"{'Broadcast:':<20} {network.broadcast_address}")
            print(f"{'Total Hosts:':<20} {network.num_addresses}")

    except ValueError as e:
        print(f"Xatolik: Noto'g'ri IPv4 tarmoq formati kiritildi -> {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()