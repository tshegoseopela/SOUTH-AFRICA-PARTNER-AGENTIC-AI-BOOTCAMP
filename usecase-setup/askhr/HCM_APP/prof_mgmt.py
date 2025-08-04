import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime as dt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import faker
import random

# Initialize Faker for generating fake data
fake = faker.Faker()
from config import generate_natural_response
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Database initialization
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#     #     id INTEGER PRIMARY KEY,
#     #     name TEXT,
#     #     title TEXT,s
#     #     time_off_balance INTEGER,
#     #     address TEXT,
#     #     requested_time_off INTEGER DEFAULT 0
#     # )''')
#     # conn.commit()
#     required_columns = {"id", "name", "time_off_balance", "title", "address","requested_time_off"}

#     # Get existing table schema
#     cursor.execute("PRAGMA table_info(users)")
#     existing_columns = {row[1] for row in cursor.fetchall()}  # Extract column names

#     # Check if any required column is missing
#     if not required_columns.issubset(existing_columns):
#         print("Table structure is incorrect. Recreating the users table...")
        
#         cursor.execute("DROP TABLE IF EXISTS users")  # Remove old table

#         # Create the new table with correct schema
#         cursor.execute("""
#             CREATE TABLE users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 time_off_balance REAL NOT NULL DEFAULT 0,
#                 title TEXT NOT NULL,
#                 address TEXT NOT NULL,
#                 requested_time_off INTEGER DEFAULT 0     
#             )
#         """)
#         conn.commit()
#     conn.close()
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time_off_balance REAL NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            address TEXT NOT NULL,
            requested_time_off INTEGER DEFAULT 0
        )
    ''')

    # Generate 50 dummy user records
    file_path = 'users_data.xlsx'
    df = pd.read_excel(file_path)

    # Convert data to list of tuples
    dummy_users = [
        (
            row['Name'],
            round(row['TimeOffBalance'], 2),
            row['Job'],
            row['Address'].replace('\n', ', '),  # Clean up newlines in addresses
            int(row['RequestedTimeOff'])
        )
        for _, row in df.iterrows()
    ]

    # Insert records into the users table
    cursor.executemany('''
        INSERT INTO users (name, time_off_balance, title, address, requested_time_off)
        VALUES (?, ?, ?, ?, ?)
    ''', dummy_users)

    conn.commit()
    conn.close()
    print("Database initialized and inserted 50 dummy user records.")

init_db()

# Request models
class TimeOffRequest(BaseModel):
    name: str
    from_date: str
    to_date: str

class UpdateTitleRequest(BaseModel):
    name: str
    new_title: str

class UpdateAddressRequest(BaseModel):
    name: str
    new_address: str

class CreateUserRequest(BaseModel):
    name: str
    time_off_balance: int
    title: str
    address: str

@app.get("/export-users/")
def export_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    if not users:
        return {"message": "No data available to export"}

    # Convert to DataFrame for Excel export
    df = pd.DataFrame(users)

    file_path = "users_data.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="users_data.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.delete("/clear-users/")
def clear_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete all records from the users table
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

    return {"message": "All user data has been cleared."}

@app.get("/user_profile_details/{name}",operation_id="userProfileDetails")
def get_user_profile(name: str):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()

    # user = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(dict(user))
    response = dict(user)
	
    return response

# @app.get("/time-off-balance/{name}",operation_id="getTimeOffBalance")
# def get_time_off_balance(name: str):
#     conn = get_db_connection()
#     user = conn.execute("SELECT name, time_off_balance FROM users WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
#     conn.close()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     data = dict(user)

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     # print(data)
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()

# @app.post("/request-time-off",operation_id="requestTimeOffBalance")
# def request_time_off(request: TimeOffRequest):
#     conn = get_db_connection()
#     user = conn.execute("SELECT * FROM users WHERE LOWER(name) =  LOWER(?)", (request.name,)).fetchone()
#     if not user:
#         conn.close()
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # from_date = dt.strptime(request.from_date, "%d-%b-%Y")
#     # to_date = dt.strptime(request.to_date, "%d-%b-%Y")
#     from_date = dt.strptime(request.from_date, "%Y-%m-%d")
#     to_date = dt.strptime(request.to_date, "%Y-%m-%d")


#     days_difference = (to_date - from_date).days
    
#     if days_difference > user["time_off_balance"]:
#         conn.close()
#         raise HTTPException(status_code=200, detail="Not enough time off balance")
    
#     conn.execute("UPDATE users SET requested_time_off = ? WHERE LOWER(name) =  LOWER(?)", (days_difference, request.name))
#     conn.commit()
#     conn.close()
#     data = {"message": "Time off request submitted.", "requested_time_off": days_difference}

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     # print(data)
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()

# @app.put("/update-title",operation_id="updateTitle")
# def update_title(request: UpdateTitleRequest):
#     conn = get_db_connection()
#     result = conn.execute("UPDATE users SET title = ? WHERE LOWER(name) =  LOWER(?)", (request.new_title, request.name))
#     conn.commit()
#     conn.close()
    
#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     data = {"message": "Title updated successfully", "new_title": request.new_title}

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     # print(data)
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()


# @app.put("/update-address",operation_id="updateAddress")
# def update_address(request: UpdateAddressRequest):
#     conn = get_db_connection()
#     result = conn.execute("UPDATE users SET address = ? WHERE LOWER(name) =  LOWER(?)", (request.new_address, request.name))
#     conn.commit()
#     conn.close()
    
#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="User not found")
        
#     data = {"message": "Address updated successfully", "new_address": request.new_address}

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()


@app.post("/create-user",operation_id="createUser")
def create_user(request: CreateUserRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define required columns
    required_columns = {"id", "name", "time_off_balance", "title", "address","requested_time_off"}

    # Get existing table schema
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = {row[1] for row in cursor.fetchall()}  # Extract column names

    # Check if any required column is missing
    if not required_columns.issubset(existing_columns):
        print("Table structure is incorrect. Recreating the users table...")
        
        cursor.execute("DROP TABLE IF EXISTS users")  # Remove old table

        # Create the new table with correct schema
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time_off_balance REAL NOT NULL DEFAULT 0,
                title TEXT NOT NULL,
                address TEXT NOT NULL,
                requested_time_off INTEGER DEFAULT 0     
            )
        """)
        conn.commit()

    # Insert the new user
    cursor.execute(
        "INSERT INTO users (name, time_off_balance, title, address) VALUES (?, ?, ?, ?)", 
        (request.name, request.time_off_balance, request.title, request.address)
    )
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return {"message": "User created successfully", "user_id": user_id}



@app.get("/user_profile_details/{name}",operation_id="userProfileDetails")
def get_user_profile(name: str):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()

    # user = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(dict(user))
    response = dict(user)
	
    return response

@app.get("/time-off-balance/{name}",operation_id="getTimeOffBalance")
def get_time_off_balance(name: str):
    conn = get_db_connection()
    user = conn.execute("SELECT name, time_off_balance FROM users WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data = dict(user)

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # # print(data)
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return data["time_off_balance"]

@app.post("/request-time-off",operation_id="requestTimeOffBalance")
def request_time_off(request: TimeOffRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(name) =  LOWER(?)", (request.name,)).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # from_date = dt.strptime(request.from_date, "%d-%b-%Y")
    # to_date = dt.strptime(request.to_date, "%d-%b-%Y")
    from_date = dt.strptime(request.from_date, "%Y-%m-%d")
    to_date = dt.strptime(request.to_date, "%Y-%m-%d")


    days_difference = (to_date - from_date).days
    
    if days_difference > user["time_off_balance"]:
        conn.close()
        raise HTTPException(status_code=200, detail="Not enough time off balance")
    
    conn.execute("UPDATE users SET requested_time_off = ? WHERE LOWER(name) =  LOWER(?)", (days_difference, request.name))
    conn.commit()
    conn.close()
    data = {"message": "Time off request submitted.", "requested_time_off": days_difference}

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # # print(data)
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return f"{days_difference} days"

@app.put("/update-title",operation_id="updateTitle")
def update_title(request: UpdateTitleRequest):
    conn = get_db_connection()
    result = conn.execute("UPDATE users SET title = ? WHERE LOWER(name) =  LOWER(?)", (request.new_title, request.name))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    data = {"message": "Title updated successfully", "new_title": request.new_title}

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # # print(data)
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return request.new_title


@app.put("/update-address",operation_id="updateAddress")
def update_address(request: UpdateAddressRequest):
    conn = get_db_connection()
    result = conn.execute("UPDATE users SET address = ? WHERE LOWER(name) =  LOWER(?)", (request.new_address, request.name))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
        
    data = {"message": "Address updated successfully", "new_address": request.new_address}

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return request.new_address
