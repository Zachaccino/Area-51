from TweetHarvester import TweetHarvester
from TimelineHarvester import TimelineHarvester
import sys
import os


def main():
    harvester_type = os.environ.get("HARVESTER_TYPE")
    bbox_index = os.environ.get("BBOX_INDEX")

    city_bboxes = {
        "melbourne_1": [144.593741856, -38.433859306, 145.512528832, -37.5112737225],
        "melbourne_2": [144.593741856, -38.433859306, 145.512528832, -37.5112737225], # Example, need to find a better box.
        "sydney_1": [150.83694126664318, -33.519404834625824, 151.36885088550818, -34.12093552755375], # Example, need to find a better box.
        "sydney_2": [150.83694126664318, -33.519404834625824, 151.36885088550818, -34.12093552755375] # Example, need to find a better box.
    }

    if harvester_type == "TWEET":
        bboxes = sorted([(n, c) for n, c in city_bboxes.items()], key=lambda x : x[0])
        target_idx = int(bbox_index)
        harvester = TweetHarvester(bboxes[target_idx][0], bboxes[target_idx][1])
        harvester.start()
    else:
        harvester = TimelineHarvester(city_bboxes)
        harvester.start()


if __name__ == "__main__":
    main()