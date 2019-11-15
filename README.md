#basher and fetcher - some helpful tools for validating DNS caching and asset caching issues on CDNs

## basher

Given a subdomain, this will resolve it across all DNS servers in the dns-servers.txt file

## fetcher

Given a url to content, this will fetch content from the url, using each DNS server to resolve the host.
(You can use this to tell if your content is pushed across a CDN as an example)

## Dependencies

* Python click library
* Python requests library
* Python dnspython library