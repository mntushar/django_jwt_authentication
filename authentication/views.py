from adrf.views import APIView
from rest_framework import status
from adrf.generics import CreateAPIView
from rest_framework.response import Response

from backend.account.authentication.serializers import LoginSerializer
from backend.account.authentication.services import AuthenticationService
from library.models.dataValidation import DataValidation


class AsyncLoginView(CreateAPIView):
    serializer_class = DataValidation(serializer_class=LoginSerializer)

    async def post(self, request, *args, **kwargs):
        service = AuthenticationService()
        result = await service.login(self.serializer_class.serializer_validate(request.data))

        if result.is_success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)

        return Response(result.to_dict(), status=status.HTTP_401_UNAUTHORIZED)


class AsyncAccessTokenView(APIView):
    data_validation = DataValidation(data_type=str)

    async def get(self, request, *args, **kwargs):
        refresh_token = self.data_validation.data_validation(request.GET.get('refresh_token'))

        service = AuthenticationService()
        result = await service.get_access_token(refresh_token)

        if result.is_success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)

        return Response(result.to_dict(), status=status.HTTP_401_UNAUTHORIZED)



