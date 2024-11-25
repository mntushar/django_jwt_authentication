import types

from rest_framework.exceptions import ValidationError


class DataValidation:
    def __init__(self, data_type=None, serializer_class=None):
        self.__data_type = data_type
        self.__serializer_class = serializer_class

    def serializer_validate(self, data):
        serializer_result = self.__serializer_class(data=data)
        if not serializer_result.is_valid():
            raise ValidationError(serializer_result.errors)
        return serializer_result.save()

    def data_validation(self, data):
        if not isinstance(data, self.__data_type):
            raise ValidationError('Invalid data type')
        return  data