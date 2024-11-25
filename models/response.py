class Response:
    def __init__(self):
            self.is_success = True
            self.message = None

    def to_dict(self):
        return vars(self)