import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button


class HomePageRoot(BoxLayout):
    pass


class PatientInfoRoot(BoxLayout):
    def add_patient(self):
        app = App.get_running_app()
        name = self.ids.patient_name.text.strip()
        surgery = self.ids.surgery_type.text
        anesthesia = self.ids.anesthesia_type.text

        if not name:
            return

        app.add_patient(name, surgery, anesthesia)

        self.ids.patient_name.text = ""
        self.ids.surgery_type.text = "select surgery type"
        self.ids.anesthesia_type.text = "select anesthesia type"


class PatientListRoot(BoxLayout):
    def refresh(self):
        app = App.get_running_app()
        container = self.ids.patient_list_container
        container.clear_widgets()

        search = self.ids.search_box.text.strip().lower()
        patients = app.flatten_patients(search)

        for patient in patients:
            row = BoxLayout(size_hint_y=None, height=70, spacing=10, padding=(10, 0))
            row.add_widget(Label(text=f"Room {patient['room']}", font_size=22, size_hint_x=0.2))
            row.add_widget(Label(text=patient['name'], font_size=24, size_hint_x=0.3))
            row.add_widget(Label(text=patient['surgery'], font_size=20, size_hint_x=0.25))
            row.add_widget(Label(text=patient['anesthesia'], font_size=20, size_hint_x=0.25))
            container.add_widget(row)

    def confirm_clear_list(self):
        popup = Popup(
            title="Clear all patients?",
            size_hint=(0.75, 0.4),
            auto_dismiss=False,
        )

        def do_clear(*_):
            App.get_running_app().clear_all_patients()
            popup.dismiss()

        content = BoxLayout(orientation="vertical", spacing=20, padding=20)
        content.add_widget(Label(text="Are you sure you want to delete ALL patients?", font_size=20))

        btns = BoxLayout(spacing=15, size_hint_y=None, height=60)
        btns.add_widget(Button(text="Cancel", on_press=popup.dismiss))
        btns.add_widget(Button(text="Clear", background_color=(0.8, 0.1, 0.1, 1), on_press=do_clear))

        content.add_widget(btns)
        popup.content = content
        popup.open()


class MyApp(App):
    selected_room = NumericProperty(0)
    patients_by_room = DictProperty({})
    data_filename = "patients.json"

    def build(self):
        return Builder.load_file("main.kv")

    def on_start(self):
        self.load_patients()

    def get_data_path(self):
        return os.path.join(self.user_data_dir, self.data_filename)

    def load_patients(self):
        path = self.get_data_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.patients_by_room = json.load(f)

    def save_patients(self):
        path = self.get_data_path()
        os.makedirs(self.user_data_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.patients_by_room, f, ensure_ascii=False, indent=2)

    def select_room(self, room_number):
        self.selected_room = room_number
        self.root.current = "patient_info"

    def add_patient(self, name, surgery, anesthesia):
        room_key = str(self.selected_room)
        room_patients = list(self.patients_by_room.get(room_key, []))
        room_patients.append({"name": name, "surgery": surgery, "anesthesia": anesthesia})
        self.patients_by_room[room_key] = room_patients

        self.save_patients()
        self.update_patient_list_screen()

    def clear_all_patients(self):
        self.patients_by_room = {}
        self.save_patients()
        self.update_patient_list_screen()

    def update_patient_list_screen(self):
        patient_list_screen = self.root.get_screen("patient_list")
        if "patient_list_root" in patient_list_screen.ids:
            patient_list_screen.ids.patient_list_root.refresh()

    def flatten_patients(self, search_text=""):
        search = search_text.lower()
        flat = []
        for room, patients in sorted(self.patients_by_room.items(), key=lambda item: int(item[0])):
            for patient in patients:
                if search and search not in patient["name"].lower():
                    continue
                flat.append(
                    {
                        "room": room,
                        "name": patient["name"],
                        "surgery": patient["surgery"],
                        "anesthesia": patient["anesthesia"],
                    }
                )
        return flat


MyApp().run()

