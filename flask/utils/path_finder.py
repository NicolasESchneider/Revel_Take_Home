import numpy as np
from math import radians, cos, sin, asin, sqrt, atan2
from models.vehicle import Vehicle

class PathFinder():

  def __init__(self, vehicles, shift):
    self.distance_matrix = self.build_distance_matrix(vehicles, shift)
    self.initial_route = self.nearest_neighbor_path(self.distance_matrix)
    ## calculate the inital_route using the nearest_neighbor search algorithm
    # O(n^2) time complexity
    # space wise we need O(n^2) space complexity, where n is num vehicles for the distance matrix
    self.best_route = self.initial_route
    self.best_distance = 0
    self.distances = []

  def update(self, new_route, new_distance):
    self.best_distance = new_distance
    self.best_route = new_route
    return self.best_distance, self.best_route

  def build_distance_matrix(self, vehicles, shift):
    # Build out a matrix of points containing the distance between 2 points in km
    all_points = [shift] + vehicles
    # the shift should always our initial point
    num_points = len(all_points)
    distance_matrix = np.zeros((num_points, num_points))
    for point_a in all_points:
      for point_b in all_points:
        i = all_points.index(point_a)
        j = all_points.index(point_b)
        distance_matrix[i][j] = self.calc_distance(point_a, point_b)
    
    return distance_matrix

  def two_opt(self, improvement_threshold=0.01):
    self.best_route = self.initial_route
    self.best_distance = self.calculate_path_dist(self.distance_matrix, self.best_route)
    improvement_factor = 1
    
    while improvement_factor > improvement_threshold:
      previous_best = self.best_distance
      for swap_first in range(1, self.num_cities - 2):
        for swap_last in range(swap_first + 1, self.num_cities - 1):
          new_route = self.swap(self.best_route, swap_first, swap_last)
          new_distance = self.calculate_path_dist(self.distance_matrix, new_route)
          self.distances.append(self.best_distance)
          if 0 < self.best_distance - new_distance:
            self.update(new_route, new_distance)

      improvement_factor = 1 - self.best_distance/previous_best
    return self.best_route, self.best_distance, self.distances

  def calc_distance(self, point_a, point_b):
    # given 2 points with longitude and latitude
    # return the distance in kilometers
    # employing the haversine solution here
    # https://en.wikipedia.org/wiki/Haversine_formula
    long_a = point_a.location_long
    lat_a = point_a.location_lat

    long_b = point_b.location_long
    lat_b = point_b.location_lat

    def haversine(lon1, lat1, lon2, lat2):
      # convert decimal degrees to radians 
      lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
      # haversine formula 
      dlon = lon2 - lon1 
      dlat = lat2 - lat1 
      a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
      c = 2 * asin(sqrt(a)) 
      # Radius of earth in kilometers is 6371
      km = 6371 * c
      # rounding to 3 decimal places for readability when console logging

      return round(km, 3)
    return haversine(long_a, lat_a, long_b, lat_b)

  def calculate_path_dist(self, distance_matrix, path):
    ## given a path and a distance_matrix, what is the total distance of said path
    path_distance = 0
    for i in range(len(path) - 1):
      path_distance += distance_matrix[path[i]][path[i + 1]]
    return round(float(path_distance), 3)

  def nearest_neighbor_path(self, distance_matrix):
    # distance_matrix at index 0 is our initial starting point, the shifts current lat/long,
    # we will always begin here 
    new_path = [0]

    current_distance_index = 1
    next_distance_index = 1
    # start at the first vehicle
    while len(new_path) < len(distance_matrix):
      # go until we have a completed path
      i = 1
      current_distance_index = next_distance_index
      # the first index is our inital starting point. We cant go home again
      min_distance = float('inf')
      while i < len(distance_matrix):
        # have we visited this vehicle before?
        # is it the smallest distance we've seen so far
        if distance_matrix[current_distance_index][i] < min_distance and i not in new_path:
          min_distance = distance_matrix[current_distance_index][i]
          next_distance_index = i

        i += 1
      new_path.append(next_distance_index)
    return new_path

  def swap(self, path, swap_first, swap_last):
    path_updated = np.concatenate(
      (
        path[0:swap_first],
        path[swap_last:-len(path) + swap_first - 1:-1],
        path[swap_last + 1:len(path)]
      )
    )
    return path_updated.tolist()


