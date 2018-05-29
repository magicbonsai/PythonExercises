# PythonExercises
Exercises in Multithreading and mySQL operation into the Intercom API as an internship assignment
for Monument Labs 

# Popen

Given a list of commands, run them simultaneously using Popen() of the subprocess library
and return the total, average, max, and min runtimes of all the commands.

This approach utilizes multithreading and a barrier object in the threading library to hold thread execution and release all simultaneously.

# Intercom

Given a user table, go over a mySQL database and create users in Intercom's API.

This theoretical approach uses a wrapper for Intercom and mySQL in python to query for user data in the mySQL database and funnels that data into commands to create users in Intercom.

The code has functionally to query for a limited number of rows at a time in case of large databases and read-locks the database during execution.





