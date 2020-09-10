Moved the database over to Mysql from sqlite3
in order to get things up and running simply instantiate a local mysql database with the following variables
- username: rev_admin
- password: rev2020
- database: revel_takehome

the flask cli commands of reset-db and create-vehicles should still work.

Had I more time:
    - further optimize pathing algorith by implementing 2-opt search heuristic to improve pathing accuracy
    - dockerize the application for better portability/easier deployments
    - write out functional tests for every route
