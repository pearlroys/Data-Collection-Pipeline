from tk import *
import tkinter as tk
from PIL import Image, ImageTk
from medexpress import Scraper


window = tk.Tk()
window.configure(background="black")
window.geometry("525x700")
window.title("MEDEXPRESS GUI")
for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)


#Labels
l1 = tk.Label(window, text="ENTER DRUG NUMBER: ", width=25, bg="gray25", fg="ghost white", font=("Times", 14))
l2 = tk.Label(window, text="DOSE", width=25, bg="gray25", fg="ghost white", font=("Times", 14))
l3 = tk.Label(window, text="PRICE", width=25, bg="gray25", fg="ghost white", font=("Times", 14))
l4 = tk.Label(window, text="QUANTITY", width=25, bg="gray25", fg="ghost white", font=("Times", 14))
l5 = tk.Label(window, text="REVIEWS", width=25, bg="gray25", fg="ghost white", font=("Times", 14))
l6 = tk.Label(window, text="ALTERNATIVES", width=25, bg="gray25", fg="ghost white", font=("Times", 14))
l7 = tk.Label(window, text="UUID", width=25, bg="gray25", fg="ghost white", font=("Times", 14))

l1.grid(row=1, column=0, pady=15)
l2.grid(row=2, column=0, pady=5)
l3.grid(row=3, column=0, pady=5)
l4.grid(row=4, column=0, pady=5)
l5.grid(row=5, column=0, pady=5)
l6.grid(row=6, column=0, pady=5)
l7.grid(row=7, column=0, pady=5)


#Image
imagePath = "/Users/pearl/Desktop/images.png"
i = Image.open(imagePath)
medexpress_image = ImageTk.PhotoImage(i)
i1 = tk.Label(window, image=medexpress_image)
i1.grid(row=0, column=0, padx=10, pady=10)

#Text-Entries
e1 = tk.Entry(window)
e2 = tk.Text(window, width=25, height=1)
e3 = tk.Text(window, width=25, height=1)
e4 = tk.Text(window, width=25, height=1)
e5 = tk.Text(window, width=25, height=1)
e6 = tk.Text(window, width=25, height=1)
e7 = tk.Text(window, width=25, height=1)

e1.grid(row=1, column=1, pady=5)
e2.grid(row=2, column=1, pady=5)
e3.grid(row=3, column=1, pady=5)
e4.grid(row=4, column=1, pady=5)
e5.grid(row=5, column=1, pady=5)
e6.grid(row=6, column=1, pady=5)
e7.grid(row=7, column=1, pady=5)

# def insert_data():
#     try:
#         temp = e1.get()
#         data = int(temp)
#         e2.insert(tk.END, drug_dictionary.name[data])
#         e3.insert(tk.END, drug_dictionary.dose[data])
#         e4.insert(tk.END, drug_dictionary.price[data])
#         e5.insert(tk.END, drug_dictionary.quantity[data])
#         e6.insert(tk.END, drug_dictionary.alternatives[data])
#         e7.insert(tk.END, drug_dictionary.uuid[data])
#     except IndexError:
#         print("Number should be between: 0-925")
#     except ValueError:
#         print("Input should be a number")

def class_data():
    bot = Scraper()
    
    bot.get_metadata()
    bot.class_choice = e1.get()

    e2.insert(tk.END, bot.dict_self)
   

    
        
def clear():
    e2.delete('1.0', tk.END)
    e3.delete('1.0', tk.END)
    e4.delete('1.0', tk.END)
    e5.delete('1.0', tk.END)
    e6.delete('1.0', tk.END)
    e7.delete('1.0', tk.END)

#Buttons
b1 = tk.Button(window, text="INFORMATION ON DRUG", command=class_data, bg="forest green", fg="gray7", font=("Times", 16))

b2 = tk.Button(window, text="QUIT", command=window.quit, bg="royal blue", fg="ghost white", font=("Times", 18))

b3 = tk.Button(window, text="CLEAR", command=clear, bg="gold", fg="gray7", font=("Times", 16))

b1.grid(row=8, column=0, padx=5, pady=10)
b2.grid(row=8, column=1, padx=5, pady=10)
b3.grid(row=9, column=0, padx=5, pady=10)




if __name__ == '__main__':
    window.mainloop()