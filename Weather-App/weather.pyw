import sys
import random
import datetime
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import requests
from PIL import ImageTk, Image

api_token = '48a90ac42caa09f90dcaeee4096b9e53'

class CustomFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        width = kwargs.get('width', 250)  
        height = kwargs.get('height', 260)  
        self.configure(width=width, height=height, padx=0)  
        
class CustomLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)
        width = kwargs.get('width', 200)  
        height = kwargs.get('height', 200)  
        bg= kwargs.get('bg', 'white')
      
        fg = kwargs.get('fg', 'black')
        
        self.configure(width=width, height=height,bg=bg, compound=tk.TOP,
                        font=('Arial', 20), )  

class WeatherApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.master.geometry('1920x1080') 
        self.pack()
        self.bg_image_label = tk.Label(self, image=background_image)
        self.bg_image_label.grid(row=0, column=0,columnspan=5)
        self.bg_image_label.grid_propagate(False)
        self.current_date_str = self.get_current_date()
        self.city_name = tk.StringVar()
        self.city_name.set('')
        self.draw_frames()
        self.draw_widgets()
        self.update_time()
        self.master.bind('<Return>', self.search_weather)

    def draw_frames(self):
        self.top_frame = CustomFrame(self.bg_image_label, width=1600, height=100, bg='SkyBlue')
        self.top_frame.grid(row=0, column=0, columnspan=4)
        self.top_frame.grid_propagate(False)
        self.search_frame = CustomFrame(self.bg_image_label, width=1600, height=90, bg='SkyBlue')
        self.search_frame.grid(row=1, column=0, columnspan=4, pady=(0, 0))
        self.search_frame.grid_propagate(False)
        self.datetime_frame = CustomFrame(self.bg_image_label, width=350, height=190, bg='SkyBlue')
        self.datetime_frame.grid(row=0, column=4, rowspan=2, padx=0,pady=(0, 0))
        self.datetime_frame.grid_propagate(False)
        
       
        self.wind_speed_frame = CustomFrame(self.bg_image_label)
        self.wind_speed_frame.grid(row=3, column=4, pady=(520, 80))
        self.wind_speed_label = CustomLabel(self.wind_speed_frame, image=wind_icon, text='\nWind Speed')
        self.wind_speed_label.grid(row=0, column=0, padx=(0, 0), sticky='S')
        
        self.weather_frame = CustomFrame(self.bg_image_label,)
        self.weather_frame.grid(row=3, column=0,pady=(520, 80))
        self.weather_label = CustomLabel(self.weather_frame, image=clear_weather_icon, text='\nWeather')
        self.weather_label.grid(row=0, column=0)
      
        self.temperature_frame = CustomFrame(self.bg_image_label,)
        self.temperature_frame.grid(row=3, column=1,pady=(520, 80))
        self.temperature_label = CustomLabel(self.temperature_frame, image=high_temp_icon, text='\nTemperature')
        self.temperature_label.grid(row=0, column=0, padx=(0, 0))
        
        self.humidity_frame = CustomFrame(self.bg_image_label,)
        self.humidity_frame.grid(row=3, column=2,pady=(520, 80))
        self.humidity_label = CustomLabel(self.humidity_frame, image=humidity_icon, text='\nHumidity' )
        self.humidity_label.grid(row=0, column=0, padx=(0, 0))
        
        self.pressure_frame = CustomFrame(self.bg_image_label,)
        self.pressure_frame.grid(row=3, column=3,pady=(520, 80))
        self.pressure_label = CustomLabel(self.pressure_frame, text='\nPressure', image=pressure_icon)
        self.pressure_label.grid(row=0, column=0, )

    def draw_widgets(self):
        
        self.app_label = tk.Label(self.top_frame, text='WEATHER REPORT', font=('Romande ADF', 30)
                          , bg='SkyBlue', fg='white')
        self.app_label.grid(row=0, column=0, ipady=20, ipadx=20)
        
        self.date_label = tk.Label(self.datetime_frame, text=self.current_date_str, font=('Arial', 25, 'bold')
                         , bg='SkyBlue', fg='white', anchor='w')
        self.date_label.grid(row=0, column=0, ipady=14, ipadx=0)
        self.time_label = tk.Label(self.datetime_frame, font=('Calibri', 24)
                         , bg='SkyBlue', fg='white', anchor='w')
        self.time_label.grid(row=1, column=0, ipady=0, ipadx=0)
        
        self.search_label = tk.Label(self.search_frame, text='Search City : '
                         ,bg='SkyBlue', fg='white', anchor='w',
                            font=('Arial', 18), width="0")
        self.search_label.grid(row=0, column=0, ipady=8, padx=(20, 2))
        self.entry = tk.Entry(self.search_frame, bg='SkyBlue', relief=tk.FLAT, font=('Arial', 12, 'bold'),
                                borderwidth=1, textvariable=self.city_name, fg='white', width="40")
        self.entry.focus_set()
        self.entry.grid(row=0, column=1, ipady=5)
        self.search_button = tk.Button(self.search_frame, image=search_icon,
                        command=self.search_weather, relief=tk.FLAT, bg='SkyBlue', width=50)
        self.search_button.grid(row=0, column=2, padx=0, ipady=3)
        self.city_name_label = tk.Label(self.search_frame, text=''
                         ,bg='SkyBlue', fg='black', anchor='c',
                            font=('Arial', 16, 'bold'), width=50)
        self.city_name_label.grid(row=0, column=3, ipady=5, )

    def update_time(self):
        current_time = datetime.datetime.now()
        self.time_label['text'] = current_time.strftime('%I:%M:%S %p')
        self.time_label.after(1000, self.update_time)

    def get_current_date(self):
        current_date = datetime.datetime.today()
        return current_date.strftime('%d %b, %Y')

    def search_weather(self, event=None):
        city_name = self.city_name.get()
        if len(city_name) > 2:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_token}'
            try:
                response = requests.get(url)
                data = response.json()

                weather_description = data['weather'][0]['description']
                weather_description = weather_description.lower()
                temperature = round(data['main']['temp'] - 273.15, 2)
                if len(weather_description.split()) == 1:
                    weather_description = '\n' + weather_description
                else:
                    weather_description = '\n'.join(weather_description.split())
                self.weather_label['text'] = f"{weather_description}"
                self.temperature_label['text'] = f"\n{temperature} C"
                self.wind_speed_label['text'] = f"\n{data['wind']['speed']} m/s"
                self.humidity_label['text'] = f"\n{data['main']['humidity']} %"
                self.pressure_label['text'] = f"\n{data['main']['pressure']} hPa"

                self.city_name_label['text'] = f'Weather in {city_name.capitalize()}'
                if temperature <= 18:
                    self.temperature_label['image'] = low_temp_icon
                else:
                    self.temperature_label['image'] = high_temp_icon

                if 'thunder' in weather_description:
                    self.weather_label['image'] = thunderstorm_icon
                elif 'cloud' in weather_description:
                    self.weather_label['image'] = cloudy_icon
                elif 'now' in weather_description:
                    self.weather_label['image'] = snow_icon
                elif 'drizzle' in weather_description or 'rain' in weather_description:
                    self.weather_label['image'] = drizzle_icon
                elif ('mist' in weather_description or 'haze' in weather_description or 'fog' in weather_description
                        or 'oke' in weather_description):
                    self.weather_label['image'] = mist_icon
                elif 'hail' in weather_description:
                    self.weather_label['image'] = hail_icon
                else:
                    self.weather_label['image'] = clear_weather_icon


            except KeyError:
                messagebox.showerror('Weather app', 'No such city in the database')
            except:
                messagebox.showerror('Weather app', 'No internet connection')
                
            self.entry.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Weather app')

    if not api_token:
        root.withdraw()
        messagebox.showerror('Weather app', 'OpenWeatherMap API Token is required\n touse this app')
        sys.exit(0)

    bg_list = [f'wallpapers/b{i}.jpg' for i in range(1, 7)]
    bg = Image.open(random.choice(bg_list))
    try:
      bg = bg.resize((1920, 1080), Image.ANTIALIAS)
    except AttributeError:
     try:
        bg = bg.resize((1920, 1080), Image.ANTIALIAS)
     except:
        bg = bg.resize((1920, 1080))


    background_image = ImageTk.PhotoImage(bg)

    search_icon = PhotoImage(file='icons/searchlogo.png')

    clear_weather_icon = PhotoImage(file='icons/clearclouds.png')
    clouds = Image.open('icons/cloudssun.png')
    cloudy_icon = ImageTk.PhotoImage(clouds)
    high_temp_icon = PhotoImage(file='icons/higher_temp.png')
    low_temp_icon = PhotoImage(file='icons/lower_temp.png')
    humidity_icon = PhotoImage(file='icons/humidityy.png')
    pressure_icon = PhotoImage(file='icons/wpressure.png')
    wind_icon = PhotoImage(file='icons/windd.png')
    thunderstorm_icon = PhotoImage(file='icons/thunderstorms.png')
    snow_icon = PhotoImage(file='icons/isnow.png')
    drizzle_icon = PhotoImage(file='icons/drizzle.png')
    mist_icon = PhotoImage(file='icons/mist1.png')
    hail_icon = PhotoImage(file='icons/cloudhail.png')

    app = WeatherApp(master=root)
    app.mainloop()