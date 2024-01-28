import sqlite3
from datetime import datetime
from bot import ai_response

# Connect to the SQLite database
connection = sqlite3.connect('your_database_file.db')
cursor = connection.cursor()

def checkTodayEntry():
    # Check if there is a journal entry for today's date
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM JournalEntries WHERE EntryDate = ?", (today,))
    entry_count = cursor.fetchone()[0]

    if entry_count == 0:
        # No journal entry for today, prompt an error
        return False
    else:
        return True

def addMessage(user_id, message):
    # Fetch id, and JournalEntry
    cursor.execute("SELECT id, JournalEntry FROM JournalEntries")
    rows = cursor.fetchall()

    # Iterating through rows to get userID's
    if rows is not None:
        for row in rows:
            Userid = row["id"]

            # Making sure there is no journal entry on present day
            if checkTodayEntry():
                for i in range(len(Userid)):
                    if user_id == Userid[i]:
                        # Add user message to database
                        cursor.execute("UPDATE JournalEntries SET JournalEntry = ? WHERE id = ?", (message, Userid))
                        return True
    return False

def gptResponse(user_id, message):
    if addMessage(user_id, message):
        # Get ai response
        gptEmotion = ai_response(message)

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

# Close the database connection
connection.commit()
connection.close()
