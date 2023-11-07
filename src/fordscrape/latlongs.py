import math
from typing import NamedTuple


class LatLong(NamedTuple):
    lat: float
    long: float


EARTH_RADIUS_MILES = 3958.756


def great_circle_unit(a: LatLong, b: LatLong) -> float:
    lat_a_radians = math.radians(a.lat)
    long_a_radians = math.radians(a.long)
    lat_b_radians = math.radians(b.lat)
    long_b_radians = math.radians(b.long)

    return math.acos(
        math.sin(lat_a_radians) * math.sin(lat_b_radians)
        + math.cos(lat_a_radians)
        * math.cos(lat_b_radians)
        * math.cos(long_a_radians - long_b_radians)
    )


def great_circle_miles(a: LatLong, b: LatLong) -> float:
    return great_circle_unit(a, b) * EARTH_RADIUS_MILES


def miles_to_latitude(miles: float) -> float:
    # https://en.wikipedia.org/wiki/Great-circle_distance#From_chord_length
    return math.degrees(2 * math.asin((miles / EARTH_RADIUS_MILES) / 2))


def miles_to_longitude(miles: float, latitude: float) -> float:
    return miles_to_latitude(miles) / math.cos(math.radians(latitude))
