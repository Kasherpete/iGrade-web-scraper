
class LoginError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class FilterError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason
