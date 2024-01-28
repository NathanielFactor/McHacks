import sqlite3
from datetime import datetime
from bot import ai_response

def connect_to_database(database_file):
    return sqlite3.connect(database_file)

def check_today_entry(cursor):
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT id FROM JournalEntries WHERE EntryDate = ? LIMIT 1", (today,))
    return cursor.fetchone() is not None

def add_message(cursor, user_id, message):
    if check_today_entry(cursor):
        cursor.execute("UPDATE JournalEntries SET JournalEntry = ? WHERE id = ?", (message, user_id))
        return True
    return False

def gpt_response(cursor, user_id, message):
    if add_message(cursor, user_id, message):
        gpt_emotion = ai_response(message)
        cursor.execute("UPDATE JournalEntries SET gptmood = ? WHERE id = ?", (gpt_emotion, user_id))
        return gpt_emotion
    return None

def get_response(cursor, user_id, entry_date):
    cursor.execute("SELECT JournalEntry FROM JournalEntries WHERE id = ? AND EntryDate = ?", (user_id, entry_date))
    row = cursor.fetchone()
    return row["JournalEntry"] if row else None

def main():
    database_file = 'your_database_file.db'
    with connect_to_database(database_file) as connection:
        cursor = connection.cursor()
        
        user_id = 'example_user_id'
        message = 'example_message'
        entry_date = 'example_entry_date'

        response = gpt_response(cursor, user_id, message)
        print(f'GPT Response: {response}')

        retrieved_response = get_response(cursor, user_id, entry_date)
        print(f'Retrieved Response: {retrieved_response}')

if __name__ == "__main__":
    main()
