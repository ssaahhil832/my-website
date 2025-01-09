import sqlite3

# Function to handle chatbot responses
def chatbot_response(user_input):
    responses = {
        "hello": "Hi there! How can I help you?",
        "how are you": "I'm just a program, but I'm functioning well! How about you?",
        "your name": "I'm ChatBot, your virtual assistant.",
        "bye": "Goodbye! Have a great day!",
    }

    # Basic response matching
    for key in responses:
        if key in user_input.lower():
            return responses[key]
    
    return "I'm sorry, I didn't understand that. Can you rephrase?"

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect("chatbot.db")  # Create a SQLite database file
    cursor = conn.cursor()

    # Create a table to store chats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            bot_response TEXT
        )
    """)

    conn.commit()
    conn.close()

# Function to save chat to the database
def save_to_database(user_input, bot_response):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_log (user_input, bot_response)
        VALUES (?, ?)
    """, (user_input, bot_response))

    conn.commit()
    conn.close()

# Main chatbot function
def main():
    print("ChatBot: Hello! Type 'bye' to exit.")
    initialize_database()  # Initialize the database

    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("ChatBot: Goodbye! Have a great day!")
            break
        
        # Generate response and save to database
        bot_response = chatbot_response(user_input)
        save_to_database(user_input, bot_response)
        print(f"ChatBot: {bot_response}")

if __name__ == "__main__":
    main()
