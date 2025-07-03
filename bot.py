import os
import mimetypes
import smtplib
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image     import MIMEImage
from email.utils          import formataddr
from telegram             import Update
from telegram.ext         import ApplicationBuilder, CommandHandler, ContextTypes

# --- SMTP Config ---
SMTP_SERVER   = "" #server ur using, in this case i used privateemail by namecheap
SMTP_PORT     = 587
SMTP_USERNAME = "" #user for ur smtp
SMTP_PASSWORD = ""          # ← password for smtp

CC          = ""
REPLY_USER  = ""

# --- Template Loader ---
def load_template(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# email sender with cid so it inboxes without going to spam
def send_email_with_template(
        to_email: str,
        subject: str,
        html_content: str,
        image_path: str = "xlogo.png",
        image_cid: str = "xlogo",
        cc: str | None = None,
        reply_to: str | None = None):
    """
    Send an HTML email with an inline image.
    cc       – optional CC address
    reply_to – optional Reply-To address
    """

    root = MIMEMultipart("related")
    root["From"] = formataddr(("X", SMTP_USERNAME))
    if reply_to:  # add header only if provided
        root["Reply-To"] = reply_to
    root["To"] = to_email
    if cc:
        root["CC"] = cc
    root["Subject"] = subject

    # html supp
    alt = MIMEMultipart("alternative")
    root.attach(alt)
    alt.attach(MIMEText("This message requires HTML support.", "plain"))
    alt.attach(MIMEText(html_content, "html"))

    # inline image
    if os.path.exists(image_path):
        ctype = mimetypes.guess_type(image_path)[0] or "image/png"
        maintype, subtype = ctype.split("/", 1)
        with open(image_path, "rb") as fp:
            img = MIMEImage(fp.read(), _subtype=subtype)
            img.add_header("Content-ID", f"<{image_cid}>")
            img.add_header("Content-Disposition",
                           "inline",
                           filename=os.path.basename(image_path))
            root.attach(img)

    # recepients
    recipients = [to_email]
    if cc:
        recipients.append(cc)

    # send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipients, root.as_string())

# --- /email Command ---
async def email_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /email someone@example.com")
        return

    to_email = context.args[0]
    try:
        html = load_template("email_template.html")
        send_email_with_template(to_email, "Placeholder email ", html) #title
        await update.message.reply_text(f"✅ Sent  email to {to_email}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# --- Telegram Bot Setup ---
if __name__ == "__main__":
    app = ApplicationBuilder().token("").build() #add ur tele bot token here
    app.add_handler(CommandHandler("email", email_command)) #u can add more commands, u just need to make more templates
    print("🤖 Bot is running...")
    app.run_polling()
