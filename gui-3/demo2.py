import time
from kivy.app import App # สำหรับเริมต้น kivy app
from kivy.uix.screenmanager import ScreenManager, Screen # จัดการระบบเปลี่ยนหน้าและจำนวนหน้า
from kivy.core.text import LabelBase # ใส่ฟอนต์ต่างๆ
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'resizable', '0')
import threading
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
import random


LabelBase.register(name= "Thai",
                   fn_regular='THSarabunNew.ttf',
                   fn_bold='THSarabunNew Bold.ttf',)

class FarmScreenManager(ScreenManager): # logic ตัวจัดการระบบเปลี่ยนหน้า
    pass

class InformationPopup(Popup):
    page2_info = ObjectProperty(None)

class Page2(Screen): # logic หน้า Page2
    light_status = StringProperty("ปิด")
    light_color = ListProperty([250/255, 226/255, 90/255, 0.3])
    water_level = NumericProperty(0)
    time_label = StringProperty("00:00:00")
    temp_label = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.time_label = time.strftime("%H:%M:%S")
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.simulate_temp, 0.01)
        Clock.schedule_once(self.show_dashboard, 0)
        Clock.schedule_interval(self.update_dashboard, 0.01)
        #threading.Thread(target=self.simulate_temp, daemon=True).start()

    def on_enter(self, *args):
        
        pass

    def simulate_temp(self, dt):
        self.temp_label = random.randint(0, 100)

    def update_time(self, dt):
        self.time_label = time.strftime("%H:%M:%S")

    def open_info(self):
        self.info_popup = InformationPopup(page2_info = self)
        self.info_popup.open()

    def update_text_label(self):
        input_text = self.ids.text_input_id.text
        self.ids.show_label_id.text = input_text
        #self.ids.show_label_id.text = "อัพเดทข้อมูลเรียบร้อยแล้ว"

    def clear_info(self):
        self.ids.show_label_id.text = ""
        self.ids.text_input_id.text = ""

    def toggle_light(self, switch_instance):
        if switch_instance.active:
            self.light_status = "เปิด"
            self.light_color = [1, 223/255, 0, 1]  # สีเหลืองสดใสเมื่อเปิด
        else:
            self.light_status = "ปิด"
            self.light_color = [250/255, 226/255, 90/255, 1]  # สีเหลืองอ่อนเมื่อปิด

    

    def show_dashboard(self, dt):
        self.fig, self.ax = plt.subplots(constrained_layout=True)
        self.data_points = 24
        self.xdata = np.array(range(self.data_points))
        self.ydata = np.array([17, 20, 21, 18 ,24 ,27 ,31 ,25 ,21 ,23 ,17, 20, 21, 18 ,24 ,27 ,31 ,25 ,21 ,23, 21, 22, 16, 26])

        self.ax.set_xlabel("Time", color='white')
        self.ax.set_ylabel("Temperature (°C)", color='white')
        #self.xnew = np.linspace(self.xdata.min(), self.xdata.max(), 300)
        #self.ysmooth = make_interp_spline(self.xdata, self.ydata)(self.xnew)

        self.ax.plot(self.xdata, self.ydata, color='green', linewidth=2, alpha=0.9, antialiased=True)
        self.ax.fill_between(self.xdata, self.ydata, color='green', alpha=0.3)

        self.ax.tick_params(axis='both', which='major', labelsize=8, colors='white')
        
        self.fig.patch.set_facecolor("none")
        self.ax.set_facecolor("#E9E9E9")

        for spine in self.ax.spines.values():
            spine.set_visible(False)
       
        self.ax.grid(True, linestyle='--', alpha=0.5, color='gray')

        self.plot_canvas = FigureCanvasKivyAgg(self.fig)
        self.ids.temp_dashboard.add_widget(self.plot_canvas)

    def update_dashboard(self, dt):
        self.temp_label = random.randint(0, 40)
        self.ydata = np.append(self.ydata[1:], self.temp_label)
        #print(self.ydata)
        # อัพเดทเฉพาะข้อมูลเส้นกราฟ โดยไม่ต้องล้างทั้งหมด
        self.ax.lines[0].set_ydata(self.ydata)
        
        # อัพเดท fill_between
        if len(self.ax.collections) > 0:
            self.ax.collections[0].remove()
        self.ax.fill_between(self.xdata, self.ydata, color='green', alpha=0.3)
        
        self.plot_canvas.draw_idle()

class Page1(Screen):
    def on_enter(self, *args):
        pass

class HomeScreen(Screen): # logic หน้า HomeScreen
    def on_enter(self, *args):
        pass
    
class Farm2App(App):
    def build(self):
        self.title = "ระบบจัดการฟาร์มอัจฉริยะ"
        return FarmScreenManager()
    
    
if __name__ == "__main__":
    Farm2App().run()








