from hhpnwapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has an existing account
    Method arguments: request -- The full HTTP request object'''
    
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    employee = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if employee is not None:
        data = {
            'id': employee.id,
            'name': employee.name,
            'uid': employee.uid
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new employee for authentication
      Method arguments: request -- The full HTTP request object'''

    # Now save the user info in the hhpnwapi_user table
    employee = User.objects.create(
        name=request.data['name'],
        uid=request.data['uid']
    )

    # Return the employee info to the client
    data = {
        'id': employee.id,
        'name': employee.name,
        'uid': employee.uid
    }
    return Response(data)
