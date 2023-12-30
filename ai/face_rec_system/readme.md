# Standalone Face recognition system

System is working with face-recognition library and working with Flask python framework.

All needed files in this repo folder.

Flask application will run on the port 8000:
```
app.run(host="0.0.0.0", port=8000, debug=True)
```

To create the docker image put all files in your folder. 
And create the same folder structure.

To build the docker image run:
```
docker build -t face_rec_flask . 
```
this will create the standalone docker image.

After you could check that image created by the command:
```
docker images
```

to run the docker container run the command:
```
docker run -p 8000:8000 face_rec_flask
```

then in the browser open local link and use it