from flask import Flask,render_template,request,url_for,session,redirect,jsonify
import psycopg2


app = Flask(__name__)
# postgressql_url = "postgres://pqwidroiztnmka:f92f9d971857884f0b79b423490f337e18ec9de14ec8233c6d3e3e4f0b703dac@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/d10l089lo6jq4n"
postgressql_url = "postgres://rlqrzgzdhjvlyd:a4cf6f365b690986f881b5ff776bd97ecb6236099a256bcc58024856974e6f69@ec2-34-194-215-27.compute-1.amazonaws.com:5432/da19esl0rg7tu0"
app.secret_key ="bookstore"



connection = psycopg2.connect(postgressql_url)
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE users (email VARCHAR(100) NOT NULL, name VARCHAR(100) NOT NULL,password VARCHAR(100) NOT NULL);")
except:
    pass
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE reviews (review_count INT NOT NULL, comment VARCHAR(200) NOT NULL,isbn VARCHAR(100) NOT NULL);")
except:
    pass

@app.route('/')
def home():  
    if "user" in session:
        user =session["user"]
    else:
        user= None
    return render_template("app.html",user=user) 


@app.route('/registration',methods=["GET","POST"])
def registration():
    if request.method == "POST":
        email=request.form.get("email")
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT *FROM users WHERE email = %s",(email,))
                
                checkUser = [row for row in cursor]
                if(len(checkUser)>0):
                    error="User registered already"
                    return render_template("registration.html",error=error)
                else:                    
                  
                    cursor.execute("INSERT INTO users VALUES(%s,%s,%s);",
                        (
                        request.form.get("email"),   
                        request.form.get("name"),  
                        request.form.get("password"),
                        )
                    )   
                    user = request.form.get("name")
                    session["user"]=user
                    return redirect(url_for("home",user=user)) 
    connection.commit()
    return render_template("registration.html") 


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form.get("name")
        password = request.form.get("password")
        if user == None or user == "":
            return render_template("login",error="Field is not allowed to be empty")
        else:
            error=""
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT *FROM users WHERE name = %s and password =%s",(user,password))  
                    record = ([row for row in cursor])
                    if len(record) > 0:
                        session["user"]=user
                        return redirect(url_for("home"))
                    else:
                        error="User name or password is not correct"
                        
                    if error:
                        return render_template("login.html",error = error)
                    else:
                        return redirect(url_for("home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))


@app.route('/search',methods=['GET','POST'])
def search():
    book=""
    query = request.form.get("search") 
    if "user" in session:
        user =session["user"]
    else:
        user= None
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT *FROM books WHERE isbn = %s OR title ILIKE %s OR author ILIKE %s OR year = %s ",( query,'%' + query + '%','%' + query + '%', query ))
            book = ([row for row in cursor])
            if(len(book)<1):
                return render_template("search.html",noproduct="No Product Found")
            else:
                if request.headers['Content-Type'] == 'application/json':
                    return jsonify(book)
                else:
                    return render_template("search.html",response=book,user=user)
                            

@app.route('/bookpage/<isbn>',methods=['GET','POST'])
def bookpage(isbn):
    book=""
    if "user" in session:
        user =session["user"]
    else:
        user= None
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT *FROM books WHERE isbn = %s",(isbn, ))
            book = ([row for row in cursor])
            if(len(book)<1):
                return render_template("search.html",noproduct="No Product Found")
            else:
                return render_template("bookpage.html",response=book,user=user)



@app.route('/review',methods=['GET','POST'])
def review():
    isbn= request.form.get("isbnNo"),
    if request.method == "POST":
        with connection:
            with connection.cursor() as cursor:
                                
                    cursor.execute("INSERT INTO reviews VALUES(%s,%s,%s);",
                        (
                        request.form.get("range"),   
                        request.form.get("comment"),
                        request.form.get("isbnNo"),                        
                        )
                    )   
                   
                    return redirect(url_for("home",)) 
    connection.commit()
    return render_template("bookpage.html",isbn=isbn) 
                          
@app.errorhandler(404)
def page_not_found(e):
        return render_template("error.html"),404

