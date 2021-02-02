# ok2curl
Okhttp logs to curl

I learnt too late about [Ok2Curl](https://github.com/mrmike/Ok2Curl) 

# Usage
Pass a log file:
`python ok2curl.py -f sample.txt`

or pipe it in:
`cat sample.txt | python ok2curl.py`

Output
```
>>> Curl command is:
curl -i -X GET -H "Authorization: Bearer TOKEN" -H "custom-header: XXX" -H "User-Agent: Dalvik/2.1.0 (Linux; U; Android 11; KB2003 Build/RP1A.201005.001)" -H "Host: ai.sumo.tv2.no" -H "Connection: Keep-Alive" -H "If-Modified-Since: Mon, 01 Feb 2021 12" "http://fpitters.com/api/v1/dummy"
```
