import decimal

# Short version: sqlalchemy does not play nice with
# stringifying to JSON (certain types cannot be serialized).
# sources indicate using another library (marshmellow), but this should
# suit the project's purposes and is very lean.

# alternatively a base class could have been made which our models extend
# but this requires that a table is defined for the base class and that
# a primary key is set for the base (may not want all serializable models
# to use the same key), so I have taken the functional route
def sqla_todict(self):

    # serialized object
    result = {}
    # types to not stringify
    donotstr = [int, float, bool]

    # mapping of types to cast explicity
    cast = {decimal.Decimal : float}

    for column in self.__table__.columns:
        value = getattr(self, column.name)
        # if the value is in the cast dict. use the mapped class to cast it
        value = value if type(value) not in cast else cast[type(value)](value)
        # set value. check if it shouldn't be stringified.
        result[column.name] = value if type(value) in donotstr or value is None else str(value)

    return result


