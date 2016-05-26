class GoatdError(Exception):
    pass


class WaypointsNotLoadedError(GoatdError):
    pass


class WaypointMalformedError(GoatdError):
    pass
