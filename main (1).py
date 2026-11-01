import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock

try:
    from plyer import tts
except Exception:
    tts = None

class RoundButton(Button):
    def __init__(self, **kwargs):
        super(RoundButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        with self.canvas.before:
            Color(0.8, 0.2, 0.5, 1) # Attractive Pink/Purple Circle
            self.ellipse = Ellipse(size=self.size, pos=self.pos)
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, instance, value):
        dim = min(instance.width, instance.height)
        self.ellipse.size = (dim, dim)
        self.ellipse.pos = (instance.center_x - dim/2, instance.center_y - dim/2)

class DictionaryApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)

        # Top layout for Circle Button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.10), spacing=10)
        top_bar.add_widget(Label(size_hint_x=0.35))

        self.circle_btn = RoundButton(
            text="🤖",
            font_size=26,
            bold=True,
            size_hint=(None, None),
            size=(65, 65)
        )
        self.circle_btn.bind(on_press=self.intro_speak)
        top_bar.add_widget(self.circle_btn)
        top_bar.add_widget(Label(size_hint_x=0.35))
        layout.add_widget(top_bar)

        # Title (AI GRAMMAR ROBOT)
        self.title_label = Label(
            text="AI GRAMMAR ROBOT",
            font_size=26,
            bold=True,
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.title_label)

        # School Name Label
        self.school_label = Label(
            text="POPE MEMORIAL HR.SEC.SCL",
            font_size=28,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.09)
        )
        layout.add_widget(self.school_label)

        # Developer Name Label
        self.dev_label = Label(
            text="DEVELOPER BY S∆NTHOSH",
            font_size=24,
            bold=True,
            color=(1, 0, 0, 1), # Pure Red Color
            size_hint=(1, 0.07)
        )
        layout.add_widget(self.dev_label)

        # Search Box (Big Font)
        self.input_box = TextInput(
            hint_text="Type word here...",
            multiline=False,
            font_size=30,
            size_hint=(1, 0.11)
        )
        layout.add_widget(self.input_box)

        # Search Button
        self.search_btn = Button(
            text="SEARCH WORD",
            font_size=24,
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),
            size_hint=(1, 0.11)
        )
        self.search_btn.bind(on_press=self.find_meaning)
        layout.add_widget(self.search_btn)

        # Answer Box Layout (Background Color Changing Box)
        self.ans_layout = BoxLayout(size_hint=(1, 0.28))

        with self.ans_layout.canvas.before:
            self.ans_bg = Color(0.2, 0.2, 0.2, 1) # Default Dark Gray
            self.ans_rect = Rectangle(size=self.ans_layout.size, pos=self.ans_layout.pos)

        self.ans_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Answer Label
        self.result_label = Label(
            text="Type word & click Search...
Meaning will appear here",
            font_size=26,
            bold=True,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.ans_layout.add_widget(self.result_label)

        layout.add_widget(self.ans_layout)

        # Speak Answer Button (One-time speak on click for current searched word)
        self.speak_btn = Button(
            text="🔊 SPEAK ANSWER (ROBOT VOICE)",
            font_size=22,
            bold=True,
            background_color=(0.1, 0.5, 0.8, 1),
            size_hint=(1, 0.12)
        )
        self.speak_btn.bind(on_press=self.speak_answer)
        layout.add_widget(self.speak_btn)

        # Default speech text
        self.current_speech_text = "Welcome to AI Grammar Robot. Please search a word."

        # Pre-load TTS engine in background to remove first-touch lag
        Clock.schedule_once(self._warmup_tts, 0.1)

        return layout

    def _warmup_tts(self, dt):
        if tts:
            try:
                # Background silent touch to initialize audio engine fast
                pass
            except Exception:
                pass

    def _update_rect(self, instance, value):
        self.ans_rect.pos = instance.pos
        self.ans_rect.size = instance.size

    def intro_speak(self, instance):
        intro_text = "Hi dear students, I am AI grammar robot, English Department, Pope Memorial Higher Secondary School"
        self.result_label.text = intro_text.replace(', ', '.
')
        if tts:
            try:
                tts.speak(intro_text)
            except Exception as e:
                print("TTS Error:", e)

    def speak_answer(self, instance):
        if tts:
            try:
                tts.speak(self.current_speech_text)
            except Exception as e:
                print("TTS Error:", e)

    def find_meaning(self, instance):
        word = self.input_box.text.strip().lower()
        self.input_box.text = ""

        if not word:
            return

        # Complete Database (Nouns, Adjectives, Verbs, Adverbs)
        english_dict = {
            # Nouns & Adjectives
            "science": "Meaning: Study of physical & natural world.
Grammar: Noun
Example: Science helps us.",
            "robot": "Meaning: A machine for complex actions.
Grammar: Noun
Example: Robot works fast.",
            "computer": "Meaning: Electronic device for data.
Grammar: Noun
Example: I use computer.",
            "school": "Meaning: Institution for education.
Grammar: Noun
Example: We go to school.",
            "happy": "Meaning: Feeling pleasure or joy.
Grammar: Adjective
Example: I am very happy.",
            "fast": "Meaning: Moving at high speed.
Grammar: Adjective
Example: Train runs fast.",
            "energy": "Meaning: Strength required for activity.
Grammar: Noun
Example: Solar energy is clean.",
            "universe": "Meaning: All existing space & matter.
Grammar: Noun
Example: Universe is vast.",
            "planet": "Meaning: Celestial body orbiting a star.
Grammar: Noun
Example: Earth is a planet.",
            "oxygen": "Meaning: Gas essential for life.
Grammar: Noun
Example: Plants give oxygen.",
            "gravity": "Meaning: Force attracting objects.
Grammar: Noun
Example: Gravity pulls down.",
            "experiment": "Meaning: Scientific test or procedure.
Grammar: Noun
Example: We did an experiment.",
            "technology": "Meaning: Application of science.
Grammar: Noun
Example: Tech changes lives.",
            "student": "Meaning: A person who studies.
Grammar: Noun
Example: He is a good student.",
            "teacher": "Meaning: Person who helps to learn.
Grammar: Noun
Example: Teacher guides us.",
            "water": "Meaning: Clear liquid for all life.
Grammar: Noun
Example: Drink clean water.",
            "nature": "Meaning: Physical world and wildlife.
Grammar: Noun
Example: Protect nature.",
            "smart": "Meaning: Having quick intelligence.
Grammar: Adjective
Example: She is smart.",
            "brightness": "Meaning: Quality of shining bright.
Grammar: Noun
Example: Sun brightness is high.",
            "future": "Meaning: Time following present.
Grammar: Noun
Example: AI is our future.",
            "success": "Meaning: Accomplishment of a goal.
Grammar: Noun
Example: Hard work brings success.",
            "knowledge": "Meaning: Information from learning.
Grammar: Noun
Example: Books give knowledge.",
            "wisdom": "Meaning: Quality of good judgment.
Grammar: Noun
Example: Wisdom comes with age.",
            "courage": "Meaning: Ability to face fear.
Grammar: Noun
Example: Show great courage.",
            "honest": "Meaning: Free of deceit, truthful.
Grammar: Adjective
Example: Always be honest.",
            "brilliant": "Meaning: Exceptionally clever.
Grammar: Adjective
Example: Brilliant idea.",
            "creative": "Meaning: Using imagination.
Grammar: Adjective
Example: Creative designer.",
            "active": "Meaning: Engaging in action.
Grammar: Adjective
Example: Stay active.",
            "patient": "Meaning: Able to tolerate delay.
Grammar: Adjective
Example: Be patient.",
            "strong": "Meaning: Having physical power.
Grammar: Adjective
Example: Exercise makes us strong.",
            "peace": "Meaning: Freedom from disturbance.
Grammar: Noun
Example: We want peace.",
            "friend": "Meaning: Person with mutual affection.
Grammar: Noun
Example: He is my friend.",
            "journey": "Meaning: Act of traveling.
Grammar: Noun
Example: Life is a journey.",
            "history": "Meaning: Study of past events.
Grammar: Noun
Example: Study history.",
            "language": "Meaning: Method of communication.
Grammar: Noun
Example: English is a language.",
            "music": "Meaning: Vocal or instrumental sounds.
Grammar: Noun
Example: I love music.",

            # Verbs (15 words)
            "run": "Meaning: Move at a fast speed.
Grammar: Verb
Example: I run in the morning.",
            "read": "Meaning: Look at and comprehend text.
Grammar: Verb
Example: She reads a book.",
            "write": "Meaning: Mark letters on a surface.
Grammar: Verb
Example: Students write notes.",
            "learn": "Meaning: Gain knowledge or skill.
Grammar: Verb
Example: We learn python.",
            "speak": "Meaning: Say something in words.
Grammar: Verb
Example: Speak clearly.",
            "listen": "Meaning: Give attention to sound.
Grammar: Verb
Example: Listen to music.",
            "think": "Meaning: Have a particular belief.
Grammar: Verb
Example: Think before acting.",
            "create": "Meaning: Bring something into existence.
Grammar: Verb
Example: He creates apps.",
            "build": "Meaning: Construct something by putting parts together.
Grammar: Verb
Example: They build robots.",
            "solve": "Meaning: Find an answer to a problem.
Grammar: Verb
Example: Solve this sum.",
            "play": "Meaning: Engage in activity for enjoyment.
Grammar: Verb
Example: Boys play cricket.",
            "walk": "Meaning: Move at a regular pace.
Grammar: Verb
Example: We walk daily.",
            "eat": "Meaning: Put food in the mouth and swallow.
Grammar: Verb
Example: Eat healthy food.",
            "sleep": "Meaning: Rest with eyes closed.
Grammar: Verb
Example: Sleep early at night.",
            "help": "Meaning: Make it easier for someone.
Grammar: Verb
Example: Help your friends.",

            # Adverbs (15 words)
            "quickly": "Meaning: At a fast speed.
Grammar: Adverb
Example: He finished quickly.",
            "slowly": "Meaning: At a slow speed.
Grammar: Adverb
Example: Walk slowly.",
            "quietly": "Meaning: Making little or no noise.
Grammar: Adverb
Example: Sit quietly.",
            "loudly": "Meaning: Producing much noise.
Grammar: Adverb
Example: Do not talk loudly.",
            "carefully": "Meaning: With great attention.
Grammar: Adverb
Example: Handle carefully.",
            "easily": "Meaning: Without difficulty.
Grammar: Adverb
Example: She passed easily.",
            "happily": "Meaning: In a happy manner.
Grammar: Adverb
Example: They live happily.",
            "brilliantly": "Meaning: In an impressive manner.
Grammar: Adverb
Example: He performed brilliantly.",
            "badly": "Meaning: In a severe way.
Grammar: Adverb
Example: Do not treat anyone badly.",
            "well": "Meaning: In a good way.
Grammar: Adverb
Example: You did well.",
            "often": "Meaning: Frequently, many times.
Grammar: Adverb
Example: I often read books.",
            "always": "Meaning: At all times, forever.
Grammar: Adverb
Example: Always speak truth.",
            "never": "Meaning: At no time in past or future.
Grammar: Adverb
Example: Never give up.",
            "today": "Meaning: On this present day.
Grammar: Adverb
Example: Today is a good day.",
            "tomorrow": "Meaning: On the day after today.
Grammar: Adverb
Example: See you tomorrow."
        }

        box_colors = [
            (0.1, 0.4, 0.6, 1),
            (0.5, 0.1, 0.5, 1),
            (0.1, 0.5, 0.3, 1),
            (0.6, 0.3, 0.1, 1),
            (0.5, 0.1, 0.1, 1),
            (0.2, 0.4, 0.4, 1)
        ]

        self.ans_bg.rgba = random.choice(box_colors)

        if word in english_dict:
            result_text = english_dict[word]
            self.result_label.text = result_text.replace('. ', '.
')
            self.current_speech_text = f"The meaning of {word} is {result_text}"
        else:
            not_found = f"Word '{word}' not found!
Try: run, quickly, science, happy..."
            self.result_label.text = not_found
            self.current_speech_text = "Word not found."

if __name__ == '__main__':
    DictionaryApp().run()