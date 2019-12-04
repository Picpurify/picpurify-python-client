# picpurify-python-client 

Python client library for accessing PicPurify moderation API.

## Before starting

Please make sure you have created an account on https://www.picpurify.com/signup.html to collect your personal API key.

Your personnal API key can be found in your dashboard in the "API keys" tab: https://www.picpurify.com/apikey.html

## Installation 
```
pip install picpurify

```

## Usage
```
#### Check image safety
from picpurify.api import PicPurifyImage

client_image = PicPurifyImage('YOUR_PERSONAL_API_KEY',['porn_moderation','gore_moderation','obscene_gesture_moderation'])
response = client_image.analyse('https://s3-eu-west-1.amazonaws.com/site-picpurify/images/porn-accepted-example.jpg')
if response["final_decision"] == "OK":
    print('Image Accepted')
else:
    print('Image Rejected')
    print('Reject criteria: %s' % (','.join(response["reject_criteria"])))

```
## Documentation

API documentation can be found at <https://www.picpurify.com/api-services.html>.

