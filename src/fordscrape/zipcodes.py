import csv
import importlib.resources
import math
from collections.abc import Iterator

from . import latlongs
from .latlongs import LatLong


def _iter_zipcode_centers() -> Iterator[tuple[str, LatLong]]:
    traversable = importlib.resources.files("fordscrape").joinpath("data")
    # dbview -d , -b tl_2020_us_zcta520.dbf | cut -d, -f 1,8,9
    with traversable.joinpath("2020-us-zcta520-centers.csv").open(mode="r") as fp:
        reader = csv.reader(fp)
        for zipcode, lat_center_str, long_center_str in reader:
            yield zipcode, LatLong(float(lat_center_str), float(long_center_str))


def iter_zipcodes_with_max_separation_miles(max_separation: float) -> Iterator[str]:
    zipcode_centers = list(_iter_zipcode_centers())

    # easy version, no bsp

    min_lat = math.inf
    max_lat = -math.inf
    min_long = math.inf
    max_long = -math.inf
    for _, center in zipcode_centers:
        if center.lat < min_lat:
            min_lat = center.lat
        if center.lat > max_lat:
            max_lat = center.lat
        if center.long < min_long:
            max_long = center.long
        if center.long > max_long:
            max_long = center.long

    step_miles = (max_separation / 2) / math.sqrt(2)
    lat_step = latlongs.miles_to_latitude(step_miles)
    long_step = latlongs.miles_to_longitude(step_miles, min_lat)

    seen_zipcode_from_grid: dict[tuple[float, float], bool] = {}
    for zipcode, center in zipcode_centers:
        grid = (center.lat // lat_step, center.long // long_step)
        if seen_zipcode_from_grid.get(grid):
            continue
        yield zipcode
        seen_zipcode_from_grid[grid] = True
