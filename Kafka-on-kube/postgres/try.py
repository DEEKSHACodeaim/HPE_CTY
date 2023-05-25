from flask import Flask
import psycopg2

app = Flask(__name__)

# PostgreSQL connection details
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'c8JQr7QolG'
POSTGRES_HOST = 'my-postgresql.default.svc.cluster.local'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'threadweaver'

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DB
)

# Define a route to test the database connection
@app.route('/')
def index():
    with conn.cursor() as cur:
        cur.execute('SELECT version()')
        result = cur.fetchone()
        return f'Connected to PostgreSQL {result[0]}'

@app.route('/auth')
def auth():
    cur = conn.cursor()

    # Define the insert statement
    insert_stmt = "INSERT INTO auth_user (id,password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (999,'pbkdf2_sha256$260000$d82Kab7kLCwPiPaALgTkeC$ahnGOexWl9ypQB7kdI07SlEqnd8qvSGpgeSsbqw8Dx4=', NULL, False, 'sanju', '', '', 'sanju@gmail.com', False, True, '2023-04-18 04:33:08.534379');"

    # Execute the insert statement with the values
    cur.execute(insert_stmt)

    # Get the number of rows affected by the previous insert statement
    row_count = cur.rowcount

    # Commit the transaction
    conn.commit()

    # Close the cursor and database connection
    cur.close()
    conn.close()

    # Check if the insert was successful
    if row_count == 1:
        print("Insert was successful")
    else:
        print("Insert failed")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

