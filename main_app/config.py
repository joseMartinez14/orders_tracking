
from main_app.models import Session,User


#host = "http://localhost:8000"
host = "http://192.168.100.34:8000"


def get_server_host():
    return host

def get_user_by_session(session):
    session_user = Session.objects.filter(session_key = session).values()
    if(bool(session_user)):
        user = User.objects.filter(Email = session_user[0]["user_email"]).values()
        if(bool(user)):
            return user[0]
    return None

