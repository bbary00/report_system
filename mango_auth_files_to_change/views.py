from rest_framework.decorators import api_view
from mongo_auth.utils import create_unique_object_id, pwd_context
from mongo_auth.db import database, auth_collection, fields, jwt_life, jwt_secret, secondary_username_field
import jwt
import datetime
import pymongo
from mongo_auth import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


@api_view(["POST"])
def signup(request):
    try:
        data = request.data if request.data is not None else {}
        last_obj = database[auth_collection].find().sort('id', pymongo.DESCENDING)
        signup_data = {"id": int(last_obj[0]['id']) + 1}
        all_fields = set(fields + ("email", "password"))
        if secondary_username_field is not None:
            all_fields.add(secondary_username_field)
        for field in set(fields + ("email", "password")):
            if field in data:
                signup_data[field] = data[field]
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"error_msg": field.title() + " does not exist."})
        signup_data["password"] = pwd_context.hash(signup_data["password"])
        signup_data["last_login"] = datetime.datetime.now()
        signup_data["date_joined"] = datetime.datetime.now()
        signup_data["is_superuser"] = False
        signup_data["is_staff"] = False
        signup_data["is_active"] = True
        signup_data["first_name"] = data['first_name'] if 'first_name' in data else ''
        signup_data["last_name"] = data['last_name'] if 'last_name' in data else ''
        if database[auth_collection].find_one({"email": signup_data['email']}) is None:
            if secondary_username_field:
                if database[auth_collection].find_one({secondary_username_field: signup_data[secondary_username_field]}) is None:
                    database[auth_collection].insert_one(signup_data)
                    res = {k: v for k, v in signup_data.items() if k not in ["_id", "password"]}
                    return Response(status=status.HTTP_200_OK,
                                    data={"data": res})
                else:
                    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                                    data={"data": {"error_msg": messages.user_exists_field(secondary_username_field)}})
            else:
                database[auth_collection].insert_one(signup_data)
                res = {k: v for k, v in signup_data.items() if k not in ["_id", "password"]}
                return Response(status=status.HTTP_200_OK,
                                data={"data": res})
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                            data={"data": {"error_msg": messages.user_exists}})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
       return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                       data={"data": {"error_msg": str(e)}})


@api_view(["POST"])
def login(request):
    try:
        data = request.data if request.data is not None else {}
        username = data['username']
        password = data['password']
        if "@" in username:
            user = database[auth_collection].find_one({"email": username}, {"_id": 0})
        else:
            if secondary_username_field:
                user = database[auth_collection].find_one({secondary_username_field: username}, {"_id": 0})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"data": {"error_msg": messages.user_not_found}})
        if user is not None:
            if pwd_context.verify(password, user["password"]):
                token = jwt.encode({'id': user['id'],
                                    'exp': datetime.datetime.now() + datetime.timedelta(
                                        days=jwt_life)},
                                   jwt_secret, algorithm='HS256').decode('utf-8')
                try:
                    database[auth_collection].updateOne(
                        {secondary_username_field: username},
                        { "$set": {"last_login": datetime.datetime.now()}}
                    )
                except Exception as error:
                    print(error)

                return Response(status=status.HTTP_200_OK,
                                data={"data": {"token": token}})
            else:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={"error_msg": messages.incorrect_password})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"data": {"error_msg": messages.user_not_found}})
    except ValidationError as v_error:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'success': False, 'message': str(v_error)})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})
