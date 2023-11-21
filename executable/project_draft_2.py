#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import tkinter as tk
from tkinter import ttk


# In[2]:


import pandas as pd


# In[3]:


def create_table(canvas):
    global tree

    tree = ttk.Treeview(
        canvas, 
        show="headings",
        selectmode="browse",
        height=10,
        padding=10,
    )
    
    tree["columns"] = ("Enunciado", "Tópico", "Dificuldade")
    tree.heading("Enunciado", text="Enunciado")
    tree.heading("Tópico", text="Tópico")
    tree.heading("Dificuldade", text="Dificuldade", command=lambda c="Dificuldade": sort_treeview(tree, c, False))
    tree.bind('<ButtonRelease-1>', on_line_click)

    fill_list(tree)

    print("Created Treeview")
    return tree


# In[4]:


def fill_list(tree):
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row["question"], row["topic"], row["difficulty"]))


# In[5]:


def create_text_box(canvas):
    global text_box
    text_box = tk.Text(
        canvas,
        height=11, 
        width=120,  
    )

    canvas.create_window(550, 300, window=text_box) 

    text_box.pack(expand=False)
    text_box.insert('end', "Question")
    text_box.config(state='disabled')

    print("Created Text Box")
    return text_box


# In[6]:


def create_input_fields(canvas, var_names, var_values):
    global input_entries
    index = 0
    
    label_list = []
    entry_list = []
    button_list = []

    label = tk.Label(canvas, text=f"Resposta:")
    label.pack()
    label_list.append(label)

    entry = tk.Entry(canvas)
    entry.pack()
    entry_list.append(entry)
    

    for variable in var_names:
        label = tk.Label(canvas, text=f"{variable}:")
        label.pack()
        label_list.append(label)

        entry = tk.Entry(canvas)
        entry.pack()
        entry.insert(0, str(var_values[index]))
        entry_list.append(entry)
        index = index + 1

    read_button = tk.Button(canvas, text="Resolver Exercício", command=solve_button_clicked)
    read_button.pack()
    button_list.append(read_button)

    input_entries = [label_list, entry_list, button_list]


# In[7]:


def solve_button_clicked():
    global current_exercise
    global df
    
    if(df['solved'].iloc[current_exercise] == False):
        call_solve_question()
    else:
        notify_solved_question()


# In[8]:


def call_solve_question():
    global current_exercise
    
    if(current_exercise == 0):
        answer = solve_question_1()
    elif(current_exercise == 1):
        answer = solve_question_2()
    elif(current_exercise == 2):
        answer = solve_question_3()
    elif(current_exercise == 3):
        answer = solve_question_4()
    elif(current_exercise == 4):
        answer = solve_question_5()
    elif(current_exercise == 5):
        answer = solve_question_6()
    elif(current_exercise == 6):
        answer = solve_question_7()
    elif(current_exercise == 7):
        answer = solve_question_8()
    elif(current_exercise == 8):
        answer = solve_question_9()
    elif(current_exercise == 9):
        answer = solve_question_10()
        
    fill_answer_box(answer)
    df.loc[current_exercise, 'solved'] = True


# In[9]:


def notify_solved_question():
    
    global root
    popup = tk.Toplevel(root)
    
    popup.title("AVISO")

    label = tk.Label(popup, text="O exercício selecionado já foi resolvido. Resolver novamente?")
    label.pack(pady=10)

    yes_button = tk.Button(popup, text="Sim", command=lambda: [popup.destroy(), call_solve_question()])
    yes_button.pack(side="left", padx=10, pady=5)

    no_button = tk.Button(popup, text="Não", command=popup.destroy)
    no_button.pack(side="right", padx=10, pady=5)


# In[10]:


def fill_answer_box(text):
    global input_entries
    
    entry = input_entries[1][0]
    entry.delete(0, 'end')
    entry.insert(0, text)


# In[11]:


def fill_text_box(text):
    global text_box
    text_box.config(state='normal')
    text_box.delete('1.0', 'end')  # Clear existing content
    text_box.insert('end', text)
    text_box.config(state='disabled')


# In[12]:


def sort_treeview(tree, col, descending):
    difficulty_order = {"Difícil": 0, "Médio": 1, "Fácil": 2}

    data = [(difficulty_order.get(tree.set(item, col), float('inf')), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (_, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


# In[13]:


def resize_canvas(event):
    global color1, color2
    
    canvas.delete("all")
    
    color1, color2 = set_color()
    
    create_gradient_background(0, 0, event.width, event.height, color1, color2)


# In[14]:


def resize_table(event):
    print("CALLED RESIZE TABLE")
    tree_width = event.width * 0.9
    
    tree.place(x=(event.width - (tree_width/2)) / 2, y=(450))


# In[15]:


def on_line_click(event):
    global current_exercise #para qualquer elemento poder sempre acessar
    
    selected_item = tree.selection()
    delete_input_entries()
    
    if selected_item:
        item = tree.selection()[0]
        question_text = tree.item(item, "values")[0]
        
        print("Values for clicked item:", question_text)
        print(tree.item(item, "values"))
        
        var_names = get_var_names_from_line(tree.index(item))
        var_values = get_var_values_from_line(tree.index(item))
        create_input_fields(canvas, var_names, var_values)
        
        current_exercise = tree.index(item)
        
        fill_text_box(question_text)
    else:
        print("No exercise selected")
        fill_text_box("No exercise selected")


# In[16]:


def delete_input_entries():
    global input_entries
    
    for label in input_entries[0]:
        label.destroy()

    for entry in input_entries[1]:
        entry.destroy()
        
    for button in input_entries[2]:
        button.destroy()


# In[17]:


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


# In[18]:


def set_color():
    c1 = (107, 31, 124)  # Rosa #A1405D
    c2 = (161, 64, 93)  # Roxo #6B1F7C
    return c1, c2


# In[19]:


def create_canvas(root, w, h):
    global canvas
    canvas = ctk.Canvas(root, width=w, height=h)
    canvas.pack(fill=tk.BOTH, expand=True)
    create_gradient_background(0, 0, w, h, color1, color2)


# In[20]:


def start_interface(root, w, h):
    global canvas, color1, color2
    global text_box
    canvas = tk.Canvas(root, width=w, height=h, bg="#A1405D", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind("<Configure>", configure_canvas)
    
    color1, color2 = set_color()
    
    create_table(canvas)
    text_box = create_text_box(canvas)
    create_input_fields(canvas, get_var_names_from_line(0), get_var_values_from_line(0))
    
    root.mainloop()


# In[21]:


def awake_interface():
    global input_entries #variável para input_fields
    global root
    input_entries = []
    
    root = tk.Tk()
    root.geometry("1280x780")
    root.title("Main Tab")
    height = 780
    width = 1280
    start_interface(root, width, height)


# In[22]:


def awake_data():
    global current_exercise
    global var_names, var_values
    global df
    
    read_data()
    current_exercise = 0 #padrão
    var_names, var_values = (decode_variables(df))
    


# In[23]:


def configure_canvas(event):
    resize_canvas(event)
    resize_table(event)


# In[24]:


def install_dependencies():
    get_ipython().system('pip install tkinter')
    get_ipython().system('pip install tk')
    get_ipython().system('pip install pandas')


# In[25]:


def read_data(): #FROM DATA_MODULE
    global df
    exercises_data_path = './data/exercises.csv'
    df = pd.read_csv(exercises_data_path)


# In[26]:


def get_dataframe(): #FROM DATA_MODULE
    return df


# In[27]:


def decode_variables(df): #FROM DATA MODULE
    global var_names
    var_names = []
    
    global var_values
    var_values = []
    
    for row in df['variables']:
        variables = row.split(';')
        var_dict = {}
        
        for variable in variables:
            var_parts = variable.split('=')
            if len(var_parts) == 2:
                var_name, var_value = var_parts
                var_dict[var_name] = float(var_value) #converte strings em floats
        
        var_names.append(var_dict.keys())
        var_values.append(var_dict.values())
        
    return var_names, var_values


# In[28]:


def get_var_names_from_line(index): #FROM DATA MODULE
    global df
        
    names = []
    
    variables = df['variables'].str.split(';').iloc[index]
    
    for variable in variables:
        var_parts = variable.split('=')
        
        if len(var_parts) == 2:
            var_name, var_value = var_parts
            names.append(var_name)
        
    return names


# In[29]:


def get_var_values_from_line(index):
    global df
    
    values = []
    
    variables = df['variables'].str.split(';').iloc[index]
    
    for variable in variables:
        var_parts = variable.split('=')
        
        if len(var_parts) == 2:
            var_name, var_value = var_parts
            values.append(var_value)
        
    return values


# In[30]:


def get_exercise_variables(id):
    global var_names, var_values
    exercise_variable_names = []
    exercise_variable_values = []
    
    for var in var_names[id]:
        exercise_variable_names.append(var)
        
    
    for var in var_values[id]:
        exercise_variable_values.append(var)
    
    print(exercise_variable_names, exercise_variable_values)
    
    return exercise_variable_names, exercise_variable_values


# In[31]:


def solve_question_1():
    var_names, var_values = get_exercise_variables(0)
    

    saltos = var_values[var_names.index('saltos')]
    tempo = var_values[var_names.index('tempo')]
    raio = var_values[var_names.index('raio')]
    
    velocidade = (saltos*2*3*(raio/100))/tempo
    #Considerando 1 salto a cada volta, são 105 voltas (n) em 30 s (Δt). v=ΔS/Δt => n*(2πR)/Δt => (105*2*3*0,9)/30 => v=18,9m/s
        
    reposta = str(velocidade) + "m/s"
    
    return reposta


# In[32]:


def solve_question_2(): 
    var_names, var_values = get_exercise_variables(1)

    velocidade_linear = var_values[var_names.index('linear_vel')]
    diametro = var_values[var_names.index('diametro')]
    
    tempo = ((3 * diametro * 10**-2) / ((velocidade_linear * 100) * 10**-2))
    #v=ΔS/Δt => v=πd/T => T=πd/v => T= (3*6*10^-2)/(4,5*10^-2) => T=4,0s

    resposta = str(tempo) + "s"
    
    return resposta


# In[33]:


def solve_question_3(): 
    var_names, var_values = get_exercise_variables(2)

    potencia = var_values[var_names.index('potencia')]
    consumo = var_values[var_names.index('consumo')]
    tensao = var_values[var_names.index('tensao')]

    media_banho = (consumo / (potencia/1000)) * (60/30)
    #P=ΔE/Δt => Δt= ΔE/P => Δt =42/7 [(kWh/mês)/kW] => Δt= 6 [h/mês] => 6[60min/30dias] => Δt=12min/dia

    resposta = str(media_banho) + "min/dia"
    
    return resposta


# In[34]:


def solve_question_4(): 
    var_names, var_values = get_exercise_variables(3)

    carga = var_values[var_names.index('carga')]
    tensao = var_values[var_names.index('tensao')]
    
    carga_C = (carga/1000) * 3600
    #Q=iΔt => Q=4000mA*h = 4 A * 3600s => Q= 14400C
    
    resposta = str(carga_C) + "C"

    return resposta


# In[35]:


def solve_question_5(): 
    var_names, var_values = get_exercise_variables(4)

    f1 = var_values[var_names.index('f1')]
    f2 = var_values[var_names.index('f2')]
    angulo = var_values[var_names.index('angulo')]
    
    FR = math.sqrt(f1**2 + f2**2 + (2 * f1 * f2 * 0.5))
    #FR = √(F1^2+F2^2+2*F1*F2*cos60) => FR = √(8^2+9^2+2*8*9*0,5) => FR= 14,7N (nos exercícos o resultado está como 17,7N)

    resposta = str(round(FR, 3)) + "N"   
    
    return resposta


# In[36]:


def solve_question_6(): 
    var_names, var_values = get_exercise_variables(5)

    campo = var_values[var_names.index('campo')]
    deslocamento = var_values[var_names.index('deslocamento')]
    comprimento = var_values[var_names.index('comprimento')]
    
    U = campo * comprimento 
    i = deslocamento / (10**-3)  
    p = U * i  
    P = p / (10**9) 
    #Calculando a tensão: U=Ed=10^4*100 => U=10^6V. Calculando a Corrente: i= Q/Δt = 30/10^-3 => i=30*10^3A. Aplicando a expressão da potência elétrica: P=Ui => P=10^6*30*10^3 => P= 30*10^9W => P= 30GW
   
    resposta = str(P) + "GW"

    return resposta


# In[37]:


def solve_question_7(): 
    var_names, var_values = get_exercise_variables(6)

    bateria = var_values[var_names.index('bateria')]
    U = var_values[var_names.index('U')]
    i = var_values[var_names.index('i')]
    
    R = (bateria - U) / i
    #A força eletromotriz da Bateria (E) é ogual à ddp (diferença de potencial) na lâmpada (U) somada com a ddp no resistor (UR). Assim: E=U+UR => E=U+Ri => 9=5,7+R(0,15) => R= (9-5,7)/0,15 = 3,3/0,15 => R=22Ω
   
    resposta = str(R) + "Ω"

    return resposta


# In[38]:


def solve_question_8():
    var_names, var_values = get_exercise_variables(7)
    
    rendimento = var_values[var_names.index('rendimento')]
    velocidade = var_values[var_names.index('velocidade')] / 3.6
    insol = var_values[var_names.index('insol')]
    massa = var_values[var_names.index('massa')]
    area = var_values[var_names.index('area')]

    # Calculando o tempo
    tempo = ((massa * (velocidade**2)) / (2 * rendimento * insol * area)) * 100
    
    resposta = str(tempo) + "s"
    
    return resposta


# In[39]:


def solve_question_9():
    var_names, var_values = get_exercise_variables(8)
    
    acel = var_values[var_names.index('acel')]
    desacel = var_values[var_names.index('desacel')]
    vel1 = var_values[var_names.index('vel1')]
    tempo = var_values[var_names.index('tempo')]
    
    espaco1 = (vel1**2) / (2 * desacel)
    
    espaco2 = ((vel1 + 1)**2 - vel1**2) / (2 * acel)
    
    espaco3 = ((vel1 + 1)**2) / (10)
    
    espaco = espaco3 + espaco2 - espaco1
    
    resposta = str(espaco) + "m"
    
    return resposta


# In[40]:


def solve_question_10():
    var_names, var_values = get_exercise_variables(9)
    
    temp1 = var_values[var_names.index('temp1')]
    temp2 = var_values[var_names.index('temp2')]
    prop = var_values[var_names.index('prop')]
    
    temp_final = int((temp1 + temp2) / (prop/10))
    
    variacao = (temp_final / 30) * 100    
    
    if(variacao < 10):
        resposta = "Selo A"
    elif (25 > variacao > 10):
        resposta = "Selo B"
    elif (40 > variacao > 25):
        resposta = "Selo C"
    elif (55 > variacao > 40):
        resposta = "Selo D"
    elif (variacao > 55):
        resposta = "Selo E"
        
    return resposta


# In[41]:


def main():
    awake_data()
    awake_interface()


# In[42]:


if __name__ == "__main__":
    main()


# In[ ]:




