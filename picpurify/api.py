# -*- coding: utf-8 -*-

'''
Copyright (c) 2019 Picpurify
https://www.picpurify.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import os, json, requests
#import picpurify

class PicpurifyClient(object):
    available_tasks = ['porn_detection', 'suggestive_nudity_detection', 'gore_detection', 'writing_detection', 'qr_code_detection', 'money_detection',
                        'weapon_detection', 'drug_detection', 'nazis_swastika_detection', 'obscene_gesture_detection', 'face_gender_detection', 'face_detection']

    def __init__(self, api_key, tasks = None):
        self.API_KEY = api_key
        self.tasks = tasks
        self.endpoint = 'https://www.picpurify.com/analyse.php'
        #self.headers = {'User-Agent': 'Picpurify-Client-Python-' + picpurify.__version__ }
        self.headers = {'User-Agent': 'Picpurify-Client-Python-' + '1.0' }
        
    
    def analyse_file(self, image_path, tasks, origin_id = None, reference_id = None):
        img_data = {'file_image': open(image_path, 'rb')}
        post_data =  { "API_KEY":self.API_KEY, "task": tasks}
        if origin_id is not None:
            post_data['origin_id'] = origin_id
        if reference_id is not None:
            post_data['reference_id'] = reference_id
        result_data = requests.post(self.endpoint,files = img_data, data = post_data)
        return json.loads(result_data.content)
    
    
    def analyse_url(self, url_image, tasks, origin_id = None, reference_id = None):
        post_data =  { "url_image" : url_image, "API_KEY":self.API_KEY, "task": tasks}
        if origin_id is not None:
            post_data['origin_id'] = origin_id
        if reference_id is not None:
            post_data['reference_id'] = reference_id
        result_data = requests.post(self.endpoint, data = post_data)
        return json.loads(result_data.content)
    
    
    def analyse(self, image, origin_id = None, reference_id = None):
        if image.lower().startswith(('http://', 'https://')):
            return self.analyse_url(image, self.tasks, origin_id, reference_id)
        else:
            return self.analyse_file(image, self.tasks, origin_id, reference_id)
        
        
        
#     def feedback(self, predict, real, image):


# 
#         output = json.loads(r.text)
#         return output


test = PicpurifyClient('44ec0a838ffd7aa90955ba50a9b4e502','porn_detection')
print(test.analyse('https://s-media-cache-ak0.pinimg.com/736x/80/21/ec/8021ec8484c7849130cccdb026c372ce.jpg'))
print('')
origin_id = 'toto'
reference_id = 'tata'
print(test.analyse('https://s-media-cache-ak0.pinimg.com/736x/80/21/ec/8021ec8484c7849130cccdb026c372ce.jpg',origin_id,reference_id))
