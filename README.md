[![Build Status](https://travis-ci.org/harrisbaird/dailyteedeals_scrapers.svg?branch=master)](https://travis-ci.org/harrisbaird/dailyteedeals_scrapers)
[![Code Climate](https://codeclimate.com/github/harrisbaird/dailyteedeals_scrapers/badges/gpa.svg)](https://codeclimate.com/github/harrisbaird/dailyteedeals_scrapers) 
[![Docker Build Statu](https://img.shields.io/docker/build/harrisbaird/dailyteedeals_scrapers.svg)](https://hub.docker.com/r/harrisbaird/dailyteedeals_scrapers/)
[![](https://images.microbadger.com/badges/image/harrisbaird/dailyteedeals_scrapers.svg)](https://microbadger.com/images/harrisbaird/dailyteedeals_scrapers "Get your own image badge on microbadger.com")

# Daily Tee Deals - Scrapers

A collection of [Scrapy](https://scrapy.org) spiders for extracting designs from daily tee websites, including: [ShirtPunch](https://shirtpunch.com), [Teefury](https://teefury.com), [Yetee](https://yetee.com), [Qwertee](https://qwertee.com) and 40+ other sites.

## Running

`docker run -p 6800:6800 -p 6900:6900 -it harrisbaird/dailyteedeals_scrapers`

Two services will now be running:
* Scrapyd on 6800
* Flask on 6900

The Flask service provides the following endpoints for convenience:
* [GET] **/status/<job_id>** - Get the status of a job. returns 'running', 'pending', 'finished' or '' for unknown state.
* [GET] **/download/<job_id>** - Download the item feed of a job in JsonLines / .jl format.
* [POST] **/schedule/<spider>** - Schedule a job with the given spider name, returning a job id.

Alternatively, the [scrapyd](https://scrapyd.readthedocs.io/) service can be called directly.

## Example JSON output

```json
{
    "name": "Abbey road", 
    "url": "https://www.qwertee.com",
    "active": true, 
    "deal": true,
    "last_chance": true, 
    "expires_at": "2017-07-07T23:00:00Z", 
    "valid": true,
    "image_url": "https://www.qwertee.com/images/designs/zoom/117577.jpg",
    "artist_name": "Darthdaloon",
    "artist_urls": [
        "https://society6.com/darthdaloon",
        "https://www.instagram.com/darthdaloon/",
        "https://www.qwertee.com/profile/662362"
    ],
    "prices": {
        "usd": 1200,
        "gbp": 900,
        "eur": 1100
    },
    "fabric_colors": [], 
    "tags": []
} 
```