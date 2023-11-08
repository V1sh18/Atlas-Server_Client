import socket
import random
import pycountry

# Get a list of all countries
all_countries = list(pycountry.countries)

# Server configuration
HOST = 'localhost'
PORT = 12345

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Store the list of countries
#countries = ["Argentina", "Brazil", "Canada", "Denmark", "Egypt", "France", "Germany", "Hungary", "India", "Japan"]
# Extract country names from the list of country objects
countries = [country.name for country in all_countries]

# Function to initiate the game and handle a client's turn
def handle_client_turn(client_socket, current_country):
    last_letter = current_country[-1]  # Initialize the last letter with the last letter of the current country

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_country = data.decode()

        # Check if the client's country is valid and starts with the last letter of the server's country
        if client_country in countries and client_country.startswith(last_letter):
            # Find a valid country to send back
            valid_countries = [country for country in countries if country.startswith(client_country[-1])]
            if valid_countries:
                response_country = random.choice(valid_countries)
                client_socket.send(response_country.encode())
                last_letter = response_country[-1]
            else:
                client_socket.send("You win! No valid countries left.".encode())
                break
        else:
            client_socket.send("InvalidCountry: Country name should start with the last letter of the previous country.".encode())

    client_socket.close()

# Main server loop
while True:
    client, addr = server_socket.accept()
    # Initiate the game by sending the first country to the client
    initial_country = random.choice(countries)
    client.send(initial_country.encode())
    handle_client_turn(client, initial_country)
