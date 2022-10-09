import jwt,time
iat = time.time()
exp = iat + 3600
payload = {
    'iss': 'https://www.mercadolibre.com.co',
    'sub': 'https://www.mercadolibre.com.co',
    'aud': ["getinfo","getuser"],
    'iat': iat,
    'exp': exp
}
private_key = open("private.pem", "r").read()
jwt_token = jwt.encode(payload, private_key, algorithm="RS256")
print(jwt_token)

