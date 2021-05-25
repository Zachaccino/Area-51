"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

from TweetHarvester import TweetHarvester
from TimelineHarvester import TimelineHarvester
import sys
import os


def main():
    harvester_type = os.environ.get("HARVESTER_TYPE")
    bbox_index = os.environ.get("BBOX_INDEX")
    city_bboxes = {
        "melbourne_1": [144.593741856, -38.433859306, 145.000000000, -37.5112737225],
        "melbourne_2": [145.000000001, -38.433859306, 145.512528832, -37.5112737225],
        "sydney_1": [150.83694126664318, -34.12093552755375, 151.36885088550818, -33.850000000000000],
        "sydney_2": [150.83694126664318, -33.850000000000001, 151.36885088550818, -33.519404834625824]
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
