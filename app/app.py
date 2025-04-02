from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
IMAGE_FROM_ENV = os.environ.get('APP_IMG')  # S3 URL or S3 bucket and object key
NAME_FROM_ENV = os.environ.get('APP_NAMES')
DBPORT = int(os.environ.get("DBPORT"))

# Function to get a fresh database connection
def get_db_connection():
    return connections.Connection(
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPWD,
        db=DATABASE
    )

def DownloadImage():
    if IMAGE_FROM_ENV:
        try:
            # Parse s3 url
            s3_url = IMAGE_FROM_ENV.strip()
            s3 = boto3.client('s3')
            
            # Extract bucket and key from the s3_url
            parsed_url = s3_url.replace("s3://", "").split("/")
            bucket_name = parsed_url[0]
            object_key = "/".join(parsed_url[1:])
            
            # Specify the local file path to save the image
            image_path = os.path.join(app.static_folder, 'bg-img.jpg')
            
            # Download the file from S3 to local static folder
            s3.download_file(bucket_name, object_key, image_path)
            print(f"Image successfully downloaded to {image_path}")
        except NoCredentialsError:
            print("Credentials not available for AWS S3.")
        except Exception as e:
            print(f"Error downloading image from S3: {str(e)}")
    else:
        print("No image URL set in the environment variable.")

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=IMAGE_FROM_ENV, name=NAME_FROM_ENV)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image=IMAGE_FROM_ENV, name=NAME_FROM_ENV)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    
    # Create a fresh database connection for this request
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = first_name + " " + last_name
    finally:
        cursor.close()
        db_conn.close()  # Close the connection after use

    print("All modification done...")
    return render_template('addempoutput.html', empname=emp_name, image=IMAGE_FROM_ENV, name=NAME_FROM_ENV)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image=IMAGE_FROM_ENV, name=NAME_FROM_ENV)

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    
    # Create a fresh database connection for this request
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        
        # The rest of your code, as it was
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            output["error"] = "Employee not found"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db_conn.close()  # Close the connection after use

    return render_template("getempoutput.html", 
                           id=output.get("emp_id", ""), 
                           fname=output.get("first_name", ""), 
                           lname=output.get("last_name", ""), 
                           interest=output.get("primary_skills", ""), 
                           location=output.get("location", ""),
                           error=output.get("error", ""),
                           image=IMAGE_FROM_ENV,
                           name=NAME_FROM_ENV)

if __name__ == '__main__':
    # Check if background image is in environment variables
    if IMAGE_FROM_ENV:
        print("Background image URL from environment variable =" + IMAGE_FROM_ENV)
        # Download the image from the URL when the application starts
        DownloadImage()
    else:
        print("No environment variable set for background image")

    app.run(host='0.0.0.0', port=81, debug=True)
