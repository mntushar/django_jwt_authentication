from rest_framework.exceptions import AuthenticationFailed


class Utility:
    def get_token(self, request):
        auth_header = request.headers.get('Authorization')  # Get the 'Authorization' header
        if not auth_header:
            raise AuthenticationFailed('Authorization header missing')

        parts = auth_header.split()  # Split the header into 'Bearer' and the token
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must be in the form "Bearer <token>"')

        token = parts[1]  # The second part is the actual token
        return token