from intercom.client import Client
import mysql.connector

# Access the intercom API w/o actual key
intercom = Client(personal_access_token = 'placeholder' )

# Alex Zhu, May 2018

# This implementation of the problem uses the python-intercom wrapper package and mysql-connector package
# Grabs users from the mysql database and funnels the data to create users within the intercom API

# simple script to go over user database cand take that information to create users in intercom.
# simpleScript takes input "n" which can be used to limit # of records grabbed at one time in case of larger database.
# Defaults to querying all records in cases where no input is given for "n"
# Additionally acquire a read lock in beginning to ensure data integrity

def simpleScript(n):

    cnx = mysql.connector.connect(user = 'Dennis', database = 'users')
    cursor = cnx.cursor()
    # lock table from being written by acquiring a read lock
    query = ("LOCK TABLE users READ")
    cursor.execute(query)

    if n == None:
        query = ("SELECT * FROM users")
        cursor.execute(query)
        # create users in intercom given results from query
        for (name, id, email) in cursor:
            user = intercom.users.create(email=email, name=name, id=id)
    else:
        # get the count of the database first
        query = ("SELECT COUNT(*) FROM users")
        count = cursor.execute(query)
        endpart = count % n
        # creates how many iterators to go through each n sized chunk
        iters = (count - endpart) / n
        for i in range(iters - 1):
            query = ("SELECT * FROM users ORDER BY id LIMIT %s, %s")
            cursor.execute(query, i*n, (i+1)*n)
            for (name, id, email) in cursor:
                user = intercom.users.create(email=email, name=name, id=id)
        # Perform the last calculation on the last dangling chunk of records
        query = ("SELECT * FROM users ORDER BY id LIMIT %s, %s")
        cursor.execute(query, iters * n, (iters * n) + endpart)
        for (name, id, email) in cursor:
            user = intercom.users.create(email=email, name=name, id=id)

    # Release the table after finishing
    query = ("UNLOCK TABLES")
    cursor.execute(query)
    # Finished w/ mysql; close cnx and cursor.
    cursor.close()
    cnx.close()

    return

if __name__ == '__main__':

    simpleScript()
    simpleScript(1000)




