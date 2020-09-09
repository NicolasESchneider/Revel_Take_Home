# Take Home Interviews

You have been provided a repository that contains a Django, Flask, or Rails application that hosts a few endpoints. We tried to keep our implementation as simple as possible, but you should feel free to revise our code to be uniform with the code you provide. Feel free to use any homegrown or third party utilities that you feel that you need. We would like you to complete the following tasks.  Please write this code like you would write production code, whatever that means to you.  

## Tasks

1. Implement Battery Swapping Shift

    At revel one of the main tasks for operations is keeping our vehicles charged.  We do that with a van full of batteries that drives around and swaps out the batteries for vehicles.  Swapping is done in shifts by one employee for a set number of vehicles.  We need to create the basic endpoints that allow us to manage shifts and the swaps on them.

    Requirements

    - create shifts ~ basic DONE
    - add vehicles to shifts ~ basic Done
    - review all vehicles in a shift ~ basic Done
    - complete a battery swap for a vehicle ~ basic Done
    - check if a swap has been completed for any vehicle in a shift ~ shiftId not null and battery is at 100
    - query shift to see if all vehicles in the shift have had their battery swaps
        - grab all vehicles with a given shift_id, do all have battery level 100
    Design and implement the database and api for the above

2. Implement automatic shift creation. Automatic shift creation should take a lat long that it uses as a start point.  Your vehicle selection should select the 20 closest vehicles to that point.  The vehicles should be in the order that they should be visited to reduce the amount of distance traveled. e.g. the first vehicle in the list should be the first vehicle that should be visited the second the second and so on. Please use euclidian distance vs drive distance for simplicity.

## implementing automatic shift creation

second step is implementing the travelling salesman algorithm to path/order the shift
    - 2opt seems to be the best way to solve this as a fast heuristic algorithm
    - build out a distance matrix between 2 points. It will be 21 by 21 to start. Which is well. huge. We cant afford a factorial time solution
    - building out this matrix, build a class that can take two tuples of longitude and latitude and spit out the distance between those two points

    -nearest neighbor heuristic can work maybe? in practice most vehicles will be in relatively close clusters, as I assume they will be docked together. this brings time down to O(n^2)
    - build out nearest neighbor, to start
    - use 2 opt to greedily optimize it a bit. but based on the 
## in order to store order, implement a linked list within the database.
    - Vehicles when added to a shift, will be stamped with a shift ID
    - shift.target_vehicle_id is a foreign key that points to the next vehicle to be visited.
    - Once the path has been determined, update each vehicle row to have a next_id that points to the next vehicle in the path.
        - this solves the issue of adding vehicles to a shift in progress,
        - adding only one vehicle now will only require updating two rows. the vehicle being added in question (shift_id, next_id) and the vehicle that would be before the new vehicle in the path. (next_id). We also can easily when updating a path mid shift,
        Only pull the vehicles that have not been swapped this shift, battery != 100
        