# Optimise Price Watch

Unofficial, privacy-scrubbed public tracker for observed E.ON Next Optimise half-hourly import and export prices.

The browser receives price and observation data only. It never receives an E.ON credential, customer name, address, postcode, account/site/meter identifier, energy usage or billing data. `scripts/export_public.py` uses an explicit allow-list to create `public/data/north-west.json` from the private collector response.

## Local build

```powershell
python scripts/export_public.py --url http://192.168.0.202:8511/api/prices --output docs/data/north-west.json
python -m unittest discover -s tests -v
python -m http.server 8522 --directory docs
```

## Publishing architecture

The authenticated E.ON integration remains private. A local scheduled publisher reads the existing collector, strips everything except the public schema, and updates the static data file. GitHub Pages serves the site without any credentials or access to Home Assistant.

The current E.ON GraphQL operation accepts a `siteId`, not a DNO-region parameter. Authorization binds accessible sites to the signed-in customer. A multi-region service therefore needs consenting contributors in each region or a documented E.ON regional feed; it must not enumerate or guess other customer site IDs.

See [REGIONS.md](REGIONS.md) for the regional collection design and [TERMS_REVIEW.md](TERMS_REVIEW.md) for the recorded terms review.

## Terms position

No Next Optimise tariff-specific clause found in the review expressly prohibits recording or publishing displayed prices. E.ON describes the tariff as a public beta and says future half-hour prices are predicted until delivery begins. There is no documented public API licence for the authenticated feed, so this project is deliberately non-commercial, rate-limited, attributed and privacy-scrubbed. Written E.ON permission is recommended before operating it as a large continuous public data service. This is practical technical due diligence, not legal advice.
