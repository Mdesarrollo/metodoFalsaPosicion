from math import *
from sympy import *
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

class NoConvergenceError(Exception):
    pass

class InvalidFunctionError(Exception):
    pass

#limpiar inputs
def clear_inputs():
    funcion_entry.delete(0, 'end')
    xl_entry.delete(0, 'end')                                                                           
    xu_entry.delete(0, 'end')
    porcentaje_entry.delete(0, 'end')
    clear_table()
#graficar funcion
def plot_function(expression_str, result_data):
    x = np.linspace(float(xl_entry.get()), float(xu_entry.get()), 400)
    y = lambdify(symbols('x'), sympify(expression_str))(x)

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=expression_str)

    roots_x = [float(row[2]) for row in result_data]
    roots_y = [lambdify(symbols('x'), sympify(expression_str))(root) for root in roots_x]
    plt.scatter(roots_x, roots_y, color='red', label='Raíces encontradas', marker='o')

    plt.title("Gráfica de la Función y Raíces Encontradas")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
#limpiar tabla
def clear_table():
    for item in tree.get_children():
        tree.delete(item)
# declaramos funcion para determinar si es valida o no la funcion a manejar
def is_valid_function(funcion, valor):
    x = symbols('x')
    try:
        func_expr = sympify(funcion)
        lambdify(x, func_expr)(valor)
        return True
    except Exception:
        return False

#evaluamos la funcion para encontrar los valores de la funcion evaluados
def evaluar(x):
    return round(eval(funcion_entry.get()),4)

def fala_posicion(error_relativo, xl, xu):
    
    if not is_valid_function(funcion_entry.get(), xl) or not is_valid_function(funcion_entry.get(), xu):
        raise InvalidFunctionError("La función no es válida en los puntos iniciales X_L y X_U.")
    
    #declaramos arrays donde almacenaremos los valores encontrados 
    tabla=[]
    porcentaje_error=100;
    
    #declaramos variable de conteo para saber el numero de iteraciones
    contador=0
    fin=100
    while(porcentaje_error>=error_relativo):

        #hallamos los valores evaludos en la funcion y el valor de xr
        fxl=evaluar(xl)
        fxu=evaluar(xu)
    
        try:
            xr = round(xu - ((fxu * (xl - xu)) / (fxl - fxu)), 4)
        except ZeroDivisionError:
            messagebox.showerror("Error",str("El metodo no converge division entre cero en XR"))
            return tabla
        
        fxr=evaluar(xr)
        
        #determinamos el error relativo porcentual y lo almacenamos en la tabla 
        if(contador == 0):
            porcentaje_error="####"
        else:
        
            try:
                porcentaje_error=abs(round(((xr-tabla[contador-1][2])/xr)*100,4))
            except ZeroDivisionError:
                porcentaje_error="error"
                messagebox.showerror("Error", str("division entre cero metodo no converge en hallar error relativo porcentual"))
                return tabla
                
        if(porcentaje_error=="####"):
            tabla.append([contador+1,xl,xr,xu,fxl,fxr,fxu,porcentaje_error])
            porcentaje_error=100
        else:
            tabla.append([contador+1,xl,xr,xu,fxl,fxr,fxu,porcentaje_error])
            
        #determinamos nuevos intervalos
        if(fxl*fxu>=0):
            
            messagebox.showerror("Error",str(f"metodo no converge fxl*fxu > 0 => '{fxl*fxu}' ")) 
            return tabla
        else:
            if((fxl <= 0) and (fxr <= 0 )):
                xl=xr
            elif((fxu<=0) and (fxr<=0)):
                xu=xr
            elif((fxl>=0) and (fxr>=0)):
                xl=xr
            elif((fxu>=0) and (fxr>=0)):
                xu=xr
            else:
                messagebox.showerror("Error",str("todos los signos son iguales no es posible continuar "))
                return tabla
        contador+=1
        if(contador==fin):
            return tabla
    return tabla
#se crea el tablero de valores 
def tablero (error,XL,XU):
    
    try:
        error_relativo=float(error)
        xl=float(XL)
        xu=float(XU)
        result_data = fala_posicion(error_relativo,xl,xu)
        clear_table()
        for row_data in result_data:
            tree.insert('', 'end', values=row_data)
        plot_function(funcion_entry.get(),result_data)
    except (InvalidFunctionError, ValueError,NoConvergenceError) as e:
        messagebox.showerror("Error", str(e))
    
# creamos interfazes

# creamos interfaz de instrucciones 
def crear_ventana1():
    #creamos ventana de inicio e instruciones
    root=Tk()
    root.geometry("1000x500")
    root.title("Falsa posicion")
    root.config(bg="cadet blue")
    
    #Titulo de la ventana de instrucciones o presentacion de la interfaz
    titulo=Label(root, text="Metodo de falsa posicion",font=('Curier', '20','bold'),bg="cadet blue",fg="white")
    titulo.place(x=350,y=0)
    # subTitulo de la ventana de instruciones 
    sub_titulo=Label(root, text="Instrucciones a seguir ",font=('Curier', '10','bold'),bg="cadet blue",fg="white")
    sub_titulo.place(x=450,y=50)

    #Indicacion de las recomendaciones a seguir
    Label(root, text="Recomendaciones ", font=('Curier', '15','bold'),bg="cadet blue",fg="white").place(x=20,y=100)

    Label(root,text="-> Al momento de generar el exponente hacia un valor base, Encerrarlo en parentesis 'x^(2)' ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=140)
    Label(root,text="-> Al momento de ingresar variables no ingresar ninguna diferente de  'X' ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=160)
    Label(root,text="-> Al momento de ingresar los valores numericos en sus campos no ingresar letras ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=180)
    Label(root,text="-> Al momento de ingresar el porcentaje no realizar conversiones poner el del ejercicio determinado '%' ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=200)
    Label(root,text="-> Al momento de ingresar logaritmo neperiano 'log()' colocar su base para trabajar 'log(x,10) '",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=220)
    Label(root,text="-> Al momento de ingresar el logaritmo natural no es necesario que ponga la base  'log(x)' ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=240)   
    Label(root,text="-> Al momento de usar lso tableros estos solo afectan la caja de texto para la funcion los demas deebn ser ingresados por teclado para mayor control por el usuario ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=260)   
    Label(root,text="-> Los signos que el usuario puede manejar son ' * , + , - , / ' estos son ingresaos por teclado donde representan multiplicacion, suma, resta y division ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=280)   
    Label(root,text="-> Al momento de selcionar o escribir la funciones solo se permiten las expuestas en la interfaz ",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=300)   
    Label(root,text="-> Recuerda que hacer bien el proceso dara una buena respuesta ",font=('Curier', '15','bold'),bg="cadet blue",fg="white").place(x=20,y=350)
    
    iniciar=Button(root,text="Inciar ↑",font=('helvetica', '10','bold'),width=50,height=2,bg="gray64",bd=5,command=root.destroy)
    iniciar.place(x=300,y=400)

    root.mainloop()
    
crear_ventana1()

root2=Tk()
root2.geometry("950x650")
root2.config(bg="cadet blue")
root2.title("Pedir datos")
Label(root2,text="Metodo Falsa Posicion 😎",font=('Curier', '20','bold'),bg="cadet blue").pack()

Label(root2,text="Valores de Entrada ",font=('Curier', '15','bold'),bg="cadet blue").place(x=50,y=100)
Label(root2,text="Funcion",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=150)
funcion_entry=Entry(root2,name="funcion",bd=4)
funcion_entry.place(x=130,y=150)   

Label(root2,text="XL-Entrada",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=180)
xl_entry=Entry(root2,name="xl",bd=4)
xl_entry.place(x=130,y=180) 

Label(root2,text="XU-Entrada",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=210)
xu_entry=Entry(root2,name="xu",bd=4)
xu_entry.place(x=130,y=210) 

Label(root2,text="Porcentaje %",font=('Curier', '10','bold'),bg="cadet blue").place(x=20,y=240)
porcentaje_entry=Entry(root2,name="porcentaje",bd=4)
porcentaje_entry.place(x=130,y=240) 

#enviar valores a caja de texto para la funcion
def enviar_numero(valor):
    
    posicion_cursor=funcion_entry.index(tk.INSERT)
    funcion_entry.insert(posicion_cursor,valor)
    
#envio del '.' y '^'
def enviar_simbolos(simbolo):
    posicion_cursor=funcion_entry.index(tk.INSERT)
    
    if(simbolo=="^"):
        funcion_entry.insert(posicion_cursor,"**()")
    else:
        funcion_entry.insert(posicion_cursor,simbolo)
    
#tablero numerico
Label(root2,text="Valores Numericos ",font=('Curier', '15','bold'),bg="cadet blue").place(x=350,y=100)
tablero_numeros=ttk.Frame(root2)
tablero_numeros.place(x=365,y=150)

numero1=Button(tablero_numeros,text="1",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(1))
numero1.grid(row=0,column=0)
    
numero2=Button(tablero_numeros,text="2",width=4,height=3,bg="gray64",font=('curier','10','bold'),command=lambda: enviar_numero(2))
numero2.grid(row=0,column=1)

numero3=Button(tablero_numeros,text="3",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(3))
numero3.grid(row=0,column=2)

numero4=Button(tablero_numeros,text="4",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(4))
numero4.grid(row=0,column=3)

numero5=Button(tablero_numeros,text="5",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(5))
numero5.grid(row=1,column=0)

numero6=Button(tablero_numeros,text="6",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(6))
numero6.grid(row=1,column=1)

numero7=Button(tablero_numeros,text="7",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(7))
numero7.grid(row=1,column=2)

numero8=Button(tablero_numeros,text="8",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(8))
numero8.grid(row=1,column=3)

numero9=Button(tablero_numeros,text="9",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(9))
numero9.grid(row=2,column=0)

numero0=Button(tablero_numeros,text="0",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_numero(0))
numero0.grid(row=2,column=1)

punto=Button(tablero_numeros,text=".",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_simbolos('.'))
punto.grid(row=2,column=2)

exponente=Button(tablero_numeros,text="^",width=4,height=3,bg="gray64",font=('curier','10','bold'), command=lambda: enviar_simbolos('^'))
exponente.grid(row=2,column=3)

#creamos funcion para mandar los valores del tablero a la caja de texto de funcion
funcionVar=StringVar()
def funciones():
    
    if(funcion_entry.get()==""):
        
        funciones=["e","sen()","cos()","tan()","log()","sqrt()"]
        posicion_cursor=funcion_entry.index(tk.INSERT)
        for fun in range(0,len(funciones)):
            if(funcionVar.get()==funciones[fun]):
                if(funcionVar.get()=="sen()"):
                    funcion_entry.insert(posicion_cursor,"sin()")
                else:
                    funcion_entry.insert(posicion_cursor,funcionVar.get())
                
    else:
        funciones=["e","sen()","cos()","tan()","log()","sqrt()"]
        posicion_cursor=funcion_entry.index(tk.INSERT)
        for fun in range(0,len(funciones)):
            if(funcionVar.get()==funciones[fun]):
                if(funcionVar.get()=="sen()"):
                    funcion_entry.insert(posicion_cursor,"sin()")
                else:
                    funcion_entry.insert(posicion_cursor,funcionVar.get())
                
# Tablero de Funciones  
Label(root2,text="Funciones ",font=('Curier', '15','bold'),bg="cadet blue").place(x=640,y=100)
tablero_funcion=ttk.Frame(root2)
tablero_funcion.place(x=620,y=150)
tablero_funcion.config()

Euler=Radiobutton(tablero_funcion,text="e",value="e",width=3,height=2,variable=funcionVar,command=funciones)
Euler.grid(row=0,column=0)

logaritmo=Radiobutton(tablero_funcion,text="Log()",value="log()",width=3,height=2,variable=funcionVar,command=funciones)
logaritmo.grid(row=0,column=1)#para este debemos porner en las instruciones que ponga la base o si no lo trbaja como ln()

raiz=Radiobutton(tablero_funcion,text="√",value="sqrt()",width=3,height=2,variable=funcionVar,command=funciones)
raiz.grid(row=0,column=2)

seno=Radiobutton(tablero_funcion, text="sen()",value="sen()",variable=funcionVar,command=funciones)
seno.grid(row=1,column=0)

coseno=Radiobutton(tablero_funcion, text="cos()",value="cos()",variable=funcionVar,command=funciones)
coseno.grid(row=1,column=1)

tangente=Radiobutton(tablero_funcion, text="tan()",value="tan()",variable=funcionVar,command=funciones)
tangente.grid(row=1,column=2)

#crecion del boton de calcular
bot=Button(root2,text="calcular 🤓",bg="gray64",font=('curier','10','bold'),command=lambda:tablero(porcentaje_entry.get(),xl_entry.get(),xu_entry.get()))
bot.place(x=590,y=270)

#creacion de boton para limpiar datos
clear_button =Button(root2, text="Borrar Datos ☠",bg="gray64",font=('curier','10','bold'), command=clear_inputs)
clear_button.place(x=680,y=270)

#boton para recordar instruciones
instrucciones=Button(root2,text="⚙️",bg="gray64",font=('curier','10','bold'),command=crear_ventana1)
instrucciones.place(x=800,y=270)

#creamos estilos para el color claro de la tabla del programa
def lite_mode():
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        style="Treeview",
        background="white",
        fieldbackground="white",
        foreground="black"
    
    )

    style.configure(
    
        style="Treeview.Heading",   
        font=('Helvetica', '10', 'bold'),
        background="gray64",
        fieldbackground="white",
        foreground="black"
    )
    
lite_mode()

#estilos de tabla oscuro
def dark():
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        style="Treeview",
        background="RoyalBlue4",
        fieldbackground="RoyalBlue4",
        foreground="white"
    
    )

    style.configure(
    
        style="Treeview.Heading",   
        font=('Helvetica','10', 'bold'),
        background="RoyalBlue4",
        fieldbackground="RoyalBlue4",
        foreground="white"
    )

    
#Boton modo oscuro
dark_boton=Button(root2,text="Dark borad",font=('curier','10','bold'),command=dark,bg="RoyalBlue4")
dark_boton.place(x=850,y=290)

#Boton modo claro
dark_boton=Button(root2,text="lite board",font=('curier','10','bold'),command=lite_mode,bg="RoyalBlue4")
dark_boton.place(x=850,y=250)

#creamos tabla para la meustra de los valores
columns = ['Iteración', 'X_L', 'X_R', 'X_U', 'f(X_L)', 'f(X_R)', 'f(X_U)', '|e_a|']
tree = ttk.Treeview(root2, columns=columns, show='headings',height=13)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=110)
tree.place(x=30,y=350)

root2.mainloop()