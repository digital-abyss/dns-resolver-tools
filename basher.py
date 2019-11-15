#!/usr/bin/env python
import click
from dns import resolver, exception


@click.command()
@click.option('--url', type=str, help='The (sub)domain that you want to resolve across all dns servers')
def runner(url):
    print('Resolving: ' + url)

    #this file was fetched from https://public-dns.info/
    with open('dns-servers.txt', 'r') as f:
        nameservers = []
        for line in f.readlines():
            nameservers.append(line.strip('\n'))


    #print(nameservers)

    servers = set()

    count = 0

    for nameserver in nameservers:
        count += 1

        if count % 20 == 0:
            print ('Processing...' + str(count))
            print('\tservers so far: ' + str(servers))

        try:
            res = resolver.Resolver()
            res.nameservers = [nameserver]

            answers = res.query(url, lifetime=5)

            for rdata in answers:
                servers.add(rdata.address)
        except (exception.Timeout, resolver.NoAnswer, resolver.NoNameservers):
            pass

    print('==========DONE========= All servers:')
    for server in servers:
        print(server)


if __name__ == '__main__':
    runner()