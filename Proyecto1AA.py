import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image
from tkinter import filedialog
from PIL import Image,ImageTk
import random
import time
import pygame

Pistas=[["Amigo","Novio","Vecino","Mensajero","Extraño","Hermanastro","Colega"],
        ["Pistola","Cuchillo","Machete","Pala","Bate","Botella","Tubo","Cuerda"],
        ["Venganza","Celos","Dinero","Accidente","Drogas","Robo"],
        ["Cabeza","Pecho","Abdomen","Espalda","Piernas","Brazos"],
        ["Sala","Comedor","Baño","Terraza","Cuarto","Garage","Patio","Balcón","Cocina"]]
Asesino  = Pistas[0][random.randint(0, len(Pistas[0])-1)]
Arma     = Pistas[1][random.randint(0, len(Pistas[1])-1)]
Motivo   = Pistas[2][random.randint(0, len(Pistas[2])-1)]
Cuerpo   = Pistas[3][random.randint(0, len(Pistas[3])-1)]
Lugar    = Pistas[4][random.randint(0, len(Pistas[4])-1)]
solucion = [Asesino,Arma,Motivo,Cuerpo,Lugar]


Prueba_FB = [["Amigo","Novio","Vecino","Mensajero","Extraño","Hermanastro","Colega"],
        ["Pistola","Cuchillo","Machete","Pala","Bate","Botella","Tubo","Cuerda"],
        ["Venganza","Celos","Dinero","Accidente","Drogas","Robo"],
        ["Cabeza","Pecho","Abdomen","Espalda","Piernas","Brazos"],
        ["Sala","Comedor","Baño","Terraza","Cuarto","Garage","Patio","Balcón","Cocina"]]
Prueba2 = [["Amigo","Novio","Vecino","Mensajero","Extraño","Hermanastro","Colega"],
        ["Pistola","Cuchillo","Machete","Pala","Bate","Botella","Tubo","Cuerda"],
        ["Venganza","Celos","Dinero","Accidente","Drogas","Robo"],
        ["Cabeza","Pecho","Abdomen","Espalda","Piernas","Brazos"],
        ["Sala","Comedor","Baño","Terraza","Cuarto","Garage","Patio","Balcón","Cocina"]]

Parejas =[]
Catidad_Restricciones=0
Encontrado = False
Encontrado2 = False
Contador=0
ContadorX=0
sugerencia_FB=None
sugerencia_BT=None
pista_eliminar_FB=None
Carta_Escogida=None
ventana=Tk()
ventana.resizable(0,0)
ventana.title("Lógica")



def ventana_Inicio():
    global ventana
    ventana.title("Lógica")
    ventana.geometry("500x300")
    blanco=PhotoImage(file="Cartas/Botones/blanca.png")
    Fondo=Label(ventana,image=blanco).place(x=0,y=0)
    contenedor=crearframe()
    contenedor.config(bg="white")
    contenedor.place(x=0,y=0)
    label_3=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label_3.grid(row=0,column=0)
    label_1=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label_1.grid(row=1,column=1)
    label_2=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label_2.grid(row=2,column=2)
    label_4=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label_4.grid(row=3,column=3)
    label_5=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label_5.grid(row=4,column=4)
    label_6=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label_6.grid(row=5,column=5)
    label=Label(contenedor,bg="white",text="abcdef",fg="white",font=("Bradley Hand ITC",20))
    label.grid(row=6,column=6)
    
    label_intentos_fb=Label(contenedor,text="Cantidad de restricciones",bg="white",fg="Black",font=("Bradley Hand ITC",24))
    label_intentos_fb.place(x=90,y=15)
    
    #Restricciones
    restricciones=Entry(contenedor,width=18,bg="white")
    restricciones.place(x=190,y=80)
    restricciones.focus_force()
    #boton de volver

    img_aceptar=PhotoImage(file="Cartas/Botones/Aceptar.png")
    btn_aceptar=Button(contenedor,bd=0,activebackground="white",bg="white",cursor="hand2",image=img_aceptar,\
                      command=lambda:(comienzo_Juego(restricciones.get(),contenedor)))
    btn_aceptar.place(x=220,y=140)
    ventana.mainloop()

def crearframe():
    global ventana
    contenedor=Frame(ventana)
    return contenedor

def comienzo_Juego(restricciones, contenedor):
    global Cantidad_Restricciones, Parejas, Solucion
    if verifica_enteros(restricciones):
        Cantidad_Restricciones=eval(restricciones)
        Parejas=crearRestricciones(Cantidad_Restricciones)
        contenedor.destroy()
        fuerzaBruta()
        backTracking()
        return ventana_Juego()
    else:
        return ventana_Inicio()
    
def verifica_enteros(dato):
    global Catidad_Restricciones
    try:
        numero=eval(dato) #convierte el número a entero
        if isinstance(numero,int) :
            if numero>0:
                Catidad_Restricciones=numero
                return True
            else:
                messagebox.showerror("ERROR","El número de restrcciones debe ser mayor a 0")
        else:
            messagebox.showerror("ERROR","La casilla no puede ser en letras")
            return False
    except:
            messagebox.showerror("ERROR","La casilla esta vacia")
            return False


def ventana_Juego():
    global sugerencia,ventana, sugerencia_BT, solucion, Contador, ContadorX, pista_eliminar_FB, Carta_Escogida
    ventana.title("Juego")
    ventana.geometry("1000x800")
    blanco=PhotoImage(file="Cartas/Botones/blanca.png")
    Fondo=Label(ventana,image=blanco).place(x=0,y=0)

    #-----------------------------imagenes fuerza bruta---------------------------------
    label_FB=Label(ventana,text="FB",bg="white",fg="Black",font=("Bradley Hand ITC",50)).place(x=30,y=50)
    label_intentos_fb=Label(ventana,text="Intentos FB: "+str(Contador),bg="white",fg="Black",font=("Bradley Hand ITC",24)).place(x=750,y=30)
    label_Pista_FB=Label(ventana,text="Carta escogida: \n"+pista_eliminar_FB,bg="white",fg="Black",font=("Bradley Hand ITC",24)).place(x=750,y=70)
    
    imagen1= PhotoImage(file="Cartas/"+sugerencia_FB[0]+".png")
    lbl_imagen1= Label(ventana,image=imagen1).place(x=150,y=30)

    imagen2= PhotoImage(file="Cartas/"+sugerencia_FB[1]+".png")
    lbl_imagen2= Label(ventana,image=imagen2).place(x=260,y=30)
    
    imagen3= PhotoImage(file="Cartas/"+sugerencia_FB[2]+".png")
    lbl_imagen3= Label(ventana,image=imagen3).place(x=370,y=30)
    
    imagen4= PhotoImage(file="Cartas/"+sugerencia_FB[3]+".png")
    lbl_imagen4= Label(ventana,image=imagen4).place(x=480,y=30)
    
    imagen5= PhotoImage(file="Cartas/"+sugerencia_FB[4]+".png")
    lbl_imagen5= Label(ventana,image=imagen5).place(x=590,y=30)

    #-----------------------------imagenes backtracking------------------------------
    label_intentos_BT=Label(ventana,text="BT",bg="white",fg="Black",font=("Bradley Hand ITC",50)).place(x=30,y=600)
    label_intentos_BT=Label(ventana,text="Intentos BT: "+str(ContadorX),bg="white",fg="Black",font=("Bradley Hand ITC",24)).place(x=750,y=580)
    label_Pista_FB=Label(ventana,text="Carta escogida: \n"+Carta_Escogida,bg="white",fg="Black",font=("Bradley Hand ITC",24)).place(x=750,y=610)
    
    imagen6= PhotoImage(file="Cartas/"+sugerencia_BT[0]+".png")
    lbl_imagen6= Label(ventana,image=imagen6).place(x=150,y=550)

    imagen7= PhotoImage(file="Cartas/"+sugerencia_BT[1]+".png")
    lbl_imagen7= Label(ventana,image=imagen7).place(x=260,y=550)
    
    imagen8= PhotoImage(file="Cartas/"+sugerencia_BT[2]+".png")
    lbl_imagen8= Label(ventana,image=imagen8).place(x=370,y=550)
    
    imagen9= PhotoImage(file="Cartas/"+sugerencia_BT[3]+".png")
    lbl_imagen9= Label(ventana,image=imagen9).place(x=480,y=550)
    
    imagen10= PhotoImage(file="Cartas/"+sugerencia_BT[4]+".png")
    lbl_imagen10= Label(ventana,image=imagen10).place(x=590,y=550)

    #-----------------------------imagenes solucion------------------------------
    label_solu=Label(ventana,text="Solución",bg="white",fg="Black",font=("Bradley Hand ITC",35))
    label_solu.place(x=10,y=315)
    imagen11= PhotoImage(file="Cartas/"+solucion[0]+".png")
    lbl_imagen11= Label(ventana,image=imagen11).place(x=200,y=280)

    imagen12= PhotoImage(file="Cartas/"+solucion[1]+".png")
    lbl_imagen12= Label(ventana,image=imagen12).place(x=310,y=280)
    
    imagen13= PhotoImage(file="Cartas/"+solucion[2]+".png")
    lbl_imagen13= Label(ventana,image=imagen13).place(x=420,y=280)
    
    imagen14= PhotoImage(file="Cartas/"+solucion[3]+".png")
    lbl_imagen14= Label(ventana,image=imagen14).place(x=530,y=280)
    
    imagen15= PhotoImage(file="Cartas/"+solucion[4]+".png")
    lbl_imagen15= Label(ventana,image=imagen15).place(x=640,y=280)
##    #----------------------------Listbox de restricciones------------------------------
##    contenedor=crearframe()
##    contenedor.config(bg="white")
##    contenedor.place(x=1080,y=380)
##
##    listNodes = Listbox(contenedor, width=20, height=10, bg="#1F1E1A",fg="white", font=("Helvetica", 12))
##    listNodes.pack(side="left")
##
##    scrollbar = Scrollbar(contenedor, orient="vertical")
##    scrollbar.config(command=listNodes.yview)
##    scrollbar.pack(side="left", fill="y")
##
##    listNodes.config(yscrollcommand=scrollbar.set)
##    x=0
##    while x < len(Restricciones_Cartas):
##        listNodes.insert(END, (str(x+1)+") "+Restricciones_Cartas[x][0]+" - "+Restricciones_Cartas[x][1]))
##        x+=1
##    #-------------------------------imagenes solucion---------------------------
    img_sigue=PhotoImage(file="Cartas/Botones/Siguiente.png")
    btn_sigue=Button(ventana,bd=0,activebackground="white",bg="white",cursor="hand2",image=img_sigue,\
                     command=lambda:(siguiente_Intento()))
    btn_sigue.place(x=850,y=300)
     
    img_reiniciar=PhotoImage(file="Cartas/Botones/Salir.png")
    btn_reiniciar=Button(ventana,bd=0,activebackground="white",bg="white",cursor="hand2",image=img_reiniciar,\
                         command=lambda:(ventana_Inicio()))
    btn_reiniciar.place(x=925,y=300)
    ventana.mainloop()

        
def siguiente_Intento():
    global Encontrado, Encontrado2
    if Encontrado and Encontrado2:
        print("Ambos terminaron")
    elif Encontrado==False and Encontrado2:
        fuerzaBruta()
        return ventana_Juego()
    else:
        backTracking()
        fuerzaBruta()
        return ventana_Juego()

    
def generarSugerenciaBT(lista):
    global Prueba_BT, sugerencia_BT
    validaSugerencia = True
    while validaSugerencia:
        Asesino  = lista[0][random.randint(0, len(lista[0])-1)]
        Arma     = lista[1][random.randint(0, len(lista[1])-1)]
        Motivo   = lista[2][random.randint(0, len(lista[2])-1)]
        Cuerpo   = lista[3][random.randint(0, len(lista[3])-1)]
        Lugar    = lista[4][random.randint(0, len(lista[4])-1)]
        if generarSugerenciaBTAux(Asesino,Arma,Motivo,Cuerpo,Lugar):
            sugerencia_BT = [Asesino,Arma,Motivo,Cuerpo,Lugar]
            validaSugerencia = False
    return sugerencia_BT

def generarSugerenciaBTAux(Asesino,Arma,Motivo,Cuerpo,Lugar):
    global Parejas
    restricciones = Parejas
    i=0
    while i < len(restricciones):
        if (restricciones[i][0]==Asesino and restricciones[i][1]==Arma)   or (restricciones[i][0]==Asesino and restricciones[i][1]==Motivo) or\
           (restricciones[i][0]==Asesino and restricciones[i][1]==Cuerpo) or (restricciones[i][0]==Asesino and restricciones[i][1]==Lugar)  or\
           (restricciones[i][0]==Arma    and restricciones[i][1]==Motivo) or (restricciones[i][0]==Arma    and restricciones[i][1]==Cuerpo) or\
           (restricciones[i][0]==Arma    and restricciones[i][1]==Lugar)  or (restricciones[i][0]==Motivo  and restricciones[i][1]==Cuerpo) or\
           (restricciones[i][0]==Motivo  and restricciones[i][1]==Lugar)  or (restricciones[i][0]==Cuerpo  and restricciones[i][1]==Lugar)  or\
           (restricciones[i][1]==Asesino and restricciones[i][0]==Arma)   or (restricciones[i][1]==Asesino and restricciones[i][0]==Motivo) or\
           (restricciones[i][1]==Asesino and restricciones[i][0]==Cuerpo) or (restricciones[i][1]==Asesino and restricciones[i][0]==Lugar)  or\
           (restricciones[i][1]==Arma    and restricciones[i][0]==Motivo) or (restricciones[i][1]==Arma    and restricciones[i][0]==Cuerpo) or\
           (restricciones[i][1]==Arma    and restricciones[i][0]==Lugar)  or (restricciones[i][1]==Motivo  and restricciones[i][0]==Cuerpo) or\
           (restricciones[i][1]==Motivo  and restricciones[i][0]==Lugar)  or (restricciones[i][1]==Cuerpo  and restricciones[i][0]==Lugar):
            return False
        i+=1
    return True
    

def generarSugerencia(lista):
    global sugerencia_FB
    Asesino  = lista[0][random.randint(0, len(lista[0])-1)]
    Arma     = lista[1][random.randint(0, len(lista[1])-1)]
    Motivo   = lista[2][random.randint(0, len(lista[2])-1)]
    Cuerpo   = lista[3][random.randint(0, len(lista[3])-1)]
    Lugar    = lista[4][random.randint(0, len(lista[4])-1)]
    sugerencia_FB = [Asesino,Arma,Motivo,Cuerpo,Lugar]
    return sugerencia_FB
    
def eliminarPista(dato):
    global Prueba2
    fila = 0
    for i in Prueba2:
        columna = 0
        for j in i:
            if j == dato:
                Prueba2[fila] = Prueba2[fila][:columna]+Prueba2[fila][columna+1:]
            columna+=1
        fila+=1
    return Prueba2

def eliminarPistaFB(dato):
    global Prueba_FB
    fila = 0
    for i in Prueba_FB:
        columna = 0
        for j in i:
            if j == dato:
                Prueba_FB[fila] = Prueba_FB[fila][:columna]+Prueba_FB[fila][columna+1:]
            columna+=1
        fila+=1
    return Prueba_FB

def eliminarCategoria(pista):
    global Prueba2
    i=0
    while i <5:
        j=0
        while j<len(Prueba2[i]):
            if Prueba2[i][j]==pista:
                Prueba2[i]= [pista]
            j+=1
        i+=1
    return Prueba2

def fuerzaBruta():
    global Prueba_FB
    global Encontrado
    global Contador
    global pista_eliminar_FB
    global sugerencia_FB
    global solucion
    sugerencia_FB=generarSugerencia(Prueba_FB)
    print("sugerencia_FB:",sugerencia_FB)
    
    sugerenciaIncorrectas = []
    if solucion != sugerencia_FB:
        Contador+=1
        numero = 0
        while numero <= 4:
            if solucion[numero] != sugerencia_FB[numero]:
                sugerenciaIncorrectas.append(sugerencia_FB[numero])
            numero+=1
        pista_eliminar_FB=random.choice(sugerenciaIncorrectas)
        print("pista_eliminar_FB",pista_eliminar_FB)
        Prueba_FB=eliminarPistaFB(pista_eliminar_FB)
        print("Prueba_FB ",Prueba_FB)
        print("Contador",Contador)
    else:
        Encontrado=True
        print("Finalizo fb")
        print("Contador fb",Contador)

def crearRestriccionesAux():
    global Pistas
    cartasPareja = random.choice(Pistas)
    pareja1 = random.choice(cartasPareja)
    cartasPareja = random.choice(Pistas)
    pareja2 = random.choice(cartasPareja)
    while pareja1 == pareja2:
        pareja2 = random.choice(cartasPareja)
    Pareja = [pareja1, pareja2]
    return Pareja

def crearRestricciones(datoParejas):
    global Parejas, solucion
    while datoParejas != 0:
        Pareja = crearRestriccionesAux()
        while all(item in solucion for item in Pareja) == True:
            Pareja = crearRestriccionesAux()
        Parejas.append(Pareja)
        datoParejas = datoParejas - 1
    return Parejas
 

def backTracking():
    global ContadorX
    global Prueba2
    global Encontrado2
    global solucion
    global sugerencia_BT
    global Carta_Escogida
    Carta_Escogida
    if Encontrado2:
        print("Finalizo")
        print("ContadorBT",ContadorX)
    else:
        sugerencia_BT=generarSugerenciaBT(Prueba2)
        #print("sugerencia_BT:",sugerencia_BT)
        #print("ContadorBT",ContadorX)
        if solucion!=sugerencia_BT:
            ContadorX=ContadorX+1
            Pos = elegirCarta()
            Carta_Escogida = sugerencia_BT[Pos]
            if esta_en_solucion(Carta_Escogida):
                Prueba2=eliminarCategoria(Carta_Escogida)
            else:
                Prueba2=eliminarPista(Carta_Escogida)
        else:
            Encontrado2=True

def esta_en_solucion(pista):
    global solucion
    x=0
    while x<5:
        if pista==solucion[x]:
            return True
        x+=1
    return False

def elegirCarta():
    global Prueba2
    validar = False
    while validar==False:
        opcion=random.randint(0, 4)
        if len(Prueba2[opcion])!=1:  
            return opcion           

ventana_Inicio()

   
                
        
    
