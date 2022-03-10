from pyramid import  request
from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config

from sqlalchemy import create_engine

from passlib.handlers.sha2_crypt import sha512_crypt
from sqlalchemy.orm import sessionmaker

from ..models import UserModel
from ..models.mymodel import UserDetails
from pyramid.threadlocal import get_current_request

#for session object
conn_string="postgresql://postgres:postgres@localhost:5432/pyramid17_db"
engine=create_engine(conn_string)
Session=sessionmaker(bind=engine)
local_session=Session(bind=engine)

#for jwt auth
# from pyramid.config import Configurator
# from pyramid.authorization import ACLAuthorizationPolicy
#
# def main():
#     config = Configurator()
#     # Pyramid requires an authorization policy to be active.
#     config.set_authorization_policy(ACLAuthorizationPolicy())
#     # Enable JWT authentication.
#     config.include('pyramid_jwt')
#     # config.set_jwt_authentication_policy('secret')
#     config.set_jwt_authentication_policy('secret',
#                                     auth_type='Bearer')

########################HOME#######################

@view_config(route_name='home', renderer='app:templates/mytemplate.pt')
def my_view(request):

    return {}


################register##########

@view_config(route_name='register',request_method="GET", renderer='app:templates/register.pt')
def register_get(request):
    return {
        "name":None,
        "email":None,
        "password1":None,
        "password2":None,
        "error":None

    }
def hash_pass(password):
    hash_password= sha512_crypt.encrypt(password, rounds=150000)
    return hash_password

def create_user(name, email, password):
    password=hash_pass(password)
    user=UserModel(name=name, password=password, email=email)
    local_session.add(user)
    local_session.commit()
    return user

@view_config(route_name='register', request_method="POST", renderer='app:templates/register.pt')
def register_post(request : Request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    password1=request.POST.get("password1")
    password2=request.POST.get("password2")
    if not name or not email or not password2 or not password1:

        return {
            "name": name,
            "email": email,
            "password1": password1,
            "password2": password2,
            "error": "some required fields are missing"
        }
    if password2 != password1:
        return {
            "name": name,
            "email": email,
            "password1": None,
            "password2": None,
            "error": "password is mismatching"
        }
    email=email.lower().strip()

    user=create_user(name, email, password1)

    return HTTPFound('/details')



###############details#############

@view_config(route_name='details',request_method="GET", renderer='app:templates/details.pt')
def details_get(request):

    users=local_session.query(UserModel).all()
    print(users)
    user_id=request.matchdict['id']
    print(user_id)
    return {
        "emp_code":None,
        "phone_no": None,
        "incharge":users,
        "error":None
    }


def create_userdetails(emp_code, phone_no, user, incharge):
    local_session.query()
    detail=UserDetails(emp_code=emp_code,phone_no=phone_no,
                       user_id=user,user_incharge_id=incharge)
    local_session.add(detail)
    local_session.commit()
    return  detail


@view_config(route_name='details',request_method="POST", renderer='app:templates/details.pt')
def details_post(request: Request):
    emp_code=request.POST.get("emp_code")
    phone_no=request.POST.get("phone_no")
    # user_id=request.matchdict['id']
    # print(user_id)
    user_incharge_id = request.POST.get("incharge")
    if not emp_code or not phone_no:
        return {
            "emp_code": emp_code,
            "phone_no": phone_no,

            "incharge": user_incharge_id,
            "error": "some required fields r missing"
        }

    create_userdetails(emp_code,phone_no,user_incharge_id)#,user_id)
    return HTTPFound("/login")

###################login####################

@view_config(route_name='login',request_method="GET", renderer='app:templates/login.pt')
def login_get(request):

    return {
        "password": None,
        "email": None,
        "error":None
    }


def verify_hash(hashed_pass,password) :
    if sha512_crypt.verify(password,hashed_pass):
        return 1
    return None

def login_user(email, password):

    user = local_session.query(UserModel).filter(UserModel.email == email).first()
    paw = user.password
    # user_id=user.id
    if not user:
        return None
    if not verify_hash(paw, password):
        return None
    #for jwt
    # if user_id:
    #     return {
    #         'result': 'ok',
    #         'token': request.create_jwt_token(user_id)
    #     }
    #
    # hdfhgdfvbkdlfvn
    return user


@view_config(route_name='login',request_method="POST", renderer='app:templates/login.pt')
def login_post(request: Request):
    password=request.POST.get("password")
    email=request.POST.get("email")
    if not email or not password:
        return {
            "email":email,
            "password":password,
            "error":"some required fields r missing"
        }
    email=email.lower().strip()
    user=login_user(email,password)
    if not user:
        return {
            "email":None,
            "password":None,
            "error":"user don't exist r wrong password"
        }

    return HTTPFound("/show")

################show####################

@view_config(route_name='show', renderer='app:templates/show.pt')
def show(request:Request):
    user=get_current_request()
    print('ans',user)


    return {"name":'pp',
            "id":'ii',}







db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
