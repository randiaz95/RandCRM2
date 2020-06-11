from .. import app
import ezgmail
import databases
import pandas as pd
from random import randint
from ..models.auth import AuthLogin, AuthConfirm
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, String, Integer, Table, MetaData
from ..utils import encrypt, decrypt, clean


# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///db/t1.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("password", String),
    Column("code", String),
    Column("active", String),
)


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


ezgmail.init()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

with open("client.key") as file:
    output = file.read()
    cipher = Fernet(output)


@app.get("/")
async def index():
    return {"status": "success"}

@app.post("/login")
async def login(auth: AuthLogin):

    clean_email = clean(auth.email)
    clean_password = clean(auth.password)
    query = users.select()
    all_users = database.fetch_one()
    df = pd.read_sql(f"""SELECT 
                            id
                        FROM 
                            users 
                        WHERE 
                            email='{clean_email}'
                            and password='{encrypt(clean_password, cipher)}'
                            and active='T';""",
                     engine)

    if df.shape[0]==0:
        return {"status": "failed",
                "id": "None",
                "message": "Failed to authenticate."}
    else:
        return {"status": "success",
                "id": encrypt(df['id'].values[0], cipher),
                "message": "Successfully logged in."}


@app.post("/signup")
async def signup(auth: AuthLogin):

    clean_email = clean(auth.email)
    clean_password = clean(auth.password)

    df = pd.read_sql(f"""SELECT 
                            id
                        FROM 
                            users 
                        WHERE 
                            email='{clean_email}'
                            and password='{encrypt(clean_password, cipher)}'
                            and active='T';""",
                     engine)

    if df.shape[0]>0:
        return {"status": "failed",
                "id": "None",
                "message": "Email is already being used."}
    else:
        code = randint(10000, 99999)
        new_id = pd.read_sql(f"""SELECT
                                max(id)+1 as new_id
                            FROM 
                                users 
                            WHERE 
                                email='{clean_email}'
                                and password='{encrypt(clean_password, cipher)}'
                                and active='T';""",
                         engine)["new_id"].values[0]

        insert = pd.DataFrame({"email": [clean_email],
                               "password": [encrypt(clean_password, cipher)],
                               "code": [code],
                               "active": ["F"]})
        await insert.to_sql("users", engine, if_exists="append", index=False)
        ezgmail.send(auth.email,
                     "RandCRM | Confirmation Code",
                     f"Please use the confirmation code: {code}")

        return {"status": "success",
                "id": encrypt(str(new_id), cipher),
                "message": "Successfully Signed Up, please confirm."}


@app.post("/confirm")
async def confirm(auth: AuthConfirm):

    if "abcdefghijklmnopqrstuvwxyz" in auth.code:
        return {"status": "failed",
                "id": "None",
                "message": "Confirmation failed."}

    df = pd.read_sql(f"""SELECT 
                            id
                        FROM 
                            users 
                        WHERE 
                            id={int(decrypt(auth.id, cipher))}
                            and code='{auth.code}';""",
                     engine)
    if df.shape[0] == 0:
        engine.execute(f"""UPDATE users SET active='T' WHERE id={int(decrypt(auth.id, cipher))};""")
        return {
            "status": "success",
            "id": auth.id,
            "message":  "You have successfully confirmed your account."
        }
