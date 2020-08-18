import sys
from math import sin, cos, sqrt, atan2, radians

# just some methods that didnt fit anywhere else

# make the load-process more pretty and understandable
def load(func):
    def wrapper(Obj, *args, **kwargs):
        print("")
        status = "loading....."
        tabs = "\t\t"
        if Obj.__class__.__name__ == "AnswerFormulator":
            tabs = "\t"
        sys.stdout.write(f"{Obj.__class__.__name__} {tabs} %s" % status)
        sys.stdout.flush()
        func(Obj, *args, **kwargs)
        status = "initialized"
        sys.stdout.write(f"\r{Obj.__class__.__name__} {tabs} %s" % status)
        sys.stdout.flush()
    return wrapper

# compute distance between two points
def computeDistance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

# compute amount of co2 with the values from the source-website
def computeCO2(distance):
    car = 0.147
    air = 0.230
    train = 0.032
    bus = 0.029

    return [[round(train * distance, 1)],
            [round(bus * distance, 1)],
            [round(car * distance, 1)],
            [round(air * distance, 1)]]
