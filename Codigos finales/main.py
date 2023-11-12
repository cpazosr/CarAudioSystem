#!/usr/bin/env python3

#Manuel Agustin Diaz Vivanco
#Carlos Antonio Pazos Reyes
#Diseno de sistemas en chip

from musicInterface import MusicInterface
import tkinter as tk

def main():
    root = tk.Tk()
    playlist_path = "/home/pi/Music/"
    root.title("Music Player")
    #root.minsize(1000,750)
    root.minsize(480,320)
    #root.attributes('-zoomed', True)
    #root.resizable(False, False)
    
    #display App al centro de la pantalla
    #ancho y alto del mainframe de App
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    #centro de ancho y alto de ambas pantalla y App
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth*1.2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight*0.8)
    #centrar el App
    root.geometry("+{}+{}".format(positionRight, positionDown))
    
    app = MusicInterface(playlist_path, root)
    app.mainloop
    
if __name__ == "__main__":
    main()