from email.policy import default
from urllib.request import DataHandler
import pandas as pd
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from tkinter.messagebox import showinfo
from tkinter import *

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

def popup_showinfo(qualidade):
    showinfo("Qualidade", str(qualidade))

pesosDefault = {
  'acidez fixa': 2,
  'acidez volátil': 3,
  'ácido cítrico': 1,
  'açúcar residual': 4,
  'cloretos': 2,
  'dióxido de enxofre livre': 2,
  'dióxido de enxofre total': 2,
  'densidade': 4,
  'pH': 5,
  'sulfatos': 3,
  'álcool': 5,
}

# Similaridades
# Local: (x -​ abs(​x -​ y)) / ​x
# Global: ⅀ var * peso / ⅀ pesos 

# ⅀ pesos 
sumPesos = 0
for key in pesosDefault.keys():
  sumPesos += pesosDefault[key]


def RBC(ents, data, text):
  similaridadeGlobal = []
  novoCaso = ents[0]
  pesos = ents[1]

  for key in pesosDefault.keys():
    peso = float(pesos[key].get())
    if peso != pesosDefault[key]:
      pesosDefault[key] = peso

  for x in range(len(data.values)):
    similaridadeLocal = {}
    
    for column in pesosDefault.keys():
      value = data[column].values[x] 
      if (value == 0):
        similaridadeLocal[column] = 0
      else:
        similaridadeLocal[column] = (value - abs(value - float(novoCaso[column].get()))) / value

    # ⅀ var * peso
    sumVars = []
    for column in pesosDefault.keys():
      sumVars.append(similaridadeLocal[column] * pesosDefault[key])

    similaridadeGlobal.append(sum(sumVars) / sumPesos)

  data['similaridade global'] = similaridadeGlobal
  data = data.sort_values(by=['similaridade global'], ignore_index=True, ascending=False)
  for column in data.columns:
    data[column] = data[column].round(decimals = 3)

  text.delete('1.0', tk.END)
  text.insert(tk.END, data.to_string(index=False))
  text.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, pady=10)

  popup_showinfo(data['qualidade'].values[0])


def makeform(root, data):
    atributos = {}
    pesos = {}

    for field in list(filter(lambda column: column != 'qualidade', data.columns)):
        minValue = min(data[field].values)
        maxValue = max(data[field].values)
        
        row = tk.Frame(root)
        lab = tk.Label(row, width=40, text=field+": min = {} - max = {}".format(minValue, maxValue), anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, str(minValue))
        row.pack(side=tk.TOP, fill=tk.X, padx=7, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.LEFT, expand=tk.NO, fill=tk.X)
        atributos[field] = ent

        lab = tk.Label(row, width=40, text='Peso ' + field, anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, str(pesosDefault[field]))
        row.pack(side=tk.TOP, fill=tk.X, padx=7, pady=5)
        ent.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.X)
        lab.pack(side=tk.RIGHT)
        pesos[field] = ent
    return atributos, pesos

if __name__ == '__main__':
    data = pd.DataFrame(pd.read_csv(r'winequality-red.csv', delimiter=';'))
    data.columns = ['acidez fixa', 'acidez volátil', 'ácido cítrico', 'açúcar residual',
      'cloretos', 'dióxido de enxofre livre', 'dióxido de enxofre total',
      'densidade', 'pH', 'sulfatos', 'álcool', 'qualidade'     
    ]

    root = tk.Tk()
    app=FullScreenApp(root)
    ents = makeform(root, data)
    
    b1 = tk.Button(root, text='Calcular', command=(lambda e=ents: RBC(e, data, TKScrollTXT)))
    b1.pack(side=tk.TOP, fill=tk.X)

    TKScrollTXT = tkscrolled.ScrolledText(wrap='word')
    TKScrollTXT.pack(side=tk.BOTTOM)
  
    root.mainloop()