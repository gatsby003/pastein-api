# PasteBin API

https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

1. Stores pasted content in the db accessible via a url 
2. Content can have an expiry 
3. Users can register or annonymously post 
4. Postgres for permanent storage , redis for caching and mongodb for document storage
5. Page view analytics 

-> read and write api with django and postgres
-> caching with redis , using redis as analytics store
-> background job to persist analytics 
