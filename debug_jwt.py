"""
Debug JWT token to see what's inside
"""
import jwt
import json
import sys

def decode_jwt_token(token):
    """Decode JWT token without verification to see its contents"""
    try:
        # Decode without verification to see the payload
        decoded = jwt.decode(token, options={"verify_signature": False})
        print("JWT Token Payload:")
        print(json.dumps(decoded, indent=2))
        return decoded
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        decode_jwt_token(token)
    else:
        print("Usage: python debug_jwt.py <token>")
