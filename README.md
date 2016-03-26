# transport-optimization

## Generate time matrix with `time_matrix.py`

Returns a time matrix containing driving time in seconds between input addresses.  
For i, j in [1, 25]: value `a_ij` of the time matrix is the time to drive from address i to address j.

**APIs**

* `geopy.geocoders` for the coordinates values
* `mapquest` for the driving time values

**INPUT**

with n = 25:

  location_1, address_1,

  location_k, address_k,

  location_n, address_n

*(format: CSV)*

**OUTPUT**

Returns a time matrix containing driving time in seconds between input addresses.
For i, j in [1, 25]: value a_ij of the time matrix is the time to drive from address i to address j.

  from_location_1_to_location_1,  ..., from_location_1_to_location_k, ..., from_location_1_to_location_n,

  from_location_k_to_location_1,  ..., from_location_k_to_location_k, ..., from_location_k_to_location_n,

  from_location_n_to_location_1,  ..., from_location_n_to_location_k, ..., from_location_n_to_location_n

*(format: CSV)*


## Generate brute force feasible routes using `brute_force_route_gen.py` 

**Parameters:**
`TIME_LIMIT` maximum total driving time threshold (routes with driving time superior to TIME_LIMIT are filtered out from the solutions set.
