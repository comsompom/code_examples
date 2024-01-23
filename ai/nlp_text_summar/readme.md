# Standalone NLP Transformer application

System is working with transformers library and working with Flask python framework.

for change the transformers model you could go to the
HuggingFace web page:
```
https://huggingface.co/models?pipeline_tag=summarization&sort=trending
```
get the nlp model that fits your needs and in the summarizer.py
file in the:
```
model_name = "t5-small"
```
set that model that you need. For example:
```
google/pegasus-cnn_dailymail
```
but check the model size, because some of them more than 2-3Gb.

All needed files in this repo folder.

Flask application will run on the port 8000:
```
app.run(host="0.0.0.0", port=8000, debug=True)
```

To create the docker image put all files in your folder. 
And create the same folder structure.

To build the docker image run:
```
docker build -t python-nlp . 
```
this will create the standalone docker image.

After you could check that image created by the command:
```
docker images
```

to run the docker container run the command:
```
docker run -p 8000:8000 python-nlp
```

then in the browser open local link and use it