from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import requests
import json

class JarvisApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.lbl = Label(text="Jarvis System Online\nBoliye Bhai!", font_size=18, halign="center")
        
        self.btn = Button(
            text="Tap to Ask Jarvis", 
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 1, 1)
        )
        self.btn.bind(on_press=self.start_thinking)
        
        self.layout.add_widget(self.lbl)
        self.layout.add_widget(self.btn)
        return self.layout

    def start_thinking(self, instance):
        self.lbl.text = "Jarvis is Thinking..."
        # Example query - Later we can add actual Mic input
        query = "Duniya ka sabse uncha pahad kaun sa hai?" 
        Clock.schedule_once(lambda dt: self.ask_groq(query), 0.1)

    def ask_groq(self, query):
        url = "https://api.groq.com/openai/v1/chat/completions"
        api_key = "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"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are Jarvis. Reply in 1 short Hinglish line."},
                {"role": "user", "content": query}
            ]
        }

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                ans = r.json()['choices'][0]['message']['content']
                self.lbl.text = f"Jarvis: {ans}"
            else:
                self.lbl.text = f"Error: {r.status_code}"
        except:
            self.lbl.text = "Connection Failed!"

if __name__ == "__main__":
    JarvisApp().run()
