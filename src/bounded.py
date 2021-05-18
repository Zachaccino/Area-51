
loc1 = [-34.9288, 138.6]
loc2 = [144.9, -38]
bbox_melb = [144.593741856, -38.433859306, 145.512528832, -37.5112737225]
# "bounding_box":{"type":"Polygon","coordinates":[[[144.593741856,-38.433859306],[145.512528832,-38.433859306],[145.512528832,-37.5112737225],[144.593741856,-37.5112737225]]]}
polygon_melb = [[144.593741856,-38.433859306],[145.512528832,-38.433859306],[145.512528832,-37.5112737225],[144.593741856,-37.5112737225]]

def bounded_point(coordinates, bounds):
    print(coordinates)
    print(bounds)
    x1_bound = bounds[0]
    y1_bound = bounds[1]
    x2_bound = bounds[2]
    y2_bound = bounds[3]
    x1 = coordinates[0] # longitude
    y1 = coordinates[1] # latitude
    if (x2_bound >= x1) and (x1 >= x1_bound) and (y2_bound >= y1) and (y1 >= y1_bound):
        return True
    return False

# print(bounded_point(loc2, bbox_melb))
# print(bounded_point(loc1, bbox_melb))


def bounded_polygon(polygon, bounds):
    x1_bound = bounds[0]
    y1_bound = bounds[1]
    x2_bound = bounds[2]
    y2_bound = bounds[3]
    x1 = polygon[0][0] # longitude
    y1 = polygon[0][1] # latitude
    x2 = polygon[1][0]
    y2 = polygon[2][1]
    if (x2_bound >= x1) and (x1 >= x1_bound) and (y2_bound >= y1) and (y1 >= y1_bound) and \
    (x2_bound >= x2) and (x2 >= x1_bound) and (y2_bound >= y2) and (y2 >= y1_bound):
        print(x1_bound, y1_bound, x2_bound, y2_bound)
        print()
        print(x1, y1, x2, y2)
        return True
    return False

print(bounded_polygon(polygon_melb, bbox_melb))
