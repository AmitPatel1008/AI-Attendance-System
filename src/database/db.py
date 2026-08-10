from src.database.config import supabase
import bcrypt


def hash_pass(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()


def check_pass(password, hashed_password):
    return bcrypt.checkpw(password.encode(),hashed_password.encode()
    )


# Returns True if username already exists
def check_teacher_exists(username):
    response = (supabase.table("teachers").select("username").eq("username", username).execute()
    )
    return len(response.data) > 0


def create_teacher(username, password, name):

    data = {
        "username": username,
        "password_hash": hash_pass(password),
        "name": name
    }
    response = (supabase.table("teachers").insert(data).execute())
    return response.data


def teacher_login(username, password):

    response = (supabase.table("teachers").select("*").eq("username", username).execute())
    if not response.data:
        return None
    
    teacher = response.data[0]

    if check_pass(password, teacher["password_hash"]):
        return teacher

    return None

def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data
