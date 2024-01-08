import os
import qrcode
from PIL import Image
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "6849177198:AAGN5qOU58V4rkHPwey3sDuvdk_IwJgbIt4"

def generate_qr_code(update: Update, context: CallbackContext):
    if update.message.reply_to_message is not None:
        link = update.message.reply_to_message.text
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = "qr_code.png"
        img.save(img_path)

        # Opening the image and pasting the logo on it
        logo_path = "etsy_logo.png"
        base_img = Image.open(img_path).convert("RGBA")
        logo_img = Image.open(logo_path).convert("RGBA")
        w, h = base_img.size
        position = ((w / 2) - (logo_img.size[0] / 2), (h / 2) - (logo_img.size[1] / 2))
        base_img.paste(logo_img, position, logo_img)
        base_img.save(img_path)

        # Sending the image
        with open(img_path, "rb") as img:
            update.message.reply_photo(img)

        # Deleting the image file
        os.remove(img_path)
    else:
        update.message.reply_text("Пожалуйста, отправьте ссылку, для которой хотите создать QR код.")

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_qr_code))

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()