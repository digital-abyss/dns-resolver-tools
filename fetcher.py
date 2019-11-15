#!/usr/bin/env python

import requests
import click
from dns import resolver, exception
from urllib3.util import connection
import hashlib


##Courtesy of https://stackoverflow.com/questions/22609385/python-requests-library-define-specific-dns
_orig_create_connection = connection.create_connection

def patched_create_connection(address, *args, **kwargs):
    """Wrap urllib3's create_connection to resolve the name elsewhere"""
    # resolve hostname to an ip address; use your own
    # resolver here, as otherwise the system resolver will be used.
    host, port = address
    hostname = the_resolver(host)

    return _orig_create_connection((hostname, port), *args, **kwargs)



current_host = '0.0.0.0'
nameserver_index = 0

def the_resolver(host):
    global current_host, nameservers, nameserver_index

    name_server = nameservers[nameserver_index]

    #print("Nameserver = " + name_server)
    res = resolver.Resolver()
    res.nameservers = [name_server]

    answers = res.query(host, lifetime=5)
    current_host = answers[0].address

    nameserver_index+=1
    return current_host




def load_nameservers():
    #this file was fetched from https://public-dns.info/
    with open('dns-servers.txt', 'r') as f:
        nameservers = []
        for line in f.readlines():
            nameservers.append(line.strip('\n'))
    
    return nameservers

def fetch_content_from_unique_server(host_hash_contents, url):
    global nameservers, nameserver_index
    try:
        response = requests.get(url)

        content_hash_obj = hashlib.md5(response.content)


        print("Host: " + current_host + " nameserver: " + nameservers[nameserver_index] + " hash: " + content_hash_obj.hexdigest() )
        #print(response.content)
        host_hash_contents[current_host] = (nameservers[nameserver_index], content_hash_obj.hexdigest(), response.content)
    except (exception.Timeout, resolver.NoAnswer, resolver.NoNameservers):
        pass


################# ugly global initialization

connection.create_connection = patched_create_connection
nameservers = load_nameservers()

################## the main

@click.command()
@click.option('--url', type=str, help='The URL of the asset you want to fetch')
def runner(url):
    print('Fetching assets from: ' + url)

    host_hash_contents = dict()
    for nameserver in nameservers:
        fetch_content_from_unique_server(host_hash_contents, url)
    print(host_hash_contents)


if __name__ == '__main__':
    runner()