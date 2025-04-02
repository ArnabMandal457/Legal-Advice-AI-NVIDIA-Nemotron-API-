import threading
import time
from tkinter import * # type: ignore
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
from openai import OpenAI
# import random
# from dotenv import load_dotenv
import os
# load_dotenv()

script_dir = os.path.dirname(__file__)

global query, q
q= 0
query= ""


def op():
    global q
    user_query.delete("1.0",END)
    chat.config(state="normal")
    if(q!=1):
        chat.delete("1.0",END)
        chat.insert(END,"YOU: "+query)
        q= 1
    else:
        chat.insert(END,"\n\nYOU: "+query)
    chat.see(END)
    send.config(state="disabled")
    clear.config(state="disabled")

def respond():
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key= "YOUR_API_KEY"
    )
    greeting= {1:"Hi, how may I help you today?", 2:"Hey! What's up? How can I help you today?", 3:"Hello! How can I assist you?"}
    # chat.config(state="normal")
    chat.insert(END, "\nAGENT: ")
    chat.see(END)

    # Stream response word by word
    def stream_response():
        
        buffer = ""  # Temporary storage for building words
        
        for chunk in client.chat.completions.create(
            model="nvidia/nemotron-4-340b-instruct",
            messages=[{"role": "user", "content": f'''I need legal advice regarding {query}. Could you provide detailed information about:

-All The relevant laws and regulations in India. Use bullet points explaining each law and use newline 2 times after each point.

-Step-by-step guidance on how to proceed.

-Potential risks, rights, and obligations I should be aware of.

-Any supporting documents or evidence I may need.

-Alternative solutions if the primary approach doesn't work.
                           
For context, I am seeking clear and practical advice. Please explain it in simple terms, avoiding excessive legal jargon wherever possible.
Take reference from Constitution of India and Indian Penal Code and every relevant rule-book of India for relevant laws and regulations.
**Include that you are an AI model and these are the details that you know or just an overview and also tell the user to consult some professional for the same for better explanation**
'''}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        ):
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                for char in text:
                    if char=="*":
                        continue
                    else:
                        buffer += char  # Add character to buffer
                        if char.isspace() or char in {".", ",", "!", "?"}:  # Send when space or punctuation appears
                            win.after(0, lambda b=buffer: append_to_chat(b))
                            buffer = ""  # Reset buffer
                            time.sleep(0.03)  # Smooth streaming delay
        
        # Flush remaining text in buffer
        if buffer:
            win.after(0, lambda: append_to_chat(buffer))

        win.after(0, lambda: send.config(state= NORMAL))  # Re-enable send button
        win.after(0, lambda: clear.config(state= NORMAL))  # Re-enable send button
        win.after(0, lambda: chat.config(state= DISABLED)) #Disable user writng to the chatbox

    threading.Thread(target=stream_response, daemon=True).start()

# Function to append text to chatbox
def append_to_chat(text):
    chat.insert(END, text)
    chat.see(END)


def combined():
    global query, q
    query= user_query.get("1.0", END)
    if query=="" or query=="\n" or query=="Enter your query here.\n":
        messagebox.showinfo('EMPTY QUERY!','Your query is epmty please enter a query to proceed further')
    else:
        chat.config(fg="black")
        op()
        win.after(1,respond)

class PlaceholderScrolledText(scrolledtext.ScrolledText):
    def __init__(self, master=None, placeholder="Placeholder Text", writable=True, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.insert("1.0", self.placeholder)
        self.configure(fg="grey")
        if(writable==True):
            self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)


    def clear_placeholder(self, event):
        if self.get("1.0", END).strip() == self.placeholder:
            self.delete("1.0", END)
            self.configure(fg="black")

    def add_placeholder(self, event):
        if not self.get("1.0", END).strip():
            self.insert("1.0", self.placeholder)
            self.configure(fg="grey")

def clear_chat():
    global q, query
    if query=="" or query=="\n" or query=="Enter your query here.\n":
        messagebox.showinfo('EMPTY QUERY!','No chat to clear :(')
    else:
        chat.config(state="normal")
        chat.delete("1.0",END)
        chat.insert("1.0","Chat with the AI Agent will appear here.")
        chat.config(state="disabled", fg="grey")
        query=""
        q=0

win= Tk()
width= win.winfo_screenwidth()         #Width of the screen
height= win.winfo_screenheight()        #Height of the screen
win.resizable(width=True, height=True)#Resizability of the window
win.state('zoomed')
win.geometry("%dx%d+0+0" % (width,height))

message= Label(win,text='Welcome...',font=('Garamond',50))
message.place(x=0,y=0)

image = Image.open(os.path.join(script_dir, "send.png"))
image = image.resize((40, 40))
photo_image = ImageTk.PhotoImage(image)
send= Button(win,image=photo_image,text='Send',font=('bold',16),compound="left",command= lambda:[combined()])
send.place(x=0.61848958333333336*width,y=0.8680555555555556*height)
send.image= photo_image  # type: ignore

image = Image.open(os.path.join(script_dir, "clear.png"))
image = image.resize((40, 40))
photo_image = ImageTk.PhotoImage(image)
clear= Button(win,image=photo_image,text='Clear Chat',font=('bold',16),compound="left",command= lambda:[clear_chat()])
clear.place(x=0.44921875*width,y=0.8680555555555556*height)
clear.image= photo_image  # type: ignore

image = Image.open(os.path.join(script_dir, "close.png"))
image = image.resize((40, 40))
photo_image = ImageTk.PhotoImage(image)
close= Button(win,image=photo_image,text='Close',font=('bold',16),compound="left",command= lambda:[win.destroy()])
close.place(x=0.32552083333333334*width,y=0.8680555555555556*height)
close.image= photo_image  # type: ignore


user_query = PlaceholderScrolledText(win, placeholder="Enter your query here.",font=(16), width=100, height=5)
user_query.place(x=0.07*width,y=0.7*height)

chat = PlaceholderScrolledText(win, placeholder="Chat with the AI Agent will appear here.",writable=False, font=(20), width=100, height=20)

chat.config(state="disabled")
chat.place(x=0.07*width,y=0.11*height)

win.mainloop()