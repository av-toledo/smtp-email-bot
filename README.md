# 📧 SMTP Email Bot (Telegram Controlled)

This project is a **Telegram-controlled SMTP email bot** built with Python. It allows you to send HTML emails with inline images using custom commands over Telegram. Ideal for automating notifications, verifications, or announcements — right from your phone.

---

## 🚀 Features

- Send styled HTML emails via a Telegram bot command
- Inline image support using **CID** to improve Gmail inboxing (avoids spam folder)
- Easy-to-extend command structure: add unlimited email templates and commands
- Uses `smtplib` and `email` for full control over content and headers
- Personalize content by modifying HTML templates

---

## 🧠 How It Works

You define:
- 📄 **HTML templates** for each type of email (e.g., `email_template.html`)
- 🤖 **Telegram bot commands** (like `/email someone@example.com`)
- 🖼️ An image (`xlogo.png`) referenced using CID inside HTML:  
  ```html
  <img src="cid:xlogo" alt="Logo" width="100" />
  ```

---

## 🛠️ Setup Instructions

1. Clone this repo:
```bash
git clone https://github.com/av-toledo/smtp-email-bot.git
cd smtp-email-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file or fill in the SMTP credentials directly in `main.py`:
```env
SMTP_SERVER=smtp.yourprovider.com
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=yourPassword
SMTP_PORT=587
```

4. Add your Telegram bot token:
```python
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
```

5. Run the bot:
```bash
python main.py
```

---

## ➕ Adding More Email Commands

Want more templates? Just:
- Create a new HTML file, e.g., `reminder_template.html`
- Define a new command like:
```python
async def reminder_command(update, context):
    html = load_template("reminder_template.html")
    send_email_with_template(to_email, "Reminder", html)
```
- Register the handler with:
```python
app.add_handler(CommandHandler("reminder", reminder_command))
```

✅ You can add **as many commands and templates as you want**.

---

## 📦 Requirements

- Python 3.9+
- `python-telegram-bot`
- `smtplib` (standard)
- `email` (standard)

Install with:

```bash
pip install python-telegram-bot
```

---

## 📌 Notes

- Uses **CID (Content-ID)** images to improve inbox delivery rates, especially on Gmail.
- Tested with Namecheap's PrivateEmail SMTP but works with any provider.
- Make sure your SMTP service allows sending from your bot.

---

## 🪪 License

MIT — Free to use and modify. Attribution appreciated.
