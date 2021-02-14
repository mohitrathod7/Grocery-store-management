def header():
    header = ["ID","Date of joining", "First name", "Last name", "Username",
              "Password", "Email ID", "DOB"]
    csvwriter.writerow(header)

def read_last_id(ids):
    #reading last customer ID to create new customer ID while creating account

    # writing to csv file 
    with open(filename, 'r', newline='') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)

        for column in csvreader:
            ids.append(column[0])
            
        ids.pop(0)

    csvfile.close()


# -------------------------------------------------------------------------------
def get_values():
    ids = []
    read_last_id(ids)
    customer_id = (int(ids[-1]) + 1)
    joining_date = time.strftime("%d/%m/%Y")
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]
    email_id = request.form["emailid"]
    date = request.form["date"]
    month = request.form["month"]
    year = request.form["year"]
    birth_date = (str(date) + "/" + str(month) + "/" + str(year))


# -------------------------------------------------------------------------------
def add_row():
    row = [customer_id, joining_date, first_name, last_name, username, password,
           email_id, birth_date]
    csvwriter.writerow(row)

    
# -------------------------------------------------------------------------------
def add_account():
    filename = "database/accounts.csv"

    # writing to csv file 
    with open(filename, 'a', newline='') as csvfile:
                
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile)

        # writing the header
        # header() 
        
        # get all values from form
        get_values()
        
        # writing the row
        add_row()

    csvfile.close()

add_account()
