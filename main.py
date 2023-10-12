# Importing modules
from bot import bot
from background import keep_alive


# Main function
def main():
    bot.polling(non_stop=True)


# Dot of entry
if __name__ == '__main__':
    keep_alive()
    main()
