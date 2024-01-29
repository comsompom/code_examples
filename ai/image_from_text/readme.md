Lets combine our knowledges about HuggingFace framework and create Funny simple
Artficial Intelegence Python project for converting the Text from the WEB page to the Picture.
The text could be any you wish - the news, the article from wiki, the messages from chat,
Your LinkedIn Profile page 🙂 or any other you would like to AI imagine as a picture - It is
really funny.

The full code of this script you could find on my GitHub public repo:

Just 50 strings of the Python code and you will be happy with this.

We will use two main AI technologies - the Summarizer which is making the summarisation
of the text and Image from Text Creator. All Libraries you could find in the HuggingFace
portal in the Models section: https://huggingface.co/models

Our project contains just 3 function:
1. First of all we are grabbing the text from the WEB page by using the BeautifulSoup
framework (strings: 16-21). Input for this function is the URL of the WEB page and the
output (return value) is the grabbed text
2. The second step is making the summarization of our grabbed text. This function is
realised in the "summarize_text" (strings: 24-32). Here we could set the maximum length
of the raw text (constant MAX_NEWS_LENGTH) and we could set the length of the summarized
text (constant MAX_SUMMAR_LEN), also we could set different transformers model
(constant TRANSFORMERS_MODEL) in our example we are using one of the simplest pretrained
model "t5-small"
3. The third function is our Funny part - creation image from the summarized text
(strings: 35-41). Here we are using the simplest diffusers model "runwayml/stable-diffusion-v1-5" in the constant DIFFUSERS_MODEL and we are save this image to the file. File name
also could be differ and you could set the name in the constant IMAGE_NAME. The image will be
saved at the same folder as your script. If you will get the error of the image creator function. then just remove
the "torch_dtype=torch.float16" parameter from 37 script string.

For this script we are setting the constants like the URL in which you could change the
WEB page url and also we are using the device for our mathematic like the 'mps' in the
constant DEVICE. We are set the device as 'mps' because the script is working on the
MacBook Air. If you are using other laptop you could set the device as 'cpu' for intel
processors, but this will be slow method, and if you have the NVidia Graphical adapter
then you could set the device as 'cuda'

And just one addition: first run time this script will download all the models (transformers and the image creator) it could take some time - depends from the speed of your Internet connection.

By Cool, Be funny! Lets Code it! Simple and Easy! Just simple things are working well!