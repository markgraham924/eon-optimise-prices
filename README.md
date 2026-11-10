# Optimise Price Watch

Unofficial historical archive of observed E.ON Next Optimise half-hourly import and export prices. Regular updates are ending as the contributor switches to Intelligent Octopus Go.

The browser receives price and observation data only. It never receives an E.ON credential, customer name, address, postcode, account/site/meter identifier, energy usage or billing data. `scripts/export_public.py` uses an explicit allow-list to create `docs/data/north-west.json` from the private collector response.

## Local build

```powershell
python scripts/export_public.py --url http://192.168.0.202:8511/api/prices/all --output docs/data/north-west.json
python -m unittest discover -s tests -v
python scripts/make_archive_charts.py  # Requires matplotlib and IANA timezone data
python -m http.server 8522 --directory docs
```

## Publishing architecture

Use the full-history `/api/prices/all` endpoint for website refreshes. The existing
`/api/prices` endpoint intentionally serves only a rolling week to the HA dashboard.
The website date selector covers every retained delivery date, including partial
boundary days, and keeps all observed revisions. No AgilePredict data is included.

The authenticated E.ON integration remains private. During regular collection, a publisher checked the freshness of both feeds and exported the static price file through the public schema. The summary charts include complete historical days across both channels. GitHub Pages serves the site without any credentials or access to Home Assistant.

The current E.ON GraphQL operation accepts a `siteId`, not a DNO-region parameter. Authorization binds accessible sites to the signed-in customer. A multi-region service therefore needs consenting contributors in each region or a documented E.ON regional feed; it must not enumerate or guess other customer site IDs.

See [REGIONS.md](REGIONS.md) for the regional collection design and [TERMS_REVIEW.md](TERMS_REVIEW.md) for the recorded terms review.

## Terms position

No Next Optimise tariff-specific clause found in the review expressly prohibits recording or publishing displayed prices. E.ON describes the tariff as a public beta and says future half-hour prices are predicted until delivery begins. There is no documented public API licence for the authenticated feed, so this project is deliberately non-commercial, rate-limited, attributed and privacy-scrubbed. Written E.ON permission is recommended before operating it as a large continuous public data service. This is practical technical due diligence, not legal advice.
