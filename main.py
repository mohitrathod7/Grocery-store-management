from flask import *
from nav import *
from footer import *
import pandas as pd
import numpy as np
import csv, time, os


app = Flask(__name__)

# -------------------------------------------------------------------------------
def header():
    header = ["ID", "Date of joining", "First name", "Last name", "Username",
              "Password", "Gender", "Email ID", "Contact Number", "DOB"]
    csvwriter.writerow(header)

    
# -------------------------------------------------------------------------------
def read_last_id(ids):
    #reading last customer ID to create new customer ID while creating account
    filename = "database/accounts.csv"
    # writing to csv file 
    with open(filename, 'r', newline='') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)

        for column in csvreader:
            ids.append(column[0])
            
        ids.pop(0)
        
    csvfile.close()


# -------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template("home.html", user=user_var, navstyle=nav_style, footerstyle=footer_style)


# -------------------------------------------------------------------------------
@app.route('/about')
def about():
    return render_template("about.html", user=user_var, navstyle=nav_style, footerstyle=footer_style)


# -------------------------------------------------------------------------------
@app.route('/feedback')
def feedback():        
    if signed == True:
        # get Email ID
        filename = "database/accounts.csv"     
        df = pd.read_csv(filename)

        for row in df.index: 
            indices = list(np.where(df["Username"] == user_var)[0])
            index = df.iloc[indices].index.tolist()[0]

        email_id = df["Email ID"][index]
        yes = "readonly"
        return render_template("feedback.html", user=user_var, navstyle=nav_style,
            feedback_username=user_var, feedback_emailid=email_id,
            isreadonly = yes, footerstyle=footer_style)
    else:
        return render_template("user.html", user=user_var, navstyle=nav_style, footerstyle=footer_style, errorText="Sign In to give feedback")


# -------------------------------------------------------------------------------
@app.route('/dashboard')        
def dashboard():
    filename = "database/accounts.csv"     
    df = pd.read_csv(filename)

    for row in df.index: 
        indices = list(np.where(df["Username"] == user_var)[0])
        index = df.iloc[indices].index.tolist()[0]
    
    # Loading Basic Details
    firstname = df["First name"][index]
    lastname = df["Last name"][index]
    number = df["Contact Number"][index]
    c_id = df["ID"][index]
    date_of_birth = df["DOB"][index]
    email = df["Email ID"][index]
    gen = df["Gender"][index]

    # Loading Order history     
    df = pd.read_csv("database/users/" + user_var + ".csv")

    bookingID = df["Booking ID"].tolist()
    dates = df["Date"].tolist()
    times = df["Time"].tolist()
    storeNames = df["Store Name"].tolist()
    if len(bookingID) == 0:
        displayAttr1 = "none"
        displayAttr2 = "block"
    else:
        displayAttr1 = "flex"
        displayAttr2 = "none"

    return render_template("dashboard.html", user=user_var, navstyle=nav_style,
                           f_name=firstname, l_name=lastname, contact=number, cid=c_id,
                           dob=date_of_birth, gender=gen, mail=email, display1="show",
                           display2="hide", display3="hide", display4="hide", footerstyle=footer_style,
                           len=len(bookingID), bookingID=bookingID, dates=dates, times=times,
                           storeNames=storeNames, display_order=displayAttr1, display_message=displayAttr2)


# -------------------------------------------------------------------------------
@app.route('/stats')        
def stats():
    return render_template("stats.html", user=user_var, navstyle=nav_style, footerstyle=footer_style)


# -------------------------------------------------------------------------------    
@app.route('/user')
def user():
    if signed != True:
        return render_template("user.html", user=user_var, navstyle=nav_style, footerstyle=footer_style), signed
    else:
        if user_var == "admin":
            return redirect(url_for("stats"))
        else:
            return redirect(url_for("dashboard"))

                                
# -------------------------------------------------------------------------------
@app.route('/gettoken', methods=['POST', 'GET'])
def getToken():
    if signed != True:
        text = "Sign In to get Token !!!"
        return render_template("user.html", user=user_var, errorText=text, navstyle=nav_style, footerstyle=footer_style)
    else:
        days30_month = [4, 6, 9, 11] 
        days31_month = [1, 3, 5, 7, 8, 10, 12]
        leap_year = [2020, 2024, 2028, 2032, 2036, 2040, 2044, 2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084, 2088, 2092, 2096]
        
        
        date = int(time.strftime("%d"))
        month = int(time.strftime("%m"))
        year = int(time.strftime("%Y"))
        max_date = date
        max_month = month
        max_year = year

        if (year in leap_year):
            # checking that next year value is same or not 
            if date == 31 and month == 12:
                max_year = year + 1
            elif date == 30 and month == 12:
                max_year = year + 1
            else:
                max_year = year

            # Now checking for months
            if (date <= 29) and (month == 2):
                if date == 28:
                    max_date = 1
                    max_month = 3
                elif  date == 29:
                    max_date = 2
                    max_month = 3
                else:
                    max_date += 2
                    max_month = month + 1
                    
            elif (date <= 30) and (month in days30_month):
                if date == 29:
                    max_date = 1
                    max_month = month + 1
                elif date == 30:
                    max_date = 2
                    max_month = month + 1
                else:
                    max_date += 2
                    max_month = month
                    
            elif (date <= 31) and (month in days31_month):
                if date == 30:
                    max_date = 1
                    max_month = month + 1
                elif date == 31:
                    max_date = 2
                    max_month = month + 1
                else:
                    max_date += 2
                    max_month = month

        elif (year not in leap_year):
            # checking that next year value is same or not 
            if date == 31 and month == 12:
                max_year = year + 1
            elif date == 30 and month == 12:
                max_year = year + 1
            else:
                max_year = year
                
            # Now checking for months
            if (date <= 28) and (month == 2):
                if date == 27:
                    max_date = 1
                    max_month = 3
                elif  date == 28:
                    max_date = 2
                    max_month = 3
                else:
                    max_date += 2
                    max_month = month + 1
                    
            elif (date <= 30) and (month in days30_month):
                if date == 29:
                    max_date = 1
                    max_month = month + 1
                elif date == 30:
                    max_date = 2
                    max_month = month + 1
                else:
                    max_date += 2
                    max_month = month
                    
            elif (date <= 31) and (month in days31_month):
                if date == 30:
                    max_date = 1
                    max_month = month + 1
                elif date == 31:
                    max_date = 2
                    max_month = month + 1
                else:
                    max_date += 2
                    max_month = month

        #print(date, month, year,)
        #print(max_date, max_month, max_year)
                    
        return render_template("token.html", user=user_var, navstyle=nav_style, today_date=date,
                               future_date=max_date, today_month=month, future_month=max_month,
                               today_year=year, future_year=max_year, footerstyle=footer_style)


# -------------------------------------------------------------------------------
@app.route('/booktoken', methods=['post'])
def bookToken():
    booking_id = "#"
    store = ""
    __ = ""
    username = request.form["username"]
    email_id = request.form["emailid"]
    contact = request.form["contact"]
    state = request.form["state"]
    slot = request.form["slot"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    storelist= [request.form["g-store"], request.form["k-store"], request.form["m-store"], request.form["r-store"]]
    for i in storelist:
        if i != "Select Store":
            store = i
    
    timelist = [request.form["m-time"], request.form["a-time"], request.form["e-time"], request.form["n-time"]]
    for i in timelist:
        if i != "NAN":
            time = i

    date = request.form["date"]
    month = request.form["month"]
    year = request.form["year"]
    if int(month) <= 10:
        full_date = str(date + "/0" + month + "/" + year)
    else:
        full_date = str(date + "/" + month + "/" + year)


    filename = "database/stores/" + state + "/" + store + ".csv"

    if slot == "Morning":
        __ = " : AM"
    elif slot == ("Afternoon" or "Evening" or "Night"):
        __ = " : PM"

    df = pd.read_csv(filename)
    date_list = list(df.loc[:,"Full Date"])

    # checking presence of today's date column value 
    if full_date in date_list:
        pass
    else:     
        filename = "database/stores/" + state + "/" + store + ".csv"
        # writing to csv file 
        with open(filename, 'a', newline='') as csvfile:
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile)
            # writing the row
            csvwriter.writerow([full_date,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        csvfile.close()

    df = pd.read_csv(filename)

    for row in df.index: 
        indices = list(np.where(df["Full Date"] == full_date)[0])
        index = df.iloc[indices].index.tolist()[0]

    # increasing slots booked in store's database
    no_of_slots = int(df[time][index])
    df[time][index] = int(no_of_slots+1)

    #adding new booking to total booking in store
    total_bookings = int(df["Total bookings"][index])
    df["Total bookings"][index] = int(total_bookings+1)

    df.to_csv(filename, index=False)

    # adding transaction to customer's database
    filename = "database/users/" + username + ".csv"
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([booking_id, full_date, time, store])
    csvfile.close()

    booking_status = "Booked"

    return render_template("status.html", user=user_var, navstyle=nav_style, booked=booking_status,
                            bookingid="NAN", bookingdate=full_date, bookingtime=time+__,
                            storename=store, fname=first_name, lname=last_name, footerstyle=footer_style)

    email_id = ""
    contact = ""
    state = ""
    store = ""
    time = ""
    date = ""
    month = ""
    year = ""
    first_name = ""
    last_name = ""
    slot = ""
    full_date = ""

# -------------------------------------------------------------------------------
@app.route('/createaccount')
def createAccount():
    return render_template("createaccount.html", user=user_var, navstyle=nav_style, footerstyle=footer_style)


# -------------------------------------------------------------------------------
@app.route('/submit', methods=['post'])
def submitAccount():
    global email_id, first_name, last_name
    joining_date = time.strftime("%d/%m/%Y")
    first_name = request.form["firstname"].capitalize()
    last_name = request.form["lastname"].capitalize()
    username = request.form["username"]
    password = request.form["password"]
    email_id = request.form["emailid"].lower()
    gender = request.form["gender"].capitalize()
    contact = request.form["contact"]
    date = request.form["date"]
    month = request.form["month"]
    year = request.form["year"]
    birth_date = (str(date) + "/" + str(month) + "/" + str(year))

    ids = []
    read_last_id(ids)
    customer_id = (int(ids[-1]) + 1)

    
    if len(contact) == 10:
        if (contact[0] == "7" or contact[0] == "8" or contact[0] == "9"):
            for i in contact[1:]:
                if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    pass
        else:
            msg = "Contact Number should start with 7 or 8 or 9"
            return render_template("createaccount.html", user=user_var, message=msg, navstyle=nav_style)
    else:
        msg = "Contact Number must contain 10 digits !"
        return render_template("createaccount.html", user=user_var, message=msg, navstyle=nav_style)

    row = [customer_id, joining_date, first_name, last_name, username, password,
           gender, email_id, contact, birth_date]

    filename = "database/accounts.csv"

    # writing to csv file 
    with open(filename, 'a', newline='') as csvfile:
                
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow("")
        # writing the row
        csvwriter.writerow(row)

    csvfile.close()

    path = "database/users/"
    name = username + ".csv"
    filename = path + name
    with open(filename, "a", newline='') as newfile:
        csvwriter = csv.writer(newfile) 
        csvwriter.writerow(["Booking ID", "Visiting Time", "Visiting Date", "Transaction Time", "Transaction Date", "Store Name"])
    newfile.close()
    
    msg = "Account created successfully"
    return render_template("createaccount.html", user=user_var, message=msg, navstyle=nav_style, footerstyle=footer_style), email_id


# -------------------------------------------------------------------------------
@app.route('/signin', methods=['post'])
def signIn():
    username = request.form["text"]
    password = request.form["password"]

    accounts = {}
    
    filename = "database/accounts.csv"
    # writing to csv file 
    with open(filename, 'r', newline='') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            accounts[row[4]] = row[5]

        del accounts['Username']
        
    csvfile.close()
    
    if username in accounts:
        if password == accounts.get(username):
            global user_var
            user_var = username
            global signed
            signed = True
            return redirect(url_for("home"))
        else:
            msg = "Incorrect password !"
            return render_template("user.html", message=msg, navstyle=nav_style, user=user_var, footerstyle=footer_style)
    else:
        msg = "Username : " + username + " does not exist."
        return render_template("user.html", message=msg, navstyle=nav_style, footerstyle=footer_style)


# -------------------------------------------------------------------------------
@app.route('/signout', methods=['post'])
def signOut():
    global signed, user_var
    signed = False
    user_var = "Sign In"
    return redirect(url_for("home"))
    

# -------------------------------------------------------------------------------
@app.route('/changenumber', methods=['post'])
def changeNumber():
    current_number = request.form["current-number"]
    new_number = request.form["new-number"]

    filename = "database/accounts.csv"     
    df = pd.read_csv(filename)

    for row in df.index: 
        indices = list(np.where(df["Username"] == user_var)[0])
        index = df.iloc[indices].index.tolist()[0]

    #adding new booking to total booking in store
    firstname = df["First name"][index]
    lastname = df["Last name"][index]
    number = df["Contact Number"][index]
    c_id = df["ID"][index]
    date_of_birth = df["DOB"][index]
    email = df["Email ID"][index]
    gen = df["Gender"][index]

    try:   
        filename = "database/accounts.csv"     
        df = pd.read_csv(filename)
        
        for row in df.index: 
            indices = list(np.where(df["Contact Number"] == int(current_number))[0])
            index = df.iloc[indices].index.tolist()[0]

        df["Contact Number"][index] = new_number
        
        df.to_csv(filename, index=False)
        msg = "Number Change Successfully !"
        return redirect(url_for(dashboard))
    
    except IndexError:
        msg = "Number does not exist"
        return redirect(url_for(dashboard))


# -------------------------------------------------------------------------------
@app.route('/changepassword', methods=['post'])
def changePassword():
    current_password = request.form["current-password"]
    new_password = request.form["new-password"]

    filename = "database/accounts.csv"     
    df = pd.read_csv(filename)

    for row in df.index: 
        indices = list(np.where(df["Username"] == user_var)[0])
        index = df.iloc[indices].index.tolist()[0]

    try:
        if new_password != current_password:
            for row in df.index: 
                indices = list(np.where(df["Password"] == current_password)[0])            
                index = df.iloc[indices].index.tolist()[0]

            df["Password"][index] = new_password
            df.to_csv(filename, index=False)
            return redirect(url_for(home))
    except TypeError:
        return redirect(url_for(home))


# -------------------------------------------------------------------------------
@app.route('/sendfeedback', methods=['post'])
def sendFeedback():
    feedback_username = request.form["feedback-username"]
    feedback_email = request.form["feedback-emailid"]
    feedback_message = request.form["feedback-message"]
    
    # get today's date
    date = time.strftime("%d") + "/" + time.strftime("%m") + "/" + time.strftime("%y")

    # saving feedback message to database
    filename = "database/feedback.csv"
    with open(filename, 'a', newline='') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)    
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow([date, feedback_username, feedback_email, feedback_message])
            
    csvfile.close()

    return render_template("feedbacksent.html", user=user_var, navstyle=nav_style, footerstyle=footer_style)


# -------------------------------------------------------------------------------
if __name__ == "__main__":
    global signed, user_var
    
    signed = False
    user_var = "Sign In"

    app.run(use_reloader = True)
# -------------------------------------------------------------------------------