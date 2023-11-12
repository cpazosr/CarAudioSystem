# CarAudioSystem

This project is a car audio player built thinking about the many users involved in a car journey.

Developed by @AgusDV111 and @cpazosr.

The audio player is a simultaneous asynchronous multi interface system. It has three different interfaces: 
- Touch screen for the driver and copilot to use easily. The main HMI
- Buttons for Play/Pause, Prev, Next, and encoder for volume control, all ideally located around the wheel for the driver to use easily
- IR controller for passengers

All these interfaces are to have the same functionalities and to work simultaneously, so any user in the vehicle can access the system.

### Block Diagram

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/f0a4d7e9-a55a-4f06-b32d-a056af66dbf7)

The system consists of two asynchronous boards:
- Arduino MEGA as hardware-software interface
- Raspberry Pi4 as main processing unit

Arduino connects to all sensors and physical interfaces like buttons and encoder. It receives the data from all components and connects with RPi for processing. Connection is through UART communication. 

RPI processes all information from all interfaces and controls the entire system. It connects to the speakers and to the main HMI, the touchscreen.

### Arduino MEGA

It receives all information from sensors and physical interfaces, process the input and outputs to the RPi to handle the commands and new data.

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/ce54f733-8424-43fc-a369-da42dfb85647)

The components:
- Rotary Encoder: for controlling volume (ideally driver)
- Buttons: for play/pause, prev, next song functionalities
- RTC-1307: for obtaining time for display in HMI
- DMT-11: for obtaining temperature and humidity to display in HMI
- IR sensor: for receiving commands through the remote controller

All information is read and formatted for the RPi to receive and process it. The logic is as follows:

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/85c0e650-14fb-4efd-9d9e-bcf7d8c49f40)

### Raspberry Pi 4

The main processing occurs here. The core of the program is playing the selected audio file through the speakers while displaying all info related to the audio in the HMI, serving at the same time as another user interface. The HMI has been programmed with Python's Tkinter and sound management through pygame. Because the systems is simultaneous, and commands come from different interfaces, specially from the Arduino, processes are handled through multi-threading and queuing. Software components and logic relates as follows:

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/76a61e3a-fe49-4c4c-8a6e-782fd9a9b129)


### Extended Functionalities

All users through each interface should be able to access the respective functionalities with no monopolization of any specific interface or user.

The main HMI:

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/be245ebf-6026-4086-8377-d5fc4c496eef)

Has these functionalities:

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/44bc8d83-dca4-4d6b-add3-faf6a072fedb)

- Displays date and hour obtained by the sensor
- Displays song name and artist
- Displays song time slider and song time elapsed
- Digital buttons for previous, play/pause, next song
- Digital button for mute/unmute
- Displays volume - from 0 to 100
- Digital tick box to shuffle/un-shuffle songs in queue
- Digital button for displaying a pop-up that shows all info related to the song - Artist, Album, Year, Producer, etc...
- Displays Humidity, Temperature and Heat Index obtained by sensor
- Digital button Ratings for displaying a pop-up that shows the list of songs with respective ratings
- Digital Button USB extension to pass the songs from a connected USB to RPi into the system playlist

The Remote Controller has these functionalities:

![imagen](https://github.com/cpazosr/CarAudioSystem/assets/67598380/63be99f5-2377-4ecc-b606-7359f7bf083c)

- PWR - Turn off system
- MODE - Displays song info
- Mute/Unmute
- Play/Pause
- Previous song or rewind
- Next song
- EQ - Displays songs ratings
- Minus (-) - Reduce volume
- Plus (+) - Increase volume
- Shuffle
- U/SD - add songs from connected USB
- 0 - 9: rate the current song

### Results

You can see a demonstration of the system here: https://www.youtube.com/watch?v=0I5TJeVoINs&ab_channel=ManuelAgust%C3%ADnD%C3%ADazVivanco

Check out the attached report file (Spanish version) to have more info
