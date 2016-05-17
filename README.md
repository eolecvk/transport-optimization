# transport-optimization

### Premise
I started this project to optimize the operations of the organization [*Lovin' Spoonfuls*](http://lovinspoonfulsinc.org/) which mission is to facilitate the rescue and distribution of healthy, fresh food that would otherwise be discarded.
Specifically, they pick up fresh food that would otherwise be thrown away from grocery stores, produce wholesalers, farms and farmers markets, and distribute it to community non-profits that feed Greater Boston’s hungry.

This project includes concepts from the field of operation research, graph theory and algorithm design.

### Data

#### Node data
I had access to the operational data of *Lovin' Spoonfuls*. The data provided by the organization are used as node attributes. The node attributes include:
  * `node_id`: unique identifier for a node
  * `node_location`: exact address in the format [street_address, street_name, city, zip]
  * `expected_load`: supply (case: expected_load > 0) or demand (case: expected_load < 0)
  * `start_time`: beginning time of the node time window in 24:00hrs format
  * `end_time`: ending time of the node time window in 24:00hrs format

*`node_location` values are anonymized because I signed a Non-Disclosure Agreement with Lovin' Spoonfuls.*
*`expected_load` values are an estimate value derived from historical data using a regression.*

#### Distance matrix with `time_matrix.py`

I developed a script to generate a distance matrix between each nodes (distance is interpreted as driving time in seconds). I am using `geopy.geocoders` to retrieve the coordinates values from the location address and `mapquest API` for the driving time values.

`time_matrix.py` :


**INPUT, format: CSV**
*with n <= 25:*
  location_1, address_1,
  location_k, address_k,
  location_n, address_n

**OUTPUT, format: CSV**
Returns a time matrix containing driving time in seconds between input addresses.  
For i, j in [1, 25]: value `a_ij` in output matrix is the driving time in seconds from address i to address j:

  from_location_1_to_location_1,  ..., from_location_1_to_location_k, ..., from_location_1_to_location_n,
  from_location_k_to_location_1,  ..., from_location_k_to_location_k, ..., from_location_k_to_location_n,
  from_location_n_to_location_1,  ..., from_location_n_to_location_k, ..., from_location_n_to_location_n

### Operational constraints

The operations of *Lovin' Spoonfuls* are subject to a number of operational constraints. Specifically:
- There is a fixed and finite number of truck/drivers.
- The drivers will drive given maximum number of hours a day.
- Trucks have a maximum load capacity (although empirically this is not a binding constraint)
- Food that is picked up needs to be delivered on the same day (storage is not an option)
- Supply and demand nodes have time windows and are not accessible outside of their specific time windows
- Food supply is uncertain and can only be estimated based on historical data

### Objective

The overall objective is to optimize the operation of *Lovin' Spoonfuls* in terms of the quantity of food they are able to rescue per week given their operational constraints.
I worked on multiple models to optimize the overall route schedule of *Lovin' Spoonfuls*.
Each model addresses a specific aspect of the route schedule optimization.

#### Sub-objective #1: 

##### Optimize a route given a set of nodes using the Travelling Salesman model

A simplification of the objective could be to find the best routes on a given day, given a set of nodes.
The Travelling Salesman model aims specifically at finding the best route given a predetermined set of nodes.

##### Assumption

The nature of the Travelling salesman model requires to have selected the nodes the driver will go through during his or her journey. The travelling salesman model alone is not helpful in determining which nodes should be included in the route and which should not. It is possible to perform multiple iterations of the TSP on different sets of nodes and to find an optimal result but this approach is rather inefficient.

##### Algorithms

###### Brute-force

see `brute_force_route_gen.py` 

###### Dynamic programming, Breadth-first search

see `TSP_dynamic_programming.ipynb`
