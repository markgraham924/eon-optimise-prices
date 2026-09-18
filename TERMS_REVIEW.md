# Terms and data review

Reviewed 18 September 2026 against the current **Next Optimise Terms and Conditions v1**, E.ON Next standard residential terms, the public tariff page, and the customer's E.ON quote/application emails.

## Finding

The tariff-specific terms do not expressly prohibit a customer from recording or publishing the prices displayed to them. The emails reviewed point to E.ON's general terms and do not add a price-data confidentiality or republication restriction.

That is not the same as an open-data licence. The authenticated GraphQL service is undocumented for third-party public reuse. UK database rights can protect a database where there has been substantial investment in obtaining, verifying or presenting its contents. Continuous systematic republication is therefore the main unresolved legal risk, even though the tariff contract itself contains no explicit ban found in this review.

## Relevant tariff clauses

- 4.2: the unit rate updates every half hour; predicted half-hour prices are visible on a rolling basis and the rate becomes fixed when delivery begins.
- 4.6: Next Optimise and its application are in public beta.
- 5.1: quote estimates use historic prices, area usage patterns, and customer-supplied system details.
- 6.1 and 6.5: billing uses actual half-hour readings and rates; average rates shown on bills are informational.
- 8: personal information is handled under E.ON's privacy policy.

Clause 3.1.9 restricts joining third-party flexibility schemes. This read-only website does not control, aggregate or enrol energy assets and is not a flexibility scheme.

## Controls in this project

- Non-commercial, unofficial presentation with source attribution.
- No E.ON branding or suggestion of endorsement.
- No credentials in the browser or repository.
- Public schema explicitly excludes customer, address, postcode, account, site, meter, usage and billing fields.
- Prices are labelled as observations from one consenting site and one region.
- Future values are labelled as changeable; E.ON remains the authoritative billing source.
- Collection remains at the established five-minute interval rather than adding load to E.ON's service.

## Recommendation

Ask E.ON for written permission or a published data licence before enabling a permanent continuously updated public feed, adding many contributors, or commercialising the service. A solicitor familiar with UK intellectual-property/database law should review any commercial expansion.

This is technical and contractual due diligence, not legal advice.

