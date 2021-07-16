# begin-fix-this
NOT MY SERVER, NOT MY PROBLEM

## docker
This is definitely not complete.

You will need a vncviewer, I used remmina.

### Building
```
docker build . -t smash
```

### Running
```
docker run -p 5900:5900 --volume="$HOME/.config/SlippiOnline:/root/.config/SlippiOnline" --volum
e="$(pwd)/../:/app" --rm -it smash
```
