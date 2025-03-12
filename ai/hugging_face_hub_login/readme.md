# How to login to Hugging face HUB

Some time using models from the HuggingFace HUB you could see 
in the code the errors like:
```commandline
access to model <MODEL-NAME> is restricted. you must have access to it and be authenticated to access it. please
```

to avoid this proble you need to register in the HuggingFace as
a developper and get the access token from it.
Then you need to connect to the HUB using the CLI:

https://huggingface.co/docs/huggingface_hub/main/en/guides/cli#huggingface-cli-whoami

or you could create the token file, and put your token to it and then 
use this token dirrectly in your code before getting access to the model:

```python
from huggingface_hub import login


with open('hf_token', 'r') as token_file:
    hf_token = token_file.read()

login(token=hf_token)
```
