import os
import re
import telebot
from telebot import types
from instaloader import Instaloader, Post

# Initialize Instaloader and Telebot
L = Instaloader()
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Validate Instagram Reel URL
def is_valid_instagram_url(url: str) -> bool:
    return re.match(r'https?:\/\/(www\.)?instagram\.com\/(reel|p)\/[\w\-]+\/?', url) is not None

# Extract shortcode
def extract_shortcode(url: str) -> str:
    match = re.search(r'instagram\.com\/(?:reel|p)\/([\w\-]+)', url)
    return match.group(1) if match else None

# Download reel (with quality options if available later)
def download_reel(shortcode: str) -> str:
    try:
        post = Post.from_shortcode(L.context, shortcode)
        if not post.is_video:
            return None
        L.download_post(post, target=f"reel_{shortcode}")
        return f"reel_{shortcode}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_UTC.mp4"
    except Exception as e:
        print(f"Download error: {e}")
        return None

# /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "👋 Hello! I'm your Instagram Reel Downloader Bot.\n\n"
                          "📥 Just send me any Instagram Reel URL and choose your desired quality!")

# /help command
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "ℹ️ *How to use:*\n"
                          "1. Copy a Reel URL from Instagram.\n"
                          "2. Paste it here.\n"
                          "3. Choose quality (currently only one available).\n\n"
                          "_Example:_\n"
                          "`https://www.instagram.com/reel/CrK3JXyJQ5X/`\n\n"
                          "⚠️ Make sure the Reel is public!",
                   parse_mode='Markdown')

# Handle messages (Reel links)
@bot.message_handler(func=lambda message: True)
def handle_reel_url(message):
    url = message.text.strip()

    if not is_valid_instagram_url(url):
        bot.reply_to(message, "❌ *Invalid URL.*\nPlease send a correct Instagram Reel link.", parse_mode='Markdown')
        return

    shortcode = extract_shortcode(url)
    if not shortcode:
        bot.reply_to(message, "⚠️ Couldn't extract Reel ID. Try another link.")
        return

    # Show inline keyboard for quality selection (for future support)
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("HD Quality 🔥", callback_data=f"download_hd_{shortcode}"),
        types.InlineKeyboardButton("Cancel ❌", callback_data="cancel")
    )

    bot.send_message(message.chat.id, "🔍 Found Reel! Choose the quality to download:", reply_markup=markup)

# Callback handler for quality selection
@bot.callback_query_handler(func=lambda call: call.data.startswith("download_hd_") or call.data == "cancel")
def handle_quality_selection(call):
    if call.data == "cancel":
        bot.edit_message_text("❌ Download cancelled.", call.message.chat.id, call.message.message_id)
        return

    shortcode = call.data.replace("download_hd_", "")
    msg = bot.edit_message_text("⏳ Downloading your reel... Please wait.", call.message.chat.id, call.message.message_id)

    video_path = download_reel(shortcode)

    if video_path and os.path.exists(video_path):
        try:
            with open(video_path, 'rb') as video:
                bot.send_video(call.message.chat.id, video, caption="✅ *Here’s your reel!*", parse_mode='Markdown', supports_streaming=True)
        except Exception as e:
            bot.send_message(call.message.chat.id, "⚠️ Failed to send video.")
            print(f"Send error: {e}")
        finally:
            try:
                os.remove(video_path)
                os.rmdir(f"reel_{shortcode}")
            except Exception as e:
                print(f"Cleanup error: {e}")
    else:
        bot.edit_message_text("❌ Failed to download. The reel might be private or unavailable.", call.message.chat.id, call.message.message_id)

# Start bot
bot.infinity_polling()
