FROM ubuntu:latest
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip x11vnc xvfb libao-dev libasound2-dev libavcodec-dev libavformat-dev libbluetooth-dev libenet-dev libgtk2.0-dev liblzo2-dev libminiupnpc-dev libopenal-dev libpulse-dev libreadline-dev libsfml-dev libsoil-dev libsoundtouch-dev libswscale-dev libusb-1.0-0-dev libwxbase3.0-dev libwxgtk3.0-gtk3-dev libxext-dev libxrandr-dev portaudio19-dev zlib1g-dev libudev-dev libevdev-dev libmbedtls-dev libcurl4-openssl-dev libegl1-mesa-dev libpng-dev qtbase5-private-dev libxxf86vm-dev x11proto-xinerama-dev xterm
RUN apt clean -y && apt autoremove -y && apt autoclean -y
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN ./Slippy.AppImage --appimage-extract
COPY . .
RUN echo "exec python3 /app/example.py -e /app/squashfs-root/usr/bin --iso iso/smash.iso" > ~/.xinitrc && chmod +x ~/.xinitrc
RUN mkdir -p /root/.config/SlippiOnline/Config
RUN cp Dolphin.ini /root/.config/SlippiOnline/Config/Dolphin.ini
EXPOSE 5900
CMD ["x11vnc", "-create", "-forever"]
