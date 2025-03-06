### Create the Simple FastAPI app

to start fom local terminal:

```commandline
uvicorn main_page:app
```

or it is also possible to run the command:

```commandline
fastapi run main_page.py 
```

after start the fastapi go to the local address:
http://0.0.0.0:8000/docs

then click to the **"POST"** the to the button **"Try it out"**, 
then in the **"num_arr"** 
field input the numeric array separated with comma:

```commandline
6, 4, 12, 10, 22, 54, 32, 42, 21, 11
```
then press big blue button "execute"

and in the section "Response body" You will see the result.

to build the docker:

```commandline
docker build -t fast-api .
```

check the image done

```commandline
docker images
```

start the docker container

```commandline
docker run -p 8000:8000 fast-api
```

to check the container in memory:

```commandline
docker ps
```

to delete the container:

```commandline
docker rmi XXXXXXcontainer-image_xxx -f
```
