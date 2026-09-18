# Regional coverage

The live-price GraphQL operation accepts an authenticated `siteId`. It has no DNO-region argument. The associated settings response identifies the site's address, which confirms that the backend resolves pricing in customer/site context.

Supplying a different `siteId` does not provide a legitimate multi-region method: authorization restricts sites to the signed-in customer, and enumerating or guessing identifiers would be inappropriate.

Safe ways to add regions are:

1. E.ON provides a documented regional endpoint and reuse permission.
2. A consenting Next Optimise customer in another region runs the same local privacy-scrubbing exporter and contributes only the public schema.

The public schema needs only the DNO region code, observation time, half-hour start/end, price, quality and price history. It must never include an address, postcode or supplier site identifier. A contributor's feed should be reviewed for identifiability before publication, especially while the tariff has few customers in a region.

