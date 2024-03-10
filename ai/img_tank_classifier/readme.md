## Orc's Tank image classifier

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

