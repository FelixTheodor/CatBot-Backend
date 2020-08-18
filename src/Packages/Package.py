import json

# parent class for all packages to make ure that they are all jsonable


class Package:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
