import socket
import tkinter as tk

# Client configuration
HOST = 'localhost'
PORT = 12345

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to send the selected country to the server
def send_country():
    country = entry.get()
    if country:
        client_socket.send(country.encode())
        entry.delete(0, tk.END)
        response = client_socket.recv(1024).decode()
        display_response(response)

# Function to display the server's response
def display_response(response):
    response_label.config(text=f"Server's Country: {response}")

# Create a GUI
window = tk.Tk()
window.title("Atlas Game")
entry = tk.Entry(window)
entry.pack()
send_button = tk.Button(window, text="Send Country", command=send_country)
send_button.pack()
response_label = tk.Label(window, text="")
response_label.pack()

# Function to receive the initial country from the server
def receive_initial_country():
    initial_country = client_socket.recv(1024).decode()
    display_response(initial_country)

# Display the initial country from the server
receive_initial_country()

window.mainloop()
