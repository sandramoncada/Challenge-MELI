import pymongo,json,os,urllib,requests,jwt,base64

def validateJWT(jwt_token):
    public_key = base64.b64decode(os.environ["public_key"])
    try:
        jwt.decode(jwt_token, public_key, algorithms=["RS256"], audience=["getinfo","getuser"])
        return True
    except:
        return False

def getUser(id):
    client = pymongo.MongoClient("mongodb+srv://"+os.environ["mongo_user"]+":"+urllib.parse.quote(os.environ["mongo_pass"])+"@cluster0.ph8e1go.mongodb.net/?retryWrites=true&w=majority")
    response = client["RetoMeli"]["Customers"].find_one(
        {
            "id": id
        }
    )
    user = {
        "id": response['id'],
        "user_name": response['user_name'],
        "credit_card_num": "xxxx-xxxx-xxxx-"+response["credit_card_num"][:-4],
        "cuenta_numero": "xxxxx"+response["cuenta_numero"][:-3],
        "codigo_zip": response["codigo_zip"],
        "fec_alta": response['fec_alta'],
        "direccion": response['direccion'],
        "geo_latitud": response['geo_latitud'],
        "geo_longitud": response['geo_longitud'],
        "color_favorito": response['color_favorito'],
        "foto_dni": response['foto_dni'],
        "ip": response['ip'],
        "auto": response['auto'],
        "auto_modelo": response['auto_modelo'],
        "cantidad_compras_realizadas": response['cantidad_compras_realizadas'],
        "avatar": response['avatar'],
        "fec_birthday": response['fec_birthday']

    }
    return user


def getInfo():
    url = "https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios"
    response = requests.request("GET", url, headers={}, data={})
    if response.status_code == 200:
        json_data = json.loads (response.text)
        client = pymongo.MongoClient("mongodb+srv://"+os.environ["mongo_user"]+":"+urllib.parse.quote(os.environ["mongo_pass"])+"@cluster0.ph8e1go.mongodb.net/?retryWrites=true&w=majority")      
        for item in json_data:
            response = client["RetoMeli"]["Customers"].replace_one(
                    {
                        "id": item["id"]
                    },
                    {
                        "id": int(item["id"]),
                        "user_name": item["user_name"],
                        "credit_card_num": item["credit_card_num"],
                        "credit_card_ccv": item["credit_card_ccv"], 
                        "cuenta_numero": item["cuenta_numero"], 
                        "codigo_zip": item["codigo_zip"],  
                        "fec_alta": item["fec_alta"],  
                        "direccion": item["direccion"],  
                        "geo_latitud": item["geo_latitud"], 
                        "geo_longitud": item["geo_longitud"], 
                        "color_favorito": item["color_favorito"],  
                        "foto_dni": item["foto_dni"],
                        "ip": item["ip"],
                        "auto": item["auto"],
                        "auto_modelo": item["auto_modelo"],
                        "auto_tipo": item["auto_tipo"],
                        "auto_color": item["auto_color"],
                        "cantidad_compras_realizadas": item["cantidad_compras_realizadas"],
                        "avatar": item["avatar"],
                        "fec_birthday": item["fec_birthday"]
                    },
                    upsert=True
            )
        return True
    return False


def handler(event, context):
    if "authorization" in event["headers"] and validateJWT(event["headers"]["authorization"].split(" ")[1]):
        if event["requestContext"]["http"]["path"] == "/getinfo" and event["requestContext"]["http"]['method'] == "POST":
            getInfo()
            return {
                'statusCode': 200,
                'body': "DB updated"
            }

        elif event["requestContext"]["http"]["path"] == "/getuser" and event["requestContext"]["http"]['method'] == "GET":
            try:
                id = int(json.loads(event["body"])['id'])
                return {
                    'statusCode': 200,
                    'body': getUser(id)
                }
            except:
                return {
                    'statusCode': 400,
                    'body': "Bad Request"
                }
            
        else:
            return {
                'statusCode': 400,
                'body': "Bad Request"
            }
    else:
        return {
                'statusCode': 403,
                'body': "Forbidden"
        }