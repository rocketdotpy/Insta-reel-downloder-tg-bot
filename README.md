
# Instagram Reel Downloader Telegram Bot

A powerful and user-friendly Telegram bot to download public Instagram Reels directly in Telegram. Built with **Python**, **Telebot (pyTelegramBotAPI)**, and **Instaloader**.

## Features

- 📥 Download Instagram Reels directly from a link  
- 🔍 Automatically detects and extracts reel information  
- 🎥 Supports HD quality video download  
- ⚙️ Inline quality selection (expandable)  
- ⚡ Fast response and clean interface with emoji UI  
- ❌ Cancel button to stop downloads  
- ✅ Sends the reel right in chat (streaming enabled)  
- 🧹 Automatic file cleanup after sending  

## Demo

![Demo Screenshot](demo.gif) *(Add demo gif if available)*

## How to Use

1. Start the bot on Telegram
2. Send a valid Instagram Reel link (public reels only)
3. Choose the video quality
4. Receive your reel directly in chat!

Example:
```
https://www.instagram.com/reel/CrK3JXyJQ5X/
```

## Installation

```bash
git clone https://github.com/harshdotpy/Insta-reel-downloder-tg-bot.git
cd Insta-reel-downloder-tg-bot
pip install -r requirements.txt
```

> Add your Telegram bot token in the script:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

## Dependencies

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Instaloader](https://instaloader.github.io/)
- Python 3.8+

```bash
pip install instaloader pyTelegramBotAPI
```

## Notes

- Works only with **public reels**
- Quality options are limited due to Instaloader constraints
- Direct video URL streaming (without downloading) is not supported due to Instagramâ€™s limitations

## Author

Made with passion by [@rocket_0_07](https://t.me/rocket_0_07)

Feel free to contribute, suggest features, or report bugs!

## License

MIT License
