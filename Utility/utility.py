from django.conf import settings

class Utility:
    def get_error(self, error: Exception) -> str:
        if settings.DEBUG:
            return str(error)
        else:
            return 'Something went wrong. Please try again after some time.'