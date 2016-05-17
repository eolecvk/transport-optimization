# transport-optimization

### Premise
I started this project to optimize the operations of the organization [*Lovin' Spoonfuls*](http://lovinspoonfulsinc.org/) which mission is to facilitate the rescue and distribution of healthy, fresh food that would otherwise be discarded.
Specifically, they pick up fresh food that would otherwise be thrown away from grocery stores, produce wholesalers, farms and farmers markets, and distribute it to community non-profits that feed Greater Boston’s hungry.

This project includes concepts from the field of operation research, graph theory and algorithm design.

### Data

* Node data
I had access to the operational data of *Lovin' Spoonfuls* but cannot display it online because I signed a NDA. The data provided by the organization are used as node attributes. The node attributes include:
- node_id
- node_location
- expected_load
- start_time
- end_time

* Distance matrix
I developed a script to generate a distance matrix between each nodes (distance is interpreted as driving time in seconds). I am using `geopy.geocoders` to retrieve the coordinates values from the location address and `mapquest API` for the driving time values. The script is available in the repository as `time_matrix.py`.

### Operational constraints

*Lovin' Spoonfuls* 
has a certain number of truck/drivers.


### Objective

The overall objective is to optimize the operation of *Lovin' Spoonfuls* in terms of the quantity of food they are able to rescue per week given their operational constraints.

My goal was to find the best routes for the drivers of *Lovin' Spoonfuls*, in terms of  in a day.
I worked on multiple models to optimize the overall route schedule of *Lovin' Spoonfuls*.
The Travelling Salesman model aims specifically at finding the best route given a predetermined set of nodes.

### Assumption
The nature of the Travelling salesman model requires to have selected the nodes the driver will go through during his or her journey. The travelling salesman model alone is not helpful in determining which nodes should be included in the route and which should not.
It is possible to perform multiple iterations of the TSP on different sets of nodes and to find an optimal result put this approach would be rather inefficient.




















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
