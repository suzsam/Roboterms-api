import os
import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Ensure environment variables are set
if not all([os.getenv('AUTH0_DOMAIN'), os.getenv('ALGORITHMS'), os.getenv('API_AUDIENCE')]):
    raise RuntimeError("Environment variables are not set, did you source setup.sh?")

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')    # 'roboterms.us.auth0.com'
ALGORITHMS = [os.getenv('ALGORITHMS')]      # ['RS256'], a list, but just one here
API_AUDIENCE = os.getenv('API_AUDIENCE')    # 'roboterms-api'

# Permissions set up on Auth0 (RBAC)
# post:company
# delete:company
# edit:policy

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes (different than standard aborts)
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    token = request.headers.get('Authorization', None)
    if not token:
        # If no header, .get above returns None
        raise AuthError({
            'code': 'missing_auth_header',
            'description': 'Missing Authorization header'
        }, 401)
    
    # Token should return a list, with first part "Bearer" and second part the actual token
    parts = token.split()

    # Check first part is bearer
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    # Check for missing token (only one element to list) or extra elements
    if len(parts) != 2:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Auth header invalid.  Must contain bearer token.'
        }, 401)
    
    # If we get here, take the token as-is
    token = parts[1]
    return token


def verify_decode_jwt(token):
    '''
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    NOTE: urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    '''
    # Get the public keys for RSA from Auth0 here:
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    try:
        unverified_header = jwt.get_unverified_header(token)    # Gets the header, but hasn't verified anything (don't trust it!)
    except Exception as e:
        print(f'Exception in verify_decode_jwt(): {e}')
        abort(400)
    
    # We need to search for the RSA public key id ("kid") that matches the public keys
    # over at the Auth0.com/well-known/jwks.json link
    
    # Example of a header for one of our tokens:
    # unverified_header = {
    #     "alg": "RS256",
    #     "typ": "JWT",
    #     "kid": "Jyh1-4Bv8DT-dLVtnbI58"
    # }

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # Iterate searching for a match
    # Example of what's in the Auth0 well-known public key info:
    
    rsa_key = {}
    for key in jwks['keys']:

        # print(f"key kid: {key['kid']}")   # Debugging why rsa_key not found

        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break   # No need to look further
    
    # Now finally verify the signature
    if rsa_key:
        try:
            # Straight from JWT documentation, https://python-jose.readthedocs.io/en/latest/jwt/api.html
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    
    if 'permissions' not in payload:
        raise AuthError({
                'code': 'invalid_token',
                'description': 'Unable to find permissions.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
                'code': 'forbidden',
                'description': 'User does not have required permissions.'
        }, 403)

    return True


'''
    @INPUTS
        permission: string permission (i.e. 'post:company')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method to validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method

    Call it with:  @requires_auth(permission='post:company')
    You'll also need to pass on 'payload' to any view which is decorated with it
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # print("in requires_auth")
            token = get_token_auth_header()
            # print("..got token")
            payload = verify_decode_jwt(token)
            # print("....verified token")
            check_permissions(permission, payload)
            # print("......permissions checked OK")
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator