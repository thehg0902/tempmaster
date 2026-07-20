# JSON-LD LocalBusiness Template
{
 "@context":"https://schema.org",
 "@type":"<subtype or LocalBusiness>",
 "name":"", "url":"", "telephone":"", "image":"<absolute hero/og url>",
 "address":{"@type":"PostalAddress","streetAddress":"","addressLocality":"",
   "addressRegion":"","postalCode":"","addressCountry":""},
 "geo":{"@type":"GeoCoordinates","latitude":0,"longitude":0},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
   "dayOfWeek":[],"opens":"","closes":""}],
 "sameAs":[]
}
Rules: every value from client.md (hours -> QUESTIONS if absent); geo from
the client's Maps link coordinates; sameAs = social URLs; omit fields you
can't source rather than inventing. Validate structure mentally against
required-by-type fields; suggest the user run Google's Rich Results test
post-deploy (record as post-deploy check).
