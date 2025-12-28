import pytest

from app.config import settings
from app import schemas
from jose import jwt



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200




def test_create_user(client):
    res = client.post("/users",json={"email":"pytest@gmail.com","password":"123456"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "pytest@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user,client):
    res = client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload= jwt.decode(login_res.access_token,settings.secret_key,[settings.algorithm])
    id : str = payload.get("user_id") # type: ignore

    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code",[
    ('pytest@gmail.com', '1234567', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 403),
    ('sanjeev@gmail.com',None , 403)
])
def test_incorrent_login(client,test_user,email,password,status_code):
    res = client.post("/login",data={"username":email,"password":password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
