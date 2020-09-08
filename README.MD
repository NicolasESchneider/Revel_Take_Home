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
    - check if a swap has been completed for any vehicle in a shift ~
    - query shift to see if all vehicles in the shift have had their battery swaps

    Design and implement the database and api for the above

2. Implement automatic shift creation. Automatic shift creation should take a lat long that it uses as a start point.  Your vehicle selection should select the 20 closest vehicles to that point.  The vehicles should be in the order that they should be visited to reduce the amount of distance traveled. e.g. the first vehicle in the list should be the first vehicle that should be visited the second the second and so on. Please use euclidian distance vs drive distance for simplicity.

## implementing automatic shift creation
first step is writing a SQL query that returns the 20 closest vehicles.
    Vehicles should currently NOT be in a shift
        - shift_id == None
    Not in use
        - in_use == False
    require a battery swap
        - battery_level != 100.0
        - dont do a < assessment its slower

second step is implementing the travelling salesman algorithm to path/order the shift

implementing vehicle queue
    when a vehicle is added to the queue, it is simply stamped with the shift_id.
    on the shift store the index that corresponds to the last visited vehicle:
        ex: after swapping the battery for a vehicle, Shift.index += 1
    what if a vehicle is added to the queue post shift begin? so say we've seen 2 vehicles and the index for this shift is 2 and we add a new vehicle:
        slice that array from the saved index, append the new vehicle to that sliced array
        re order the sliced section using the above pathing algorithm, the pathing algorithm should take an array of Vehicles and sort them so that the travel distance is optimized.
        Then, we slice the origin array, up to the saved index like: Vehicles[0:saved_index]
        then concat that with the un visited Vehicles. This way we only have to update only field in our database. The time complexity for repathing a shift when Adding a vehicle will be bad, But at the same I severely doubt that a shift is going to have a large amount of vehicles in it