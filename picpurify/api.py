# -*- coding: utf-8 -*-

'''
Copyright (c) 2019 PicPurify
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
import picpurify


class PicPurify(object):
    '''
    
    '''
    MODERATION_TASKS = ['porn_moderation', 'suggestive_nudity_moderation', 'gore_moderation', 'qr_code_moderation', 'money_moderation',
                        'weapon_moderation', 'drug_moderation', 'hate_sign_moderation', 'obscene_gesture_moderation','qr_code_moderation']
    DETECTION_TASKS = ['face_detection', 'face_gender_detection', 'face_age_detection', 'face_gender_age_detection']
    AVAILABLE_TASKS = MODERATION_TASKS + DETECTION_TASKS + ['content_moderation_profile']
    

    def __init__(self, api_key):
        if type(self) is PicPurify:
            raise TypeError("PicPurify is an abstract class and should not be instanciated directly. Please use PicPurifyVideo or PicPurifyImage.")
        self.API_KEY = api_key
        self.session = requests.Session()
        self.session.headers = requests.utils.default_headers()
        self.session.headers.update({'User-Agent': 'PicPurify-Client-Python-' + picpurify.__version__ })
        
    def updateTasks(self, tasks):
        if type(tasks) is not list:
            raise ValueError('The task parameter must be a list of available task '+ str(tasks) +'\nAvailable tasks :\n' + '\n'.join(self.AVAILABLE_TASKS))
        for task in tasks:
            if task not in self.AVAILABLE_TASKS:
                raise ValueError('This task is not available '+ str(task)+ '\nPlease check the task name or upgrade your package if this task is not available in this package version.')            
        self.tasks = tasks

        
    
    def isSafe(self, data_path, **optional_parameters):
        #check if tasks is only focusing on detection 
        if len(self.tasks) == len(set(self.tasks) & set(self.DETECTION_TASKS)):
            raise ValueError('isSafe method is meant to be used with moderation tasks')
        response = self.analyse(data_path, **optional_parameters)
        if "final_decision" in response:
            return response["final_decision"] == "OK"

       
    def analyseFile(self, file_path, **optional_parameters):
        file_data = {self.file_field: open(file_path, 'rb')}
        post_data =  {"API_KEY": self.API_KEY, "task": ','.join(self.tasks)}
        post_data.update(optional_parameters)
        result_data = requests.post(self.endpoint, files = file_data, data = post_data, headers = self.session.headers)
        return json.loads(result_data.content)
    
    
    def analyseUrl(self, url_data, **optional_parameters):
        post_data =  { self.url_field : url_data, "API_KEY":self.API_KEY, "task": ','.join(self.tasks)}
        post_data.update(optional_parameters)
        result_data = requests.post(self.endpoint, data = post_data, headers = self.session.headers)
        return json.loads(result_data.content)
    
    
    def analyse(self, data_path, **optional_parameters):
        if data_path.lower().startswith(("http://", "https://","data:image/")):
            response = self.analyseUrl(data_path, **optional_parameters)
        else:
            response = self.analyseFile(data_path, **optional_parameters)
        
        if "status" not in response:
            raise  PicpurifyException(50,"Cannot get valid answer from Picpurify endpoint")          
        if response["status"] == "success":
            return response
        elif response["status"] == "failure":
            raise PicpurifyException(response["error"]["errorCode"],response["error"]["errorMsg"])




        
class PicPurifyImage(PicPurify):
    '''
    IMAGE API DOC : https://www.picpurify.com/api-services.html#single_image_api_doc
    
    Optional_parameters: 
    reference_id     String    A unique reference associated to the image in your information system
    origin_id        String    A reference to retrieve the origin of the image, profile id, account id ...
    '''
       
    def __init__(self, api_key, tasks):
        '''
        api_key: your personnal API key (can be found in the "API keys" section in your dashboard
        tasks: an array of tasks pickup in the AVAILABLE_TASKS
        '''
        super(PicPurifyImage, self).__init__(api_key)
        self.updateTasks(tasks)
        self.endpoint = 'https://www.picpurify.com/analyse/1.1'
        
    @property
    def file_field(self):
        return 'file_image'
    
    @property
    def url_field(self):
        return 'url_image'
                 
    

class PicPurifyVideo(PicPurify):
    '''
    VIDEO API DOC : https://www.picpurify.com/api-services.html#video_api_doc
    
    Optional_parameters: 
    frame_interval   Decimal   Interval in seconds between the analyzed images. The default value is 1, which means that one frame every second will be analyzed. Values less than 1 can be used. For example 0.1 means an image every 100 ms.
    reference_id     String    A unique reference associated to the video in your information system
    origin_id        String    A reference to retrieve the origin of the video, profile id, account id ...
    '''
    
    
    def __init__(self, api_key, tasks):
        '''
        api_key: your personnal API key (can be found in the "API keys" section in your dashboard
        tasks: an array of tasks pickup in the AVAILABLE_TASKS
        '''
        super(PicPurifyVideo, self).__init__(api_key)
        self.updateTasks(tasks)
        self.endpoint = 'https://www.picpurify.com/analyse_video/1.1'
         
    @property
    def file_field(self):
        return 'file_video'
    
    @property
    def url_field(self):
        return 'url_video'
        

class PicpurifyException(Exception):
    def __init__(self, errorCode, errorMsg):
        self.errorCode = errorCode
        self.errorMsg = errorMsg
        
    def __str__(self):
        return 'Error code ' + str(self.errorCode) + ' : ' + self.errorMsg
            
def getNbFace(api_key, image_path):
    client = PicPurifyImage(api_key, ['face_detection'])
    response = client.analyse(image_path)
    return response["face_detection"]["nb_face"]


