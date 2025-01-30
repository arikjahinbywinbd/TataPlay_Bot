import telebot  # Import the telebot library
from dotenv import load_dotenv  # Import dotenv to load the .env file
import os  # Import os to access environment variables

# Load environment variables from .env file
load_dotenv()

# Retrieve the API Token from the .env file
API_TOKEN = os.getenv("7841656270:AAGEIU6KthRCZLaVWUbNjIhhnOXcrktbRyE")


# Initialize the bot with the API token
bot = telebot.TeleBot(API_TOKEN)

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalamu alaikum. Welcome! How can I assist you today?")

# /help command handler
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Available commands:\n"
                          "/start - Start the bot\n"
                          "/help - List available commands\n"
                          "/status - Check bot status\n"
                          "/webdl - Perform a web download task\n"
                          "/getfile <filename> - Retrieve a file by name")

# /status command handler
@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, "The bot is running and ready to assist you!")

# /webdl command handler
@bot.message_handler(commands=['webdl'])
def webdl_command(message):
    try:
        args = message.text.split()
        category, start_time, end_time, title = None, None, None, None

        for i, arg in enumerate(args):
            if arg == '-c' and i + 1 < len(args):
                category = args[i + 1]
            elif arg == '-ss' and i + 1 < len(args):
                start_time = datetime.strptime(args[i + 1], "%m/%d/%Y+%H:%M:%S")
            elif arg == '-to' and i + 1 < len(args):
                end_time = datetime.strptime(args[i + 1], "%m/%d/%Y+%H:%M:%S")
            elif arg == '-title' and i + 1 < len(args):
                title = args[i + 1]

        if not all([category, start_time, end_time, title]):
            bot.reply_to(message, "Missing required parameters. Use: "
                                  "/webdl -c <Category> -ss <StartTime> -to <EndTime> -title <Title>")
           

       
# Validate the arguments
    if not category or not start_time or not end_time or not title:
        bot.reply_to(message, "Missing required parameters. Use the correct format: /webdl -c <Category> -ss <StartTime> -to <EndTime> -title <Title>")
        return

    # Example of responding with the parsed information
    bot.reply_to(message, f"Processing download:\n"
                          f"Category: {category}\n"
                          f"Start Time: {start_time}\n"
                          f"End Time: {end_time}\n"
                          f"Title: {title}")

# Define the /getfile command handler
@bot.message_handler(commands=['getfile'])
def get_file_command(message):
    # The file name is passed as an argument to the command
    file_name = message.text[len('/getfile '):].strip()  # Extract the file name from the command

    if not file_name:
        bot.reply_to(message, "Please provide a file name. Example: /getfile recorded_video.mp4")
        return

    # Example: Retrieve the file from the channel
    # Here, you should specify the logic to find the file in the channel.
    # For demonstration, we're assuming the file is already in a list of files in the channel
    # In practice, you'd fetch the file using a direct link or get the file ID.
    
    try:
        # Send the file from the bot's storage (assuming it's uploaded to the bot or can be fetched by URL)
        bot.send_document(message.chat.id, open(file_name, 'rb'))  # This is just an example
    except FileNotFoundError:
        bot.reply_to(message, f"File {file_name} not found. Please check the file name.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Start the bot and keep it running
if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()  # Keeps the bot running and listening for messages