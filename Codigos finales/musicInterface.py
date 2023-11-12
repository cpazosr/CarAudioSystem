#!/usr/bin/env python3

#Manuel Agustin Diaz Vivanco
#Carlos Antonio Pazos Reyes
#Diseno de sistemas en chip

#librerias
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import pygame as pg
import os, random, serial, time, subprocess, threading, queue, csv
import usbdev

#clase para multi hilo grafico de la interfaz
class GUI:
    
    #constructor
    def __init__(self, master, queue, prevFunc, playPauseFunc, nextFunc, randFunc, usbFunc, muteFunc):
        
        #cola de comunicacion asincrona
        self._queue = queue
        
        #variables display
        self._valueTitle = tk.StringVar()
        self._valueArtist = tk.StringVar()
        self._valueDate = tk.StringVar()
        self._valueHour = tk.StringVar()
        self._valueHum = tk.StringVar()
        self._valueTemp = tk.StringVar()
        self._valueHeatIdx = tk.StringVar()
        self._random = tk.IntVar(value=0)
        self._volume = tk.StringVar(value="50")
        self._tiempo = tk.StringVar(value="00:00")
        
        #variable support
        self._pausa = True
        self._contador = 0
        self._val_prev = 0
        
        #variables de datos
        self._info = {"Archivo":' ', "Titulo":' ', "Formato":' ', "Artista":' ', "Album":' ', "Fecha":' ', "Duracion":' ', "BitRate":' ', "SampleRate":' ', "Canales":' ', "Rating":' ', "Milis":' '}
        self._dia = {"Fecha":' ', "Hora":' '}
        self._clima = {"Hum":' ', "Temp":' ', "HeatIdx":' '}
        
        #crear widgets
        #labels: datos de cancion
        titleLabel = tk.Label(master, textvariable=self._valueTitle, justify="center", font=(("Verdana"),10, "bold"))
        artistLabel = tk.Label(master, textvariable=self._valueArtist, justify="center", font=(("Verdana"), 10, "bold"))
        #labels: datos del exterior
        dateLabel = tk.Label(master, text="Fecha:", justify="center", font=(("Verdana"),12))
        dateValueLabel = tk.Label(master, textvariable=self._valueDate, justify="center", font=(("Verdana"),12))
        hourLabel = tk.Label(master, text="Hora:", justify="center", font=(("Verdana"),12))
        hourValueLabel = tk.Label(master, textvariable=self._valueHour, justify="center", font=(("Verdana"),12))
        humLabel = tk.Label(master, text="Humedad:", justify="center", font=(("Verdana"),12))
        humValueLabel = tk.Label(master, textvariable=self._valueHum, justify="center", font=(("Verdana"),12))
        tempLabel = tk.Label(master, text="Temperatura:", justify="center", font=(("Verdana"),12))
        tempValueLabel = tk.Label(master, textvariable=self._valueTemp, justify="center", font=(("Verdana"),12))
        heatIdxLabel = tk.Label(master, text="Heat Index:", justify="center", font=(("Verdana"),12))
        heatIdxValueLabel = tk.Label(master, textvariable=self._valueHeatIdx, justify="center", font=(("Verdana"),12))
        #labels: volumen
        volumeValueLabel = tk.Label(master, textvariable=self._volume, justify="center", font=(("Verdana"),12))
        #labels: tiempo
        TiempoValueLabel = tk.Label(master, textvariable=self._tiempo, justify="center", font=(("Verdana"),12))
        
        #imagenes de los botones
        self._prevBtnImage = tk.PhotoImage(file="images/prevBtn_50x50alpha.png")
        self._pauseBtnImage = tk.PhotoImage(file="images/pauseBtn_50x50alpha.png")
        self._playBtnImage = tk.PhotoImage(file="images/playBtn_50x50alpha.png")
        self._nextBtnImage = tk.PhotoImage(file="images/nextBTn_50x50alpha.png")
        self._usbBtnImage = tk.PhotoImage(file="images/25-USB-512_30x30.png")
        self._randomBtnImage = tk.PhotoImage(file="images/random_30x30alpha.png")
        self._volImage = tk.PhotoImage(file="images/volume_35x35.png")
        self._muteImage = tk.PhotoImage(file="images/mute_35x35.png")
        self._songInfoImage = tk.PhotoImage(file="images/songinfo_30x30alpha.png")
        
        #controles menu
        controls = tk.Frame()
        controls.place(relx = 0.1, rely=0.8)
        
        #volumen frame
        volFrame = tk.Frame()
        volFrame.place(relx=0.7, rely=0.83)
        self._volumeBtnLabel = tk.Button(volFrame, image=self._volImage, bd=0, command=muteFunc)
        volumeValueLabel = tk.Label(volFrame, textvariable=self._volume, justify="center", font=(("Verdana"),12))
        
        #checkbutton
        randomCheckbox = tk.Checkbutton(master, image=self._randomBtnImage, borderwidth=0, text="Random", compound="top", variable=self._random, onvalue=1, offvalue=0, command=randFunc)
        
        #botones
        btnPrev = tk.Button(controls, image=self._prevBtnImage, bd=0, command=prevFunc)
        self._btnPlayPause = tk.Button(controls, image=self._playBtnImage, bd=0, command=playPauseFunc)
        btnNext = tk.Button(controls, image=self._nextBtnImage, bd=0, command=nextFunc)
        btnRatings = tk.Button(master, justify="center", bd=0, text="Ratings", command=self.showRatings, width=5, height=1)
        btnInfo = tk.Button(master, image=self._songInfoImage, bd=0, text="Info", compound="top", command=self.showInfo)
        btnUSB = tk.Button(master, image=self._usbBtnImage, bd=0, text="USB", compound="left", command=usbFunc)

        #mostrar items
        titleLabel.place(relx=0.01, rely=0.35)
        artistLabel.place(relx=0.01, rely=0.45)
        
        dateLabel.place(relx=0.01, rely=0.01)
        dateValueLabel.place(relx=0.15, rely=0.01)
        hourLabel.place(relx=0.01, rely=0.08)
        hourValueLabel.place(relx=0.15, rely=0.08)
        
        humLabel.place(relx=0.66, rely=0.01)
        humValueLabel.place(relx=0.9, rely=0.01)
        tempLabel.place(relx=0.66, rely=0.08)
        tempValueLabel.place(relx=0.9, rely=0.08)
        heatIdxLabel.place(relx=0.66, rely=0.15)
        heatIdxValueLabel.place(relx=0.9, rely=0.15)
        
        TiempoValueLabel.place(relx=0.37, rely=0.6)
        
        btnPrev.grid(row=0, column=0, padx=10)
        self._btnPlayPause.grid(row=0, column=1, padx=10)
        btnNext.grid(row=0, column=2, padx=10)
        
        self._volumeBtnLabel.grid(row=0, column=0, padx=10)
        volumeValueLabel.grid(row=0, column=1, padx=10)
        
        btnRatings.place(relx=0.42, rely=0.15)
        btnInfo.place(relx=0.85, rely=0.3)
        btnUSB.place(relx=0.4, rely=0.01)
        
        randomCheckbox.place(relx=0.75, rely=0.53)
        
        self._song_slider = ttk.Scale(master, from_ = 0, to = 100, orient = tk.HORIZONTAL,length = 360, value = 0, state="disabled")
        self._song_slider.place(relx=0.05, rely=0.7)

    #process I/O
    def processInputOutput(self):
        while self._queue.qsize():
            try:
                msg = self._queue.get(0)
                delimiter = msg.find(':')
                if delimiter != -1:
                    key = msg[0:delimiter]
                    value = msg[delimiter+1:]
                    if key == "Info":
                        values = value.split("^#^")
                        self._info["Archivo"] = values[0]
                        self._info["Titulo"] = values[1]
                        self._info["Formato"] = values[2]
                        self._info["Artista"] = values[3]
                        self._info["Album"] = values[4]
                        self._info["Fecha"] = values[5]
                        self._info["Duracion"] = values[6]
                        self._info["BitRate"] = values[7]
                        self._info["SampleRate"] = values[8]
                        self._info["Canales"] = values[9]
                        self._info["Rating"] = values[10]
                        self._info["Milis"] = values[11]
                        
                        self._valueTitle.set(self._info["Titulo"])
                        self._valueArtist.set(self._info["Artista"])
                    elif key == "UTC":
                        values = value.split("^#^")
                        values = value.split(",")
                        self._dia["Fecha"] = values[0]
                        times = values[1].split(":")
                        if len(times[1]) == 1:
                            times[1] = "0"+times[1]
                        self._dia["Hora"] = times[0]+":"+times[1]
                        
                        self._valueDate.set(self._dia["Fecha"])
                        self._valueHour.set(self._dia["Hora"])
                    elif key == "DHT":
                        values = value.split(",")
                        self._clima["Hum"] = values[0]
                        self._clima["Temp"] = values[1]
                        self._clima["HeatIdx"] = values[2]
                        
                        self._valueHum.set(self._clima["Hum"])
                        self._valueTemp.set(self._clima["Temp"])
                        self._valueHeatIdx.set(self._clima["HeatIdx"])
                    elif key == "Error":
                        tk.messagebox.showerror("No hay archivos", message="No hay canciones")
                    elif key == "IR":
                        if value == "100+":
                            if self._random.get() == 1:
                                self._random.set(0)
                            else:
                                self._random.set(1)
                        elif value == "EQ":
                            self.showRatings()
                        elif value == "Mode":
                            self.showInfo()
                        elif value == "USBerror":
                            tk.messagebox.showerror("USB Faltante", message="No USB detectada")
                        elif value == "USBcorrect":
                            tk.messagebox.showinfo("USB Exitosa", message="Nuevas canciones agregadas")
                    elif key == "BTN":
                        if value == "PAUSE":
                            self._pausa = True
                            self._btnPlayPause.config(image=self._playBtnImage)
                        elif value == "PLAY":
                            self._pausa = False
                            self._btnPlayPause.config(image=self._pauseBtnImage)
                    elif key == "VOL":
                        self._volume.set(value)
                        if int(self._volume.get()) == 0:
                            self._volumeBtnLabel.config(image=self._muteImage)
                        else:
                            self._volumeBtnLabel.config(image=self._volImage)
                    elif key == "Pos":
                        current_time = time.strftime('%M:%S',time.gmtime(int(value)))
                        self._tiempo.set(current_time)
                        self._song_slider.config(to = int(self._info["Milis"]))
                        if self._pausa == False:
                            self._contador += 1
                            if self._contador == 10:
                                next_time = int(self._song_slider.get())+ 1
                                self._song_slider.config(value = next_time)
                                self._contador = 0
                        if self._val_prev > int(value):
                            self._song_slider.config(value = 0)
                        self._val_prev = int(value)
            except queue.Empty:
                print("Empty Queue")
    
    #display de las puntuaciones
    def showRatings(self):
        createPopUp = threading.Thread(target=self.ratingsWindow, daemon=True)
        createPopUp.start()
        createPopUp.join(0.1)
        
    #pop up puntuaciones
    def ratingsWindow(self):
        popup = tk.Tk()
        popup.title("Puntuaciones")
        
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth*2.3)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight*1.8)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        
        with open("Rating.csv") as f:
            # reading file
            Rating = str(f.read())
        # Display whole message
        display = scrolledtext.ScrolledText(popup, width=30, height=7, font=("Times New Roman",15))
        display.pack(padx=10, pady=10)
        display.insert(tk.INSERT, Rating)
        display.configure(state="disabled")
        popup.mainloop()
            
    #informacion de la cancion
    def showInfo(self):
        createPopUp = threading.Thread(target=self.infoWindow, daemon=True)
        createPopUp.start()
        createPopUp.join(0.1)
        
    #pop up informacion
    def infoWindow(self):
        popup = tk.Tk()
        popup.title("Informacion")
        
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth*2.3)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight*1.8)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        
        k = list(self._info.keys())
        v = list(self._info.values())
        info = k[0]+":\n"+v[0]+"\n"+k[1]+":\n"+v[1]+"\n"+k[2]+":\n"+v[2]+"\n"+k[3]+":\n"+v[3]+"\n"+k[4]+":\n"+v[4]+"\n"+k[5]+":\n"+v[5]+"\n"+k[6]+":\n"+v[6]+"\n"+k[7]+":\n"+v[7]+"\n"+k[8]+":\n"+v[8]+"\n"+k[9]+":\n"+v[9]+"\n"+k[10]+":\n"+v[10]+"\n"
        display = scrolledtext.ScrolledText(popup, width=30, height=7, font=("Times New Roman",15), background="white")
        display.pack(padx=10, pady=10)
        display.insert(tk.INSERT, info)
        display.configure(state="disabled")
        popup.mainloop()

class MusicInterface(tk.Frame):
    
    #constructor
    def __init__(self, path, master=None):
        
        #playlist path
        self._playlist_path = path
        
        #propiedades de la interfaz
        super().__init__(master)
        self._master = master  
        self._master.protocol('WM_DELETE_WINDOW',self.Quit)
        self.pack()
        
        #comunicacion con arduino
        self._sensing = threading.Thread(target=self.sensors, daemon=True)
        self._arduino = serial.Serial('/dev/ttyACM0',9600,timeout=1)
        time.sleep(1)
        self._sensorsReading = True
        
        #crear playlist
        self._playlist = [file for file in os.listdir(self._playlist_path) if os.path.isfile(os.path.join(self._playlist_path, file))]  #excluye directorios
        self._playlist.sort(key = lambda file: os.path.getmtime(os.path.join(self._playlist_path, file)))  #ordena por ultima modificacion (fecha agregada a SD)
        
        #cola a mandar a GUI
        self._queue = queue.Queue()
        self._gui = GUI(self._master, self._queue, self.prev, self.playPause, self.next, self.randomSelect, self.copyUSBfiles, self.mute)
        
        #guardar copia de playlist ordenada
        self._playlist_orden = self._playlist
        
        #longitud de playlist
        self._playlist_length = len(self._playlist)
        
        #playlist vacia
        if self._playlist_length == 0:
            self._queue.put("Error:Empty")
            self._sensorsReading = False
            self._arduino.close()
            self._sensing.join(0.1)
            self._master.quit()
            self._master.destroy()
            print("No songs in directory")
        
        #ordenamiento de reproduccion
        self._randomCheck = False
        
        #finalizar asincrono
        self._terminate = False
        
        #path csv
        self._csvPath = "/home/pi/Documents/Reto/Rating.csv"
        
        #inicializamos un csv con valores default de 0
        self.Datos_Rating()
        
        #cancion apuntada
        self._current = 0
        
        #inicializar mixer
        pg.init()
        pg.mixer.init()
        
        #tipo de evento al terminar la cancion
        self._SONG_END = pg.USEREVENT + 1
        
        #cargar current y pausar y enviar evento de fin de cancion
        pg.mixer.music.load(self._playlist_path + self._playlist[self._current])
        pg.mixer.music.play()
        pg.mixer.music.pause()
        pg.mixer.music.set_endevent(self._SONG_END)
        
        #estado de reproduccion
        self._playing = False
        
        #estado de volumen
        self._unmuted = True
        
        #senales de hardware por recibir y procesar
        self._hardware = {"Button": None, "IR": None, "Volumen":50, "UTC":None, "DHT":None}
        
        #volumen medio
        self._volume = 50
        pg.mixer.music.set_volume(self._volume/100)
        self._queue.put("VOL:"+str(self._volume))
        
        #info de la primera cancion
        self.info(self._playlist, self._current)
        
        #usb listener y path support
        self._observer = usbdev.startListener()
        self._devpath = None
        
        #empezar a sensar asincrono
        self._sensing.start()
        
        #empezar a ver en la cola
        self.checkQueue()
    
    #llamado periodico a la cola para checar contenidos
    def checkQueue(self):
        #llamar a procesar los datos en cola
        self._gui.processInputOutput()
        
        #tiempo actual de la cancion
        current_time = int(pg.mixer.music.get_pos()/1000)
        self._queue.put("Pos:"+str(current_time))
        
        #manejo de fin de cancion
        for event in pg.event.get():
            if event.type == self._SONG_END:
                self.next()
        
        #cierre de programa asincrono
        if self._terminate:
            self.Quit()
        
        if self._sensorsReading:
            #cada 100ms
            self._master.after(100, self.checkQueue)
    
    def Datos_Rating(self):
        #abrimos un csv con los titulos de las columnas 
        with open('Rating.csv','a',newline='') as Rating:
             R = csv.reader(open(self._csvPath))
             #sacamos los valores que ya estan en el csv guradados
             self.Rating_list = list(R)
             #si la lista está vacia, la inicializamos
             if len(self.Rating_list) == 0:
                 for i in range (self._playlist_length):
                     self.Rating_list.insert(i,[self._playlist[i],0])
             #checamos si en la direccion de memoria hay mas archivos que los guardados en la lista
             if self._playlist_length > (len(self.Rating_list)):      
                 for i in range(self._playlist_length - (len(self.Rating_list))):
                    self.agregar()
             #checamos si en la direccion de memoria hay menos archivos que los guardados en la lista      
             if self._playlist_length < (len(self.Rating_list)):
                 for i in range((len(self.Rating_list))  - self._playlist_length):
                    self.eliminar()
        #corregimos los nimeros de la primera variable del csv 
        writer = csv.writer(open(self._csvPath, 'w'))
        writer.writerows(self.Rating_list)
    
    #agregar cancion a csv
    def agregar(self):
         #Ya checamos y hay mas archivos en la direccion que en la lista 
         for i in range(self._playlist_length):
            #insertamos el valor que no coincide
            if i >= len(self.Rating_list):
                self.Rating_list.insert(i,[self._playlist[i],0])
                break
            elif (self._playlist[i] != self.Rating_list[i][0]) :
                #insertamos el valor que no coincide
                self.Rating_list.insert(i,[self._playlist[i],0])
                #hacemos un break para que se agregue y se escriba, para evitar errores (se agregan uno por uno los archivos faltantes)
                break
    
    #eliminar canciones del csv que no esten en el path
    def eliminar(self):
            #Ya checamos y hay mas archivos en la direccion que en la lista 
             for i in range(len(self.Rating_list)):
                #insertamos el valor que no coincide
                if i >= self._playlist_length:
                    del self.Rating_list[i]
                    break
                elif (self._playlist[i] != self.Rating_list[i][0]) :
                    #insertamos el valor que no coincide
                    del self.Rating_list[i]
                    #hacemos un break para que se agregue y se escriba, para evitar errores (se agregan uno por uno los archivos faltantes)
                    break
    
    #funcion de Rating
    def Rating(self,value):
        for i in range(len(self.Rating_list)):
            if self._playlist[self._current] == self.Rating_list[i][0]:
                self.Rating_list[i][1] = value
                writer = csv.writer(open(self._csvPath, 'w'))
                writer.writerows(self.Rating_list)
    
    #funcion hilo sensado activo desde arduino
    def sensors(self):
        while self._sensorsReading:
            line = self._arduino.readline().decode('utf-8').rstrip()
            if line != '':
                delimiter = line.find(':')
                if delimiter != -1:
                    key = line[0:delimiter]
                    value = line[delimiter+1:]
                    if key in self._hardware.keys():
                        self._hardware[key] = value
                        if key == "Button":
                            if value != None and value == "prev":
                                self.prev()
                            elif value != None and value == "play":
                                self.playPause()
                            elif value != None and value == "next":
                                self.next()
                        elif key == "IR":
                            if value != None and value == "OFF":
                                self._terminate = True
                            elif value != None and value == "Mode":
                                self._queue.put(line)
                            elif value != None and value == "Mute":
                                self.mute()
                            elif value != None and value == ">=":
                                self.playPause()
                            elif value != None and value == "|<<":
                                self.prev()
                            elif value != None and value == ">>|":
                                self.next()
                            elif value != None and value == "EQ":
                                self._queue.put(line)
                            elif value != None and value == "-":
                                self._volume -= 1
                                if self._volume < 0:
                                    self._volume = 0
                                pg.mixer.music.set_volume(self._volume/100)
                                self._queue.put("VOL:"+str(self._volume))
                            elif value != None and value == "+":
                                self._volume += 1
                                if self._volume > 100:
                                    self._volume = 100
                                pg.mixer.music.set_volume(self._volume/100)
                                self._queue.put("VOL:"+str(self._volume))
                            elif value != None and value == "100+":
                                self._queue.put(line)
                                self.randomSelect()
                            elif value != None and value == "200+":
                                self.copyUSBfiles()
                            elif value != None:
                                self.Rating(value)
                                self.info(self._playlist, self._current)
                        elif key == "Volumen":
                            if value != None:
                                self._volume += int(value)
                                if self._volume > 100:
                                    self._volume = 100
                                elif self._volume < 0:
                                    self._volume = 0
                                pg.mixer.music.set_volume(self._volume/100)
                                self._queue.put("VOL:"+str(self._volume))
                        elif key == "UTC":
                            if value != None:
                                self._queue.put(line)
                        elif key == "DHT":
                            if value != None:
                                self._queue.put(line)
    
    #mute de volumen
    def mute(self):
        if self._unmuted:
            self._unmuted = False
            pg.mixer.music.set_volume(0)
            self._queue.put("VOL:0")
        else:
            self._unmuted = True
            pg.mixer.music.set_volume(self._volume/100)
            self._queue.put("VOL:"+str(self._volume))
    
    #archivos de la USB
    def copyUSBfiles(self):
        status = usbdev.isDeviceConnected()
        if status:
            device = usbdev.getDevData()
            if device != None:
                self._devpath = device["DEVPATH"]
            path = usbdev.getMountPathUsbDevice()
            if path != None:
                os.system("cp " + path + "/*.mp3 " + self._playlist_path)
                os.system("cp " + path + "/*.wav " + self._playlist_path)
                #recrear playlist
                self._playlist = [file for file in os.listdir(self._playlist_path) if os.path.isfile(os.path.join(self._playlist_path, file))]  #excluye directorios
                self._playlist.sort(key = lambda file: os.path.getmtime(os.path.join(self._playlist_path, file)))  #ordena por ultima modificacion (fecha agregada a SD)
                #reset guardar copia de playlist ordenada
                self._playlist_orden = self._playlist
                #reset longitud de playlist
                self._playlist_length = len(self._playlist)
                #reset current
                self._current = 0
                self._queue.put("IR:USBcorrect")
                self.Datos_Rating()
        else:
            self._queue.put("IR:USBerror")
    
    #funcion de boton prev
    def prev(self):
        if pg.mixer.music.get_pos() > 10000:
            pg.mixer.music.load(self._playlist_path + self._playlist[self._current])
            pg.mixer.music.set_volume(self._volume/100)
            pg.mixer.music.play()
        else:
            if self._current == 0:
                self.info(self._playlist, self._playlist_length - 1)
                pg.mixer.music.load(self._playlist_path + self._playlist[self._playlist_length - 1])
                pg.mixer.music.set_volume(self._volume/100)
                pg.mixer.music.play()
                self._current = self._playlist_length - 1
            else:
                self.info(self._playlist, self._current - 1)
                pg.mixer.music.load(self._playlist_path + self._playlist[self._current - 1])
                pg.mixer.music.set_volume(self._volume/100)
                pg.mixer.music.play()
                self._current -= 1
        self._queue.put("BTN:PLAY")
        self._playing = True
        time.sleep(0.5)

    #funcion de boton pausa
    def playPause(self):
        if self._playing:
            pg.mixer.music.pause()
            self._queue.put("BTN:PAUSE")
            self._playing = False
        else:
            pg.mixer.music.unpause()
            self._queue.put("BTN:PLAY")
            self._playing = True
        time.sleep(0.5)
    
    #funcion de boton next
    def next(self):
        if self._current == self._playlist_length - 1:
            self.info(self._playlist, 0)
            pg.mixer.music.load(self._playlist_path + self._playlist[0])
            pg.mixer.music.set_volume(self._volume/100)
            pg.mixer.music.play()
            self._current = 0
        else:
            self.info(self._playlist, self._current + 1)
            pg.mixer.music.load(self._playlist_path + self._playlist[self._current + 1])
            pg.mixer.music.set_volume(self._volume/100)
            pg.mixer.music.play()
            self._current += 1
        self._queue.put("BTN:PLAY")
        self._playing = True
        time.sleep(0.5)
    
    #info de la cancion 
    def info(self,playlist,numero):     
        nombre_archivo = playlist[numero]
        nombre_cancion = subprocess.check_output ("mediainfo --Inform="+'"General;%Title%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        formato = subprocess.check_output("mediainfo --Inform="+'"General;%Format%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        if "Wave" in formato:
            artista = subprocess.check_output ("mediainfo --Inform="+'"General;%Director%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
            album = subprocess.check_output ("mediainfo --Inform="+'"General;%OriginalSourceForm/Name%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        elif "MPEG Audio" in formato:
            artista = subprocess.check_output ("mediainfo --Inform="+'"General;%Performer%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
            album = subprocess.check_output ("mediainfo --Inform="+'"General;%Album%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        fecha = subprocess.check_output("mediainfo --Inform="+'"General;%Recorded_Date%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        duracion = subprocess.check_output("mediainfo --Inform="+'"General;%Duration/String3%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        duracion_milis = subprocess.check_output("mediainfo --Inform="+'"General;%Duration%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        bit_rate = subprocess.check_output("mediainfo --Inform="+'"General;%BitRate%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        sample_rate = subprocess.check_output("mediainfo --Inform="+'"Audio;%SamplingRate%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        canales = subprocess.check_output("mediainfo --Inform="+'"Audio;%Channel(s)%" '+self._playlist_path+playlist[numero],shell=True,universal_newlines=True)
        
        #procesamiento pre envio
        duracion_milis = int(duracion_milis)/1000
        duracion_milis = int(duracion_milis)
        if " " in fecha[0:4]:
            pos = fecha.find(" ")
            fecha = fecha[pos+1:pos+5]
        else:
            fecha = fecha[0:4]
        for i in range(len(self.Rating_list)):
            if self._playlist[numero] == self.Rating_list[i][0]:
                rating = str(self.Rating_list[i][1])
        
        information = "Info:"+nombre_archivo+"^#^"+nombre_cancion+"^#^"+formato+"^#^"+artista+"^#^"+album+"^#^"+fecha+"^#^"+duracion+"^#^"+bit_rate+"^#^"+sample_rate+"^#^"+canales+"^#^"+rating+"^#^"+str(duracion_milis)
        
        #enviar a cola para procesar I/O
        self._queue.put(information)
    
    #modificar variables de random
    def randomSelect(self):
        if self._randomCheck == False:
            new_playlist = random.sample(self._playlist, len(self._playlist))
            self._playlist = new_playlist
            self._randomCheck = True
        else:
            self._playlist = self._playlist_orden
            self._randomCheck = False
    
    #funcion al cerrar la ventana de la interfaz
    def Quit(self):
        self._sensorsReading = False
        pg.mixer.music.stop()
        pg.mixer.quit()
        pg.quit()
        time.sleep(1)
        usbdev.stopListener(self._observer)
        if self._devpath != None:
            os.system("sudo umount " + self._devpath)
        self._arduino.close()
        self._sensing.join(0.1)
        self._master.quit()
        self._master.destroy()
        print("closed")