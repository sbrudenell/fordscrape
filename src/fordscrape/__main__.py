import argparse

from fordscrape import zipcodes


def main() -> int:
    parser = argparse.ArgumentParser("fordscrape")

    parser.parse_args()

    for zipcode in zipcodes.iter_zipcodes_with_max_separation_miles(100):
        print(zipcode)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
