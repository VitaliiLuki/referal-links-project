from rest_framework import views, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .utils import generate_random_inv_code, generate_auth_code
from users.models import Invite, User
from .serializers import UserSerializer
from .validators import (validate_auth_code, validate_phone_number,
                         validate_invite_code)
import time


class RetrieveViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    pass


class SendAuthCodeView(views.APIView):
    """
    View for sending an authentication code to a user's phone number.

    This view handles the process of sending an authentication code to the
    provided phone number. If a user with the specified phone number already
    exists, the authentication code is updated for that user. If the user
    does not exist, a new user is created with a generated authentication code
    and an invite code.

    Parameters:
    - phone_number (str): The phone number to which
      the authentication code is sent.

    Returns:
    - 200 OK: If the authentication code is successfully sent or updated.
    - 400 BAD REQUEST: If the 'phone_number' field is missing or invalid.
    """

    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'phone_number is required field.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Imitating 1 second delay from server
        time.sleep(1)
        auth_code = generate_auth_code()

        # Trying to find a user with provided phone_number.
        # If there is not such user, just handling exception and
        # create a new user.
        try:
            user = User.objects.get(phone_number=phone_number)
            user.auth_code = auth_code
            user.save()
        except User.DoesNotExist:
            # Invite code generation for new user.
            invite_code = generate_random_inv_code()

            # Make a phone number validation,
            # if it's invalid - throw an exception
            validate_phone_number(phone_number)

            user = User.objects.create(phone_number=phone_number,
                                       auth_code=auth_code,
                                       invite_code=invite_code)
            user.save()

        return Response({'auth_code': auth_code}, status=status.HTTP_200_OK)


class CheckPhoneAuthCodeView(views.APIView):
    """
    API view for checking phone_number, authentication code and
    generating an access token.

    This view handles the process of checking whether the provided phone number
    and authentication code match a user's credentials. If the provided
    credentials are valid, an access token is generated and returned.

    Parameters:
    - phone_number (str): The user's phone number.
    - auth_code (str): The authentication code to be checked.

    Returns:
    - 200 OK: If the provided credentials are valid an access token providing.
    - 400 BAD REQUEST: If either 'phone_number' or 'auth_code' is missing,
      or if the provided credentials do not match any user.
    """
    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if not (phone_number and auth_code):
            return Response(
                {'error': 'please submit both: phone_number and auth_code.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validating phone_number and auth_code
        # If not valid - throw an exception
        validate_phone_number(phone_number)
        validate_auth_code(auth_code)

        # Trying to find a user with provided credentials
        try:
            user = User.objects.get(
                phone_number=phone_number,
                auth_code=auth_code
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': f'Token {token}'},
                status=status.HTTP_200_OK
            )
        # If user wasn't found return 400 code.
        except User.DoesNotExist:
            return Response(
                {'message': 'User with provided credentials is not found'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileViewSet(RetrieveViewSet):
    """
    Viewset for managing user profiles and invite code application.

    This viewset provides functionality to retrieve a user profile and
    apply an invite code, and also provides with list of users and detail
    user's information. User can view their own profile using a GET request,
    and they can apply an invite code using a POST request.

    Endpoints:
    - GET /users/: Get list of users.
    - GET /users/<user_id>: Retrieve information about certain user.
    - GET /users/me/: Retrieve the user's own profile.
    - POST /users/me/: Apply an invite code to the user's profile.

    Parameters:
    - invite_code (str): The invite code to be applied to the user's profile
      (for POST request).

    Returns:
    - 200 OK: If the GET request is successful, along with the user's profile
      data.
    - 201 CREATED: If the invite code is successfully applied to the user's
      profile.
    - 400 BAD REQUEST: If the invite code is missing, invalid, or
      already applied, or if the provided
      invite code doesn't exist.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['GET', 'POST'],
        url_path='me'
    )
    def my_profile(self, request):
        user = request.user

        # For GET request
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # For POST request
        invite_code = request.data.get('invite_code')

        # Check that invite_code is provided
        if not invite_code:
            return Response(
                {'error': 'invite_code is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Invite code validation
        validate_invite_code(invite_code)

        # Check that provided invite code exists
        try:
            code_belong_to = User.objects.get(invite_code=invite_code)
            # Check for user has already had invite code
            if user.activated_invite_code:
                return Response(
                    {'message': 'invite code has already applied.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.activated_invite_code = invite_code
            user.save()

            # Create a note in DB whose invite code was used by
            Invite.objects.create(
                invitation_belong_to=code_belong_to,
                invited_user=user
            )
            return Response(
                {'message: ': f'{invite_code} has been applied.'},
                status=status.HTTP_201_CREATED
            )
        except User.DoesNotExist:
            return Response(
                {"message: ": "provided invite code doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
