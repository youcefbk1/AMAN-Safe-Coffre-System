import serial
from gpiozero import Button, OutputDevice
from signal import pause
import time
import sys
import os
import threading


def timeout():
    """
    Closes the script if no coin is inserted within the next minute.
    """
    print("No coin inserted within the last minute. Closing the script.")
    os._exit(0)


# Start the timeout timer
timer = threading.Timer(10.0, timeout)
timer.start()

# GPIO pins for coin acceptor and relays
coin_signal_pin = 17  # GPIO pin connected to the coin acceptor
relay_pins = {1: 27, 2: 22, 3: 23}  # Relay pins for casier_id 1, 2, and 3

total_amount_inserted = 0  # Total value of coins inserted
price_to_reach = 0  # Price received from PC
casier_id = None  # Casier ID received from PC
payment_successful = False  # Flag to track payment status

# Coin value per pulse (adjust based on your coin acceptor configuration)
coin_value_per_pulse = 10  # 1 pulse = 10 DA

# Initialize relay objects for each GPIO pin
relays = {
    1: OutputDevice(relay_pins[1], active_high=True, initial_value=False),
    2: OutputDevice(relay_pins[2], active_high=True, initial_value=False),
    3: OutputDevice(relay_pins[3], active_high=True, initial_value=False),
}

# Initialize UART communication
uart = serial.Serial(
    port="/dev/serial0",  # Use '/dev/serial0' or '/dev/ttyS0' for Raspberry Pi
    baudrate=9600,
    timeout=1,
)


def receive_data():
    """
    Receives the price and casier_id from the PC via UART.
    Format: "price:casier_id"
    """
    global price_to_reach, casier_id
    try:
        data = uart.readline().decode("utf-8").strip()  # Read UART data
        if ":" in data:  # Ensure the format is "price:casier_id"
            price_str, casier_id_str = data.split(":")
            price_to_reach = int(price_str)
            casier_id = int(casier_id_str)
            print(f"Received Price: {price_to_reach} DA, Casier ID: {casier_id}")
        else:
            print(f"Invalid data received: {data}")
    except Exception as e:
        print(f"UART Error: {e}")


def activate_relay(casier_id):
    """
    Activates the relay corresponding to the given casier_id.
    """
    if casier_id in relays:
        print(
            f"Opening relay for casier ID {casier_id} (GPIO {relay_pins[casier_id]})."
        )
        relay = relays[casier_id]
        relay.on()  # Turn on the relay
        time.sleep(1)  # Keep the relay open for 5 seconds (adjust as needed)
        relay.off()  # Turn off the relay
        print(f"Relay for casier ID {casier_id} has been closed.")
    else:
        print(f"Invalid casier ID: {casier_id}. No relay found.")


def coin_inserted():
    """
    Increments the total inserted value when a coin is inserted and checks if the price is reached.
    """
    global total_amount_inserted, price_to_reach, casier_id, payment_successful
    if payment_successful:  # Ignore pulses if payment is already successful
        return

    # Add the value of the coin to the total
    total_amount_inserted += coin_value_per_pulse
    print(f"Coin Pulse Detected! Total Amount: {total_amount_inserted} DA")

    # Check if the inserted amount matches or exceeds the received price
    if total_amount_inserted >= price_to_reach:
        print("? Payment Successful!")
        payment_successful = True  # Set the payment flag
        uart.write(b"done\n")  # Send "done" message to PC
        if casier_id is not None:
            activate_relay(casier_id)  # Open the relay for the specific casier
        else:
            print("casier not recognized")
        reset_coin_acceptor()  # Reset the coin acceptor state


def reset_coin_acceptor():
    """
    Resets the coin acceptor state and unbinds the coin_inserted event.
    """
    global total_amount_inserted, payment_successful
    total_amount_inserted = 0  # Reset the total amount
    payment_successful = False  # Reset the payment flag
    coin_input.when_pressed = None  # Unbind the coin_inserted function
    print("Coin acceptor reset and coin_inserted unbound.")
    os._exit(0)


# Set up GPIO button for coin acceptor

coin_input = Button(coin_signal_pin, pull_up=True)
coin_input.when_pressed = coin_inserted  # Attach function

print("Waiting for price and casier ID from PC...")

# Track the start time
# start_time = time.time()

# Wait until price and casier_id are received
while price_to_reach == 0 or casier_id is None:
    receive_data()
    time.sleep(0.1)  # Add a short delay to reduce CPU usage
    # Check if the script has been running for more than 1 minute
    # if time.time() - start_time > 10:
    # print("Script has been running for more than 1 minute. Exiting...")
    # os._exit(0)

print(f"Ready! Insert coins to reach {price_to_reach} DA for casier ID {casier_id}.")


pause()  # Keep the script running
