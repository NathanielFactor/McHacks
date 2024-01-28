import sqlite3
from datetime import datetime
from bot import ai_response

# Connect to the SQLite database

def connect():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    return connection, cursor

connection, cursor = connect()


def addUser(user_id):
    # Check if user already exists
    connection, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM Calendar WHERE userId = ?", (user_id,))
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        print("hello")
        # User does not exist, add to database
        cursor.execute("INSERT INTO Calendar (userId) VALUES (?)", (user_id,))
        connection.commit()
        return True
    else:
        # User already exists
        return False

def checkTodayEntry(user_id):
    # Check if there is a journal entry for today's date
    connection, cursor = connect()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM JournalEntries WHERE EntryDate = ? AND userId = ?", (today, user_id))
    entry_count = cursor.fetchone()[0]

    if entry_count == 0:
        # No journal entry for today, prompt an error
        return False
    else:
        return True

def addMessage(user_id, message):
    # Fetch id, and JournalEntry

    connection, cursor = connect()
    entry_date = datetime.now().strftime('%Y-%m-%d')
    
    response = ai_response(message)

    # Iterating through rows to get userID's
    if not checkTodayEntry(user_id):
        print(message)
        print(user_id)
        cursor.execute("INSERT INTO JournalEntries (JournalEntry, userId, EntryDate) VALUES (?, ?, ?)",
               (message, user_id, entry_date))


        connection.commit()
        return True
    return False

def gptResponse(user_id, message):
    connection, cursor = connect()
    if addMessage(user_id, message):
        # Get ai response
        gptEmotion = ai_response(message)
        print(gptEmotion)

        # Select id, journalentries
        cursor.execute("SELECT id, JournalEntry FROM JournalEntries")
        rows = cursor.fetchall()

        if rows is not None:
            for row in rows:
                Userid = row["id"]

        for i in range(len(Userid)):
            if user_id == Userid[i]:
                # Insert new message for the specific user
                cursor.execute("UPDATE JournalEntries SET gptmood = ? WHERE id = ?", (gptEmotion, Userid))

        return gptEmotion

def getResponse(user_id, entry_date):
    cursor.execute("SELECT JournalEntry FROM JournalEntries WHERE id = ? AND EntryDate = ?", (user_id, entry_date))
    row = cursor.fetchone()

    if row is not None:
        return row["JournalEntry"]
    else:
        return None
    
def get_messages_by_month(user_id, year, month):
    # Connect to the SQLite database
    connection, cursor = connect()

    # Format year and month as 'YYYY-MM'
    formatted_date = f'{year:04d}-{month:02d}'

    # Execute the SQL query
    query = "SELECT userId, gptmood, JournalEntry, EntryDate FROM JournalEntries WHERE userId = ? AND strftime('%Y-%m', EntryDate) = ?"
    cursor.execute(query, (user_id, formatted_date))

    # Fetch all the rows
    rows = cursor.fetchall()

    # Return the result
    return rows


# Close the database connection
connection.commit()
connection.close()
