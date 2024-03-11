## Orc's Tank image classifier

The AI image classifier model design to collect and classify the Russian's orcs Army 
units for the purpose of correctly destroing them.

The Image model designed with two main components:
* Dataset downloader
* Image processor

### Dataset image creator

Automatically download and create the images Label set for model classification.
in the ``constants`` ``IMAGE_LABEL_LIST`` should be described in the list the labels 
by which will be created the model. All main lists already created and described in the 
```constants.py``` file and you could copy and set or add them or change in to the 
``IMAGE_LABEL_LIST`` constant. 

Also the ```DatasetCreator``` class is possible to use like a standalone application for 
the image label dataset
The variable ```TIME_SLEEP_AFTER_EACH_DOWNLOAD``` is set to the time sleep after each 
image download because some of the search engine does not allow to download a lot of 
images by once.
The variable ```EACH_LABEL_COUNT``` has the value of the downloaded images for each 
label category in the model. For the best practice this value should be at least 1000 
images in one category, but it could take some time for creating the model with the 
huge number of the images. After dataset image downloader will be finished and images 
will be downloaded and created in the separated categories then it is recomended 
manually check the categories and remove the images that does not fit to the category 
or duplicated

### Image processor

The image processor create the model, train it, save the weights in to the file 
```PRETRAINED_WEIGHTS_PATH``` and predict the image from url (from internet or local)
It is important to use one image height and one image width for the all images in the 
label set for creating the correctly working model. This values could be set in the 
valiables: ```IMAGE_WIDTH``` and ``IMAGE_HEIGHT``

The main Image processor variables are set in the variables:
* ```BATCH_SIZE``` for the send the batches of the images in the train process
* ```MODEL_EPOCH``` for the number of the train epochs
* ```MODEL_OPTIMIZER``` for the model optimizer - for tune process it could be differ
* ```MODEL_LAYER_ACTIVATION``` for the layers activation inside the model

To use the model in the code you need to Initialise it and put some parameters to it:

```
img_url = "https://thediplomat.com/wp-content/uploads/2016/07/sizes/medium/thediplomat_2016-07-19_16-31-08.jpg"
image_processor = ImgClassifierProcessor(new_dataset=False, show_logs=True, use_weights=True, model_augment=False)
prediction = image_processor.model_prediction_process(img_url)
print(prediction)
```

in the ``img_url`` variable you should to set up the image Url of the Orcs tank that you 
need to classify.

inside the ```image_processor``` there are some init variables:

``new_dataset`` if it Sets the `True` then new datase from the constant ``IMAGE_LABEL_LIST``
will be downloaded abd created for the model. ``False`` value will be using the current
model dataset from the ``labels`` folder.

``show_logs`` if set to the ``True`` then all models logging will be printed in the console

``use_weights`` if set to the ``True`` then it will use the already calculated model 
weights from the constant ```PRETRAINED_WEIGHTS_PATH```. If the model created from the 
scratch then set this value to the ``False``

```model_augment``` if set to the ``True`` then extra augmentation will be calculated 
until the model training process is going on. This method is usefull when the model 
has a small number of the trained image data

the the ```prediction``` will execute the ``model_prediction_process`` method with 
the input variable of the ``img_url`` for predicting the image

and at the end the prediction of that model is predicted will be output to the console

