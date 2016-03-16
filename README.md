# transport-optimization

Input a list of location address and get a time matrix containing driving time values.
For i, j in [1, 25]: value `a_ij` of the time matrix is the time in second to drive from i to j.

## APIs

* `geopy.geocoders` for the coordinates values
* `mapquest` for the driving time values

## INPUT:

with n = 25:

  location_1, address_1,

  location_k, address_k,

  location_n, address_n

(format: CSV)

## OUTPUT

Driving times...

  from_location_1_to_location_1,  ..., from_location_1_to_location_k, ..., from_location_1_to_location_n,

  from_location_k_to_location_1,  ..., from_location_k_to_location_k, ..., from_location_k_to_location_n,

  from_location_n_to_location_1,  ..., from_location_n_to_location_k, ..., from_location_n_to_location_n

(format: CSV)
