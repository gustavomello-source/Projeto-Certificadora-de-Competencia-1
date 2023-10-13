#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import tkinter as tk
from tkinter import ttk


# In[2]:


import pandas as pd
import json


# In[3]:


def create_table(canvas):
    global tree
    tree = ttk.Treeview(canvas,show="headings")
    tree["columns"] = ("Enunciado", "Tópico", "Dificuldade")
    tree.heading("Enunciado", text="Enunciado")
    tree.heading("Tópico", text="Tópico")
    tree.heading("Dificuldade", text="Dificuldade", command=lambda c="Dificuldade": sort_treeview(tree, c, False))
    tree.bind('<ButtonRelease-1>', on_line_click)
    
    fill_list(tree)
    
    tree.grid(row=0, column=0)
    tree.place(x=canvas.winfo_width(), y=canvas.winfo_height())
    print(canvas.winfo_width(), canvas.winfo_height())


# In[4]:


def fill_list(tree):
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row["question"], row["topic"], row["difficulty"]))


# In[5]:


def sort_treeview(tree, col, descending):
    difficulty_order = {"Difícil": 0, "Médio": 1, "Fácil": 2}

    data = [(difficulty_order.get(tree.set(item, col), float('inf')), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (_, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


# In[6]:


def resize_canvas(event):
    global color1, color2
    
    canvas.delete("all")
    
    color1, color2 = set_color()
    
    create_gradient_background(0, 0, event.width, event.height, color1, color2)


# In[7]:


def resize_table(event):
    
    tree_width = event.width * 0.9
    tree_height = event.height * 0.5
    
    tree.place(x=(event.width - tree_width) / 2, y=(event.height - tree_height) / 2, width=tree_width, height=tree_height)


# In[8]:


def on_line_click(event):
    selected_item = tree.selection()

    if selected_item:
        item = tree.selection()[0]
        values = tree.item(item, 'values')
        print("Values for clicked item:", values)
    else:
        print("No exercise selected")


# In[9]:


def create_gradient_background(x1, y1, x2, y2, color1, color2):
    # Direção do gradiente
    dx = x2 - x1
    dy = y2 - y1
    
    #Cálculo para interpolação das cores
    steps = max(dx, dy)
    step_r = (color2[0] - color1[0]) / steps
    step_g = (color2[1] - color1[1]) / steps
    step_b = (color2[2] - color1[2]) / steps
    
    
    
    for y in range(y1, y2):
        # Calculando cor
        r = int((color1[0] * (y2 - y) + color2[0] * (y - y1)) / (y2 - y1))
        g = int((color1[1] * (y2 - y) + color2[1] * (y - y1)) / (y2 - y1))
        b = int((color1[2] * (y2 - y) + color2[2] * (y - y1)) / (y2 - y1))
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        
        canvas.create_line(x1, y, x2, y, fill=hex_color)


# In[10]:


def set_color():
    c1 = (107, 31, 124)  # Rosa #A1405D
    c2 = (161, 64, 93)  # Roxo #6B1F7C
    return c1, c2


# In[11]:


def create_canvas(root, w, h):
    global canvas
    canvas = ctk.Canvas(root, width=w, height=h)
    canvas.pack(fill=tk.BOTH, expand=True)
    create_gradient_background(0, 0, w, h, color1, color2)


# In[12]:


def start_interface(root, w, h):
    global canvas, color1, color2
    canvas = tk.Canvas(root, width=w, height=h, bg="#A1405D", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind("<Configure>", resize_canvas)
    canvas.bind("<Configure>", resize_table)
    color1, color2 = set_color()
    create_gradient_background(0, 0, w, h, color1, color2)
    create_table(canvas)


# In[13]:


def awake_interface():
    #import data_module.ipynb
    read_data()
    root = tk.Tk()
    root.geometry("1280x780")
    root.title("Main Tab")
    height = 780
    width = 1280
    start_interface(root, width, height)
    root.mainloop()


# In[14]:


def install_dependencies():
    get_ipython().system('pip install tkinter')
    get_ipython().system('pip install tk')
    get_ipython().system('pip install pandas')


# In[15]:


def read_data():
    global df
    exercises_data_path = './data/exercises.csv'
    df = pd.read_csv(exercises_data_path)


# In[16]:


def get_dataframe():
    return df


# In[17]:


def main():
    awake_interface()


# In[18]:


if __name__ == "__main__":
    main()


# In[ ]:




