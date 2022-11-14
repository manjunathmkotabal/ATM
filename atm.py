 
from __future__ import print_function
import random
import sys
import os
import mysql.connector
from mysql.connector import errorcode

#update translimit daily
#see if you can get the required attributes in user_verify 
#no of transaction on the given day
#handle amount input for int or not

try:
    cnx = mysql.connector.connect(  user='manju',
                                    password='1234',
                                    host='localhost',
                                    database='atm',
                                )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with db your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print(cnx)
    print()
    cursor = cnx.cursor(buffered=True)

def signup_user():
    #os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        add_user = (f"INSERT INTO user (name,pin) VALUES ('{name}',{pin});")
        cursor.execute(add_user)
        cnx.commit()
    except ValueError:
        print("Bro! , PIN must be Integer :(")


    # sql = (f"select * from user where name='{name}'");
    # cursor.execute(sql)
    # myresult = cursor.fetchall()
 
    # for x in myresult:
    #     print(x)
    # print(cursor.rowcount, "details inserted")

 

def login_user():
    os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        varify_user = (f"select * from user as u where u.name = '{name}' and u.pin = {pin}")
        cursor.execute(varify_user)
        #print(cursor.rowcount)
        if cursor.rowcount:
            print("logged in successfully")
            logged = 1
        else:
            print("Invalid Credentials")
    except ValueError:
        print("Bro! , PIN must be Integer :(")
    


def  deposit_user():
    os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        varify_user = (f"select * from user as u where u.name = '{name}' and u.pin = {pin}")
        cursor.execute(varify_user)
        
        #print(cursor.rowcount)
        if cursor.rowcount:
            query = (f"select limit_of_transactions from user as u where u.name = '{name}' and u.pin = {pin}")
            cursor.execute(query)
            limit = cursor.fetchone()
            limit = limit[0]
            if(limit>0):
                amount = int(input("Enter the amount to deposit:"))
                two_k = int(input("Enter no of 2000's: "))
                half_k = int(input("Enter no of 500's: "))
                two_hundreds= int(input("Enter no of 200's: "))
                hundreds = int(input("Enter no of 100's: "))
                SUM = 2000 * two_k+500*half_k+200*two_hundreds+100*hundreds
                if(SUM == amount):
                    varify_user = (f"update user set balance = balance+{amount},number_of_transactions = number_of_transactions+1,limit_of_transactions=limit_of_transactions-1 where user.pin = {pin}")
                    cursor.execute(varify_user)
                    cnx.commit()
                    upd = (f"update atm set atmamount = atmamount+{amount},two_k = two_k+{two_k},half_k = half_k+{half_k},hundreds = hundreds+{hundreds},two_hundreds = two_hundreds+{two_hundreds};")
                    cursor.execute(upd)
                    cnx.commit()

                    query = (f"select user_id from user as u where u.name = '{name}' and u.pin = {pin}")
                    cursor.execute(query)
                    u_id = cursor.fetchone()
                    u_id = u_id[0]
                    trans_up = (f"INSERT INTO transaction (t_user_id,user_name,withdrawn_or_deposited,amount) VALUES ({u_id},'{name}',True,{amount});")
                    cursor.execute(trans_up)
                    cnx.commit()
                    print("Amount deposited successfully")
                else:
                    print("Bro!, Enter correct denominations :(\n")
            else:
                print("You Daily Limit Of Transactions Has Reached ")

        else:
            print("Invalid Credentials")
    except ValueError:
        print("Bro! , PIN must be Integer :(")
    
 
def withdraw_user():
    os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        varify_user = (f"select * from user as u where u.name = '{name}' and u.pin = {pin}")
        cursor.execute(varify_user)
        
        #print(cursor.rowcount)
        if cursor.rowcount:
            query = (f"select limit_of_transactions from user as u where u.name = '{name}' and u.pin = {pin}")
            cursor.execute(query)
            limit = cursor.fetchone()
            limit = limit[0]
            if(limit>0):
                amount = int(input("Enter the amount to withdraw:"))

                query = (f"select balance from user as u where u.name = '{name}' and u.pin = {pin}")
                cursor.execute(query)
                curbal = cursor.fetchone()
                curbal = curbal[0]
                print("\n")
                print(f"Your Current Balance is {curbal}")

                if curbal>=amount:
                    query = (f"select * from atm;")
                    cursor.execute(query)
                    amt = cursor.fetchone()
                    amtt = amt[0]
                    # two_k = amt[1]
                    # half_k = amt[2]
                    # hundreds = amt[3]
                    # two_hundreds = amt[4]
                    lis = [amt[1],amt[2],amt[3],amt[4]]
                    if(amtt < amount):
                        print("Bro , that much amount is not there in our atm :(\n")
                        return
                    varify_user = (f"update user set balance = balance-{amount},number_of_transactions = number_of_transactions+1,limit_of_transactions=limit_of_transactions-1 where user.pin = {pin}")
                    cursor.execute(varify_user)
                    cnx.commit()

                    query = (f"select user_id from user as u where u.name = '{name}' and u.pin = {pin}")
                    cursor.execute(query)
                    u_id = cursor.fetchone()
                    u_id = u_id[0]


                    trans_up = (f"INSERT INTO transaction (t_user_id,user_name,withdrawn_or_deposited,amount) VALUES ({u_id},'{name}',False,{amount});")
                    cursor.execute(trans_up)
                    cnx.commit()
                    print("Amount withdrawn successfully")
                    avail = curbal-amount
                    print(f"Balance After Transaction {avail}")


                else:
                    print("Insufficient Balance")

            else:
                print("You Daily Limit Of Transactions Has Reached ")

        else:
            print("Invalid Credentials")
    except ValueError:
        print("Bro! , PIN must be Integer :(")
 
def balanceEnquiry():
    os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        varify_user = (f"select * from user as u where u.name = '{name}' and u.pin = {pin}")
        cursor.execute(varify_user)
        
        #print(cursor.rowcount)
        if cursor.rowcount:

            query = (f"select balance from user as u where u.name = '{name}' and u.pin = {pin}")
            cursor.execute(query)
            bal = cursor.fetchone()
            bal = bal[0]
            print(bal)

        else:
            print("Invalid Credentials")
    except ValueError:
        print("Bro! , PIN must be Integer :(")
 
def numberOfTransactions():
    os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        varify_user = (f"select * from user as u where u.name = '{name}' and u.pin = {pin}")
        cursor.execute(varify_user)
        
        #print(cursor.rowcount)
        if cursor.rowcount:
            query = (f"select user_id from user as u where u.name = '{name}' and u.pin = {pin}")
            cursor.execute(query)
            u_id = cursor.fetchone()
            u_id = u_id[0]
            query = (f"select count(transaction_id) from transaction as t group by t_user_id having t_user_id={u_id} ")
            cursor.execute(query)
            if cursor.rowcount:
                count = cursor.fetchone()
                count = count[0]
                print(count)
            else:
                print("0")
        else:
            print("Invalid Credentials")
    except ValueError:
        print("Bro! , PIN must be Integer :(")
    
 
def amountWithdrawnOnPresentDay():
    os.system('cls')
    print('\n')
    name = input("Enter username:")
    try:
        pin = int(input("Enter pin:"))
        varify_user = (f"select * from user as u where u.name = '{name}' and u.pin = {pin}")
        cursor.execute(varify_user)
        
        #print(cursor.rowcount)
        if cursor.rowcount:
            query = (f"select user_id from user as u where u.name = '{name}' and u.pin = {pin}")
            cursor.execute(query)
            u_id = cursor.fetchone()
            u_id = u_id[0]
            query = (f"select sum(amount) from transaction as t where date=curdate() and withdrawn_or_deposited=False group by t_user_id having t_user_id={u_id} ;")
            cursor.execute(query)
            if cursor.rowcount:
                count = cursor.fetchone()
                count = count[0]
                print(count)
            else:
                print("0")
        else:
            print("Invalid Credentials")
    except ValueError:
        print("Bro! , PIN must be Integer :(")
    
    
 
def signup_admin():
    os.system('cls')
    print('\n')
    name = input("Enter admin name:")
    password = input("Enter password:")
    add_admin = (f"INSERT INTO admin (name,password) VALUES ('{name}','{password}');")
    cursor.execute(add_admin)
    cnx.commit()
 
def login_admin():
    os.system('cls')
    print('\n')
    name = input("Enter admin name:")
    password = input("Enter password:")
    varify_user = (f"select * from admin as a where a.name = '{name}' and a.password = '{password}'")
    cursor.execute(varify_user)
    #print(cursor.rowcount)
    if cursor.rowcount:
        print(" admin logged in successfully")
        logged = 1
    else:
        print("Invalid Credentials")

 
def deposit_admin():
    os.system('cls')
    print('\n')
    name = input("Enter admin name:")
    password = input("Enter password:")
    varify_user = (f"select * from admin as a where a.name = '{name}' and a.password = '{password}'")
    cursor.execute(varify_user)
    #print(cursor.rowcount)
    if cursor.rowcount:
        atmamount = int(input("Enter amount to be deposited (max limit 1 Crore): "))
        two_k = int(input("Enter no of 2000's: "))
        half_k = int(input("Enter no of 500's: "))
        two_hundreds= int(input("Enter no of 200's: "))
        hundreds = int(input("Enter no of 100's: "))
        SUM = 2000 * two_k+500*half_k+200*two_hundreds+100*hundreds
        if(SUM == atmamount and SUM<1000000):
                upd = (f"update atm set atmamount = atmamount+{atmamount},two_k = two_k+{two_k},half_k = half_k+{half_k},hundreds = hundreds+{hundreds},two_hundreds = two_hundreds+{two_hundreds};")
                cursor.execute(upd)
                cnx.commit()
        else:
            print("\n Bro!, Enter Correct denomination ;)")

    else:
        print("Invalid Credentials")


# def setTransactionLimit():
#     os.system('cls')
#     print('\n')
#     limit = int(input("Enter transaction limit"))
#     translimit = limit
 
# def setAmountLimit():
#     os.system('cls')
#     print('\n')
#     limit = int(input("Enter transaction limit"))
#     amountlimit = limit
    
 

def main():
    while True:
        os.system('cls')
        print("\n")
        print("******* WELCOME TO BANK OF GreedyMens *******")
        print("---------------------------------------------\n")
        print("Are You ADMIN or USER?\n")
        print("1. USER")
        print("2. ADMIN")
        print("3. EXIT")
        print()
        choice1 = int(input("Enter Your Choice(1/2): "))
        if(choice1 == 1):
            os.system('cls')
            while True:
                print("\n")
                print("you wanna?\n")
                print("     1.Sign Up")
                print("     2.Log In")
                print("     3.Deposit")
                print("     4.Withdraw")
                print("     5.Enquire Balance")
                print("     6.See No Of Transactions")
                print("     7.See Amount Withdrawn Today")
                print("     8.Go To Main Menu \n")
                choice2 = int(input("Enter Your Choice: "))
                if(choice2 == 1):
                    signup_user()
                elif(choice2 == 2):
                    login_user()
                elif choice2 == 3 :#and logged:
                    deposit_user()
                elif choice2 == 4:# and logged:
                    withdraw_user()
                elif choice2 == 5:# and logged:
                    balanceEnquiry()
                elif choice2 == 6:# and logged:
                    numberOfTransactions()
                elif choice2 == 7 :#and logged:
                    amountWithdrawnOnPresentDay()
                else:
                    logged = 0
                    break
        elif(choice1 == 2):
            os.system('cls')
            while True:
                print("\n")
                print("you wanna?\n")
                print("     1.Sign Up")
                print("     2.Login")
                print("     3.Deposit")
                print("     4.Go To Main Menu \n")

                choice2 = int(input("Enter Your Choice: "))
                if choice2 == 1:
                    signup_admin()
                elif choice2 == 2:
                    login_admin()
                elif choice2 == 3:
                    deposit_admin()
                else:
                    logged=0
                    break
        else:
            os.system('cls')
            print("\nThank you for choosing us as your bank , visit again :)")
            cnx.close()
            sys.exit()


if __name__=='__main__':
    main()
