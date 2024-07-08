import tkinter as tk
# import ttkbootstrap as ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import os
from matplotlib import rc
from matplotlib import rcParams
from pdf2image import convert_from_path
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
# import fitz

COLORS = {'dark_gray': '#242424','light_gray': '#2b2b2b', 'entry_gray': '#343638'}
initial_setup_complete = False
CD = os.getcwd()
DPI = 0

def get_ctk_image(text, png_path, size):
    bg_color = {'light': '#CFCFCF', 'dark': '#333333'}
    txt_color = {'light': 'black', 'dark': 'white'}
    light_path = png_path + '_light.png'
    dark_path = png_path + '_dark.png'
    light_image = latex_image(text, light_path, txt_color['light'], bg_color['light'], size = size)
    dark_image = latex_image(text, dark_path, txt_color['dark'], bg_color['dark'], size = size)
    ctk_image = ctk.CTkImage(
        light_image = light_image,
        dark_image = dark_image
    )
    return ctk_image

def latex_image(text, png_path, txt_color, bg_color, size):
    rcParams['text.usetex'] = True
    rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
    fig = plt.figure(facecolor = bg_color)
    plt.axis('off')
    plt.text(x = 0.5, y = 0.5, s = f'{text}', size = size, ha = 'center', color = txt_color)
    plt.savefig(
        png_path,
        format = 'png', 
        bbox_inches = 'tight')
    image = Image.open(png_path)
    return image

class App(ctk.CTk):
    def __init__(self, title, window_dim):
        super().__init__()
        self.title(title)
        self.bind('<Escape>', lambda event: self.quit())

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        midpoint = (int(screen_width/2),int(screen_height/2))
        offsetx = midpoint[0]-int(window_dim[0]/2)
        offsety = midpoint[1]-int(window_dim[1]/2)
        self.geometry(f'{window_dim[0]}x{window_dim[1]}+{offsetx}+{offsety}')
        global DPI
        DPI = screen_width / (window_dim[0] / 2.54)
        print(DPI)
        #self.geometry(f'1920x1080+{offsetx}+{offsety}')

        self.rowconfigure(0, weight = 1, uniform = 'a')  
        self.rowconfigure(1, weight = 7, uniform = 'a')  
        #self.rowconfigure(2, weight = 2, uniform = 'a')
        self.columnconfigure(list(range(2)), weight = 1, uniform = 'a')

        self.display_frame = tk.Frame(master = self)
        self.display_frame.grid(column = 1, row = 0, rowspan = 3, columnspan = 2)
        self.fig, self.axes = plt.subplots(layout='constrained')
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.display_frame)
        self.canvas.get_tk_widget().pack()
        self.axes.set_ylim(-4,4)
        self.axes.set_xlim(-1,14)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.display_frame, pack_toolbar = False)
        self.toolbar.update()
        self.toolbar.pack()

        self.control_panel = ControlPanel(self)

        self.is_dark = tk.StringVar()
        self.is_dark.set('light')
        ctk.set_appearance_mode(self.is_dark.get())
        self.dark_mode_toggle = ctk.CTkSwitch(self, 
            text = 'Enable dark mode', 
            command = self.dark_toggle, 
            variable = self.is_dark,
            onvalue = 'dark',
            offvalue = 'light')
        self.dark_mode_toggle.grid(row = 0, column = 0, sticky = 'nw')

        global initial_setup_complete
        initial_setup_complete = True
        self.update()
        self.mainloop()

    def update(self, value = None):
        if initial_setup_complete != True: return None
        
        new_data = self.control_panel.get_data()
        e = new_data[0]
        k_1 = new_data[1]
        k_2 = new_data[2]
        a = new_data[3]
        y_1i = new_data[4]
        y_2i = new_data[5]

        temp_x = self.axes.get_xlim()
        temp_y = self.axes.get_ylim()
        self.axes.clear()
        self.axes.set_xlim(temp_x[0],temp_x[1])
        self.axes.set_ylim(temp_y[0],temp_y[1])
        self.axes.grid(True)

        c_1 = k_1/(1+e+k_1)
        v_1 = (1-c_1)/(1+e)
        s_1 = e*v_1
        c_2 = k_2/(1+e+k_2)
        v_2 = (1-c_2)/(1+e)
        s_2 = e*v_2
        b = 1-a
        golden_pi = 1/((0.5)*(c_1+v_2+((c_1-v_2)**2+4*v_1*c_2)**0.5))-1
        # still need the js

        M_11 = c_1
        M_12 = c_2
        M_21 = (b*s_1*c_1+v_1)/(1-b*s_2)
        M_22 = (b*s_1*c_2+v_2)/(1-b*s_2)
        # Still need the N's

        # I have to compute all of the eigenschtuff myself because the fucking numpy eigen function auto-orders the vectors, infuriating
        mu_1 = 0.5*(M_11+M_22 + np.sqrt((M_11-M_22) ** 2 + 4*M_12*M_21))
        mu_2 = 0.5*(M_11+M_22 - np.sqrt((M_11-M_22) ** 2 + 4*M_12*M_21))
        m_11 = 1
        m_12 = (mu_1-M_11)/M_12*m_11
        m_21 = 1
        m_22 = -(M_11-mu_2)/M_12*m_21
        P = np.array([[m_11,m_21],[m_12,m_22]])
        P_inverse = np.linalg.inv(P)
        y_vec = np.array([[y_1i],[y_2i]])
        eta_vec = np.matmul(P_inverse,y_vec)

        r_l = (m_22*y_1i - m_21*y_2i)/(m_11*m_22-m_12*m_21)

        t_range = np.linspace(-3,14,1000)
        exp_1 = (1/mu_1) ** t_range
        if k_2 > k_1:
            exp_2 = (-1/mu_2) ** t_range
            exp_2 = exp_2 * np.cos(np.pi*t_range)
        else:
            exp_2 = 1/mu_2 ** t_range
        z_l1 = r_l * m_11 * exp_1
        z_l2 = r_l * m_12 * exp_1

        y_1 = (exp_1 * eta_vec[0] * m_11) + (exp_2 * eta_vec[1] * m_21)
        y_2 = (exp_1 * eta_vec[0] * m_12) + (exp_2 * eta_vec[1] * m_22)
        self.axes.plot(t_range, y_1, color = 'blue')
        self.axes.plot(t_range, y_2, color = 'red')
        self.axes.plot(t_range, z_l1, color = 'blue', linestyle = 'dashed')
        self.axes.plot(t_range, z_l2, color = 'red', linestyle = 'dashed')
        self.canvas.draw()

    def dark_toggle(self):
        mpl_trans = {'light':'default', 'dark':'dark_background'}
        ctk.set_appearance_mode(self.is_dark.get())
        plt.style.use(mpl_trans[self.is_dark.get()])
        self.axes.clear()
        self.canvas.draw()

class ControlPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets = []
        self.parent = parent

        self.exploitation_widget = EntryBlock(self, '$e=$', 'exploitation', (0,5), 1.22)
        self.exploitation_widget.pack(fill = 'both')
        self.widgets.append(self.exploitation_widget)
        self.comp_one_widget = EntryBlock(self, '$k_1=$', 'comp_1', (0,5), 1.5)
        self.comp_one_widget.pack(fill = 'both')
        self.widgets.append(self.comp_one_widget)
        self.comp_two_widget = EntryBlock(self, '$k_2=$', 'comp_2', (0,5), 3.6)
        self.comp_two_widget.pack(fill = 'both')
        self.widgets.append(self.comp_two_widget)
        self.reinvestment_widget = EntryBlock(self, '$a=$', 'reinvestment_rate', (0,5), 0.5)
        self.reinvestment_widget.pack(fill = 'both')
        self.widgets.append(self.reinvestment_widget)
        self.init_output_one_widget = EntryBlock(self, '$y_1=$', 'output_1', (0,5), 1)
        self.init_output_one_widget.pack(fill = 'both')
        self.widgets.append(self.init_output_one_widget)
        self.init_output_two_widget = EntryBlock(self, '$y_2=$', 'output_2', (0,5), 0.67)
        self.init_output_two_widget.pack(fill = 'both')
        self.widgets.append(self.init_output_two_widget)
        
        self.grid(row = 1, column = 0, sticky = 'new', padx = 10)

    def update(self, *args):
        try:
            self.parent.update()
        except ValueError:
            pass

    def get_data(self):
        data = []
        for widget in self.widgets:
            data.append(widget.get())
        return data

class EntryBlock(ctk.CTkFrame):
    def __init__(self, parent, var_label, png_path, range, initial):
        super().__init__(parent)
        self.entry_text = tk.StringVar()
        self.entry_text.set(initial)
        self.entry_var = tk.DoubleVar()
        self.entry_var.set(float(initial))
        self.parent = parent
        self.entry_text.trace_add('write', self.parent.update)

        # Attribute to keep track of if the info-window is open
        self.info_window = None

        label_image_ctk = get_ctk_image(var_label, png_path, size = 200)

        vcmd = (self.register(self.update_slider), '%P')
        self.slider = ctk.CTkSlider(self, from_ = range[0], to = range[1],
         number_of_steps = 1000, command = self.update_num, variable = self.entry_var)
        self.slider.set(initial)  

        self.var_label = ctk.CTkLabel(self, text = '', fg_color = ('#CFCFCF', '#333333'), image = label_image_ctk)
        self.var_entry = ctk.CTkEntry(self, textvariable= self.entry_text, validate = 'key', validatecommand = vcmd)
        self.q_button = ctk.CTkButton(self, text = "?", width = 10, height = 2, font = ('Arial', 10))
        # self.q_button.bind("<Enter>", self.on_enter)
        self.q_button.bind("<Leave>", self.on_leave)

        self.columnconfigure((0,1,3), weight= 1, uniform = 'b')
        self.columnconfigure(2, weight = 3, uniform = 'b')
        self.rowconfigure((0,1), weight= 1, uniform = 'b')

        self.q_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nw')
        self.var_label.grid(row= 0, column= 1, sticky = 'e', padx = 5)
        self.var_entry.grid(row= 0, column= 2, columnspan = 2, sticky= 'nsew')
        self.slider.grid(row= 1, column= 1, columnspan = 2, pady= 5, sticky= 'nsew')

    # Method for when the user hovers mouse over help button
    # def on_enter(self, event):
    #     if self.info_window: self.info_window.destroy()

    #     pdf = fitz.open('exploitation.pdf')
    #     page = pdf[0]
    #     pix = page.get_pixmap()
    #     image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    #     self.tk_image = ImageTk.PhotoImage(image = image)

    #     self.info_window = tk.Toplevel(self)
    #     self.info_window.title("Information")
    #     x, y = event.x_root + 10, event.y_root + 10
    #     self.info_window.geometry(f'{pix.width}x500+{x}+{y}')

    #     canvas = tk.Canvas(self.info_window, width = pix.width)
    #     canvas.create_image(0,0,anchor = 'nw', image = self.tk_image)
    #     canvas.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    # Method for when user leaves help button with mouse
    def on_leave(self, event):
        if self.info_window:
            self.info_window.destroy()

    def update_num(self, value):
        self.entry_text.set(f'{self.entry_var.get():.3f}')
        self.parent.update()

    def import_text(self, path_name):
        with open(os.path.join(CD, path_name),'r') as file:
            text = file.read()
            text_image_ctk = get_ctk_image(text, 'exploitation', size = 20)
            return text_image_ctk

    def update_slider(self, value):
        try:
            entry = float(value)
            self.slider.set(entry)
            return True
        except ValueError:
            if len(value.strip()) == 0:
                return True
            else:
                return False

    def get(self):
        return float(self.entry_text.get())

# class InitValueBlock(EntryBlock):
#     def __init__(self, parent, var_label, png_path, range, initial):


if __name__ == "__main__":
    root = App("Marx Visualizer", (800,600))

    root.mainloop()
    print(DPI)
