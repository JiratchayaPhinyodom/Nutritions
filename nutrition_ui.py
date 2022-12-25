import sys
import tkinter as tk
from tkinter import ttk
from nutrition import Get, Get_Value
import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class NutritionUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.menu = Get("Menu").get()
        self.combobox = Get("Combobox").get()
        self.usrd = Get("Usrd").get()
        self.usrd_value = Get_Value("Usrd_Value")
        self.compare_value = Get_Value("Compare_Value")
        self.rank = Get_Value("Rank")

        self.title("Food Nutrition")
        self.geometry("1500x1500")

        self.search_text = tk.StringVar()
        self.search_food_one = tk.StringVar()
        self.search_food_two = tk.StringVar()
        self.list_menu = tk.StringVar(value=self.menu)
        self.select_compare_combobox = tk.StringVar()
        self.select_nutrition_combobox = tk.StringVar()
        self.radio_food = tk.StringVar()
        self.init_component()

    def init_component(self):
        #main
        self.main = tk.Label(self, text="Food Nutrition Menu", font=("Abadi MT", 20))
        self.main.place(x=650, y=5)

        self.scroll_bar = ttk.Scrollbar(self)

        #listbox show
        self.listbox_menu = tk.Listbox(self, listvariable=self.list_menu, selectmode='extended', width=100, height=10,
                                       yscrollcommand=self.scroll_bar.set)
        self.listbox_menu.place(x=300, y=50)
        self.listbox_menu.bind('<<ListboxSelect>>', self.food_selected)
        self.scroll_bar.config(command=self.listbox_menu.yview)
        self.scroll_bar.pack(side='left', fill='y')
        self.scroll_bar.place(x=280, y=100)


        #search button and search entry
        self.selected_main = ttk.Radiobutton(self, text="Select", value='Value1', variable=self.radio_food,
                                             command=self.clear_handler)
        self.selected_main.place(x=50, y=250)
        self.selected = tk.Entry(self, textvariable=self.search_text, font=("Monospace", 10), width=30)
        self.selected.place(x=125, y=250)
        self.selected['state'] = 'readonly'


        #comapare 2 food and 2 entry of 2 food
        self.compare_food1 = ttk.Radiobutton(self, text="Select Food 1", value='Value2', variable=self.radio_food,
                                             command=self.clear_handler)
        self.compare_food1.place(x=475, y=250)
        self.search_food1 = tk.Entry(self, textvariable=self.search_food_one, font=("Monospace", 10), width=30)
        self.search_food1.place(x=610, y=250)
        self.search_food1['state'] = 'readonly'

        self.compare_food2 = ttk.Radiobutton(self, text="Select Food 2", value='Value3', variable=self.radio_food,
                                             command=self.clear_handler)
        self.compare_food2.place(x=475, y=300)
        self.search_food2 = tk.Entry(self, textvariable=self.search_food_two, font=("Monospace", 10), width=30)
        self.search_food2.place(x=610, y=300)
        self.compare_food2['state'] = 'readonly'

        #select botton combobox
        self.compare_combobox_botton = ttk.Radiobutton(self, text="Compare", value='Value4', variable=self.radio_food,
                                                       command=self.clear_handler)
        self.compare_combobox_botton.place(x=475, y=350)
        self.compare_combobox = ttk.Combobox(self, textvariable=self.select_compare_combobox, font=("Monospace", 10)
                                             , width=25)
        self.compare_combobox.place(x=610, y=350)
        self.compare_combobox['state'] = 'readonly'
        self.compare_combobox['values'] = self.combobox

        #rank
        self.top_rank = ttk.Radiobutton(self, text="Top 10", value='Value5', variable=self.radio_food,
                                        command=self.clear_handler)
        self.top_rank.place(x=900, y=250)
        self.rank_combobox = ttk.Combobox(self, textvariable=self.select_nutrition_combobox, font=("Monospace", 10)
                                          , width=25)
        self.rank_combobox.place(x=1000, y=250)
        self.rank_combobox['state'] = 'readonly'
        self.rank_combobox['values'] = self.combobox

        #rank progressbar
        self.bar_rank = ttk.Progressbar(self, mode="determinate", length=300)
        self.status_rank = ttk.Label(self, text="Stopped")
        self.start_rank = ttk.Button(self, text="Start", command=self.run_rank)

        self.bar_rank.place(x=1000, y=300)
        self.start_rank.place(x=1225, y=250)
        self.status_rank.place(x=1000, y=350)

        #search progressbar
        self.bar_search = ttk.Progressbar(self, mode="determinate", length=390)
        self.status_search = ttk.Label(self, text="Stopped")
        self.start_search = ttk.Button(self, text="Start", command=self.run_search)

        self.bar_search.place(x=50, y=300)
        self.status_search.place(x=50, y=350)
        self.start_search.place(x=355, y=250)

        #compare progressbar
        self.bar_compare = ttk.Progressbar(self, mode="determinate", length=150)
        self.status_compare = ttk.Label(self, text="Stopped")
        self.start_compare = ttk.Button(self, text="Start", command=self.run_compare)

        self.start_compare.place(x=475, y=400)
        self.bar_compare.place(x=610, y=400)
        self.status_compare.place(x=775, y=400)

        #exit button
        self.exit_button = ttk.Button(self, text="Exit", command=self.exit)
        self.exit_button.place(x=1300, y=700)

        #create Matpotlib figure and plotting
        self.fig = Figure(figsize=(12, 4.5))
        self.axes = self.fig.add_subplot()

        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.fig_canvas.get_tk_widget().place(x=200, y=425)

    def exit(self):
        """exit() function that will close the all system."""
        sys.exit()

    def plot_usrda(self):
        """plot_usrda() function that will plot the all of nutrition in usrda and show the barh on the screen."""
        self.axes.clear()
        self.fig.subplots_adjust(left=0.30, right=0.95)
        search_txt = str(self.search_text.get())
        list_value = self.usrd_value.get_value(search_txt)
        df = pd.DataFrame({search_txt: self.usrd, 'Nutrition': list_value})
        df.plot(kind='barh', x=search_txt, y='Nutrition', ax=self.axes)
        self.axes.set(title=search_txt)
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        self.fig_canvas.draw()

    def plot_compare(self):
        """plot_compare() function that will plot the 2 different food of 1 nutrition and show the bar on the screen."""
        value_compare = str(self.select_compare_combobox.get())
        self.axes.clear()
        self.fig.subplots_adjust(bottom=0.25)
        food1 = str(self.search_food_one.get())
        food2 = str(self.search_food_two.get())
        list_value_compare = self.compare_value.get_value(value_compare, food1, food2)
        df = pd.DataFrame({'Compare Food': [food1, food2], value_compare: list_value_compare})
        df.plot(kind='bar', x='Compare Food', y=value_compare, ax=self.axes, rot=0)
        self.axes.set(title=value_compare)
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        self.fig_canvas.draw()

    def plot_rank(self):
        """plot_rank() function that will plot the top 10 of each nutrition and that will show barh on the screen."""
        value_rank = str(self.select_nutrition_combobox.get())
        self.axes.clear()
        self.fig.subplots_adjust(left=0.30, right=0.95)
        rank_shortdescrip = self.rank.get_value('ShortDescrip', value_rank)
        rank_value = self.rank.get_value(value_rank, value_rank)
        df = pd.DataFrame({'Food Nutrition top 10': rank_shortdescrip, value_rank: rank_value})
        df.plot(kind='barh', x='Food Nutrition top 10', y=value_rank, ax=self.axes)
        self.axes.set(title=value_rank)
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        self.fig_canvas.draw()

    def run_rank(self):
        """run_rank() function that will show the running... on the terminal when the program are running.
        And this function that will run the task_rank() and plot graph."""
        print("Running....")
        self.task_rank()
        self.plot_rank()

    def task_rank(self):
        """task_rank() function that will config the labels of start and status.And set the time of searching."""
        self.start_rank.config(state="disabled")
        self.status_rank.config(text="Running...")
        for i in range(101):
            time.sleep(0.1)
            self.bar_rank.config(value=i)
        self.start_rank.config(state="enabled")
        self.status_rank.config(text="Done.")

    def run_compare(self):
        """run_compare() function that will show the running... on the terminal when the program are running.
        And this function that will run the task_compare() and plot graph."""
        print("Running....")
        self.task_compare()
        self.plot_compare()

    def task_compare(self):
        """task_compare() function that will config the labels of start and status.And set the time of searching."""
        self.start_compare.config(state="disabled")
        self.status_compare.config(text="Running...")
        for i in range(101):
            time.sleep(0.1)
            self.bar_compare.config(value=i)
        self.start_compare.config(state="enabled")
        self.status_compare.config(text="Done.")

    def run_search(self):
        """run_search() function that will show the running... on the terminal when the program are running.
        And this function that will run the task_search() and plot graph."""
        print("Running....")
        self.task_search()
        self.plot_usrda()

    def task_search(self):
        """task_search() function that will config the labels of start and status.And set the time of searching."""
        self.start_search.config(state="disabled")
        self.status_search.config(text="Running...")
        for i in range(101):
            time.sleep(0.1)
            self.bar_search.config(value=i)
        self.start_search.config(state="enabled")
        self.status_search.config(text="Done.")

    def food_selected(self, event):
        """food_selected() function will selected the food in the listbox of each radiobutton."""
        self.clear_handler()
        if self.radio_food.get() == 'Value1':
            self.select_indices = self.listbox_menu.curselection()
            self.search_text.set(self.menu[int(self.select_indices[0])])
        if self.radio_food.get() == 'Value2':
            self.select_indices_f1 = self.listbox_menu.curselection()
            self.search_food_one.set(self.menu[int(self.select_indices_f1[0])])
        if self.radio_food.get() == 'Value3':
            self.select_indices_f2 = self.listbox_menu.curselection()
            self.search_food_two.set(self.menu[int(self.select_indices_f2[0])])

    def clear_handler(self):
        """clear_handler() function will clear the entry of another radiobutton that the users not selected."""
        if self.radio_food.get() == 'Value1':
            self.search_food_two.set('')
            self.search_food_one.set('')
            self.select_nutrition_combobox.set('')
            self.select_compare_combobox.set('')
        if self.radio_food.get() == 'Value5':
            self.search_food_two.set('')
            self.search_food_one.set('')
            self.search_text.set('')
            self.select_compare_combobox.set('')
        if self.radio_food.get() == 'Value2' or self.radio_food.get() == 'Value3' or self.radio_food.get() == 'Value4':
            self.search_text.set('')
            self.select_nutrition_combobox.set('')

    def run(self):
        """run() function that will run mainloop"""
        self.mainloop()
