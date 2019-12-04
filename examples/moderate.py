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

from picpurify.api import *

my_api_key = 'YOUR_PERSONAL_API_KEY'


#Image moderation
client_image = PicPurifyImage(my_api_key,['porn_moderation'])
print(client_image.analyse('https://s-media-cache-ak0.pinimg.com/736x/80/21/ec/8021ec8484c7849130cccdb026c372ce.jpg'))
print('')
 
client_image.updateTasks(['gore_moderation','obscene_gesture_moderation'])
print(client_image.analyse('https://s-media-cache-ak0.pinimg.com/736x/80/21/ec/8021ec8484c7849130cccdb026c372ce.jpg', origin_id = 'MY_ORIGIN_ID', reference_id = 'MY_REFERENCE_ID'))
print('') 

client_image.updateTasks(['weapon_moderation'])
is_safe_image = client_image.isSafe('https://www.everydaynodaysoff.com/wp-content/uploads/2016/03/revolver-gun-extendo-clip.jpg')
if is_safe_image:
    print('Image Accepted')
else:
    print('Image Rejected')
print('')

client_image.updateTasks(['porn_moderation','face_age_detection'])
is_safe_image = client_image.isSafe('https://www.everydaynodaysoff.com/wp-content/uploads/2016/03/revolver-gun-extendo-clip.jpg')
if is_safe_image:
    print('Image Accepted')
else:
    print('Image Rejected')
print('')


nb_faces = getNbFace(my_api_key,'https://cdn.pixabay.com/photo/2018/01/24/19/49/people-3104635_960_720.jpg')
print('Faces detected in image : %s' % (nb_faces))
print('')

#Video moderation
client_video = PicPurifyVideo(my_api_key,['face_detection','porn_moderation'])
print(client_video.analyse('https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_480_1_5MG.mp4', frame_interval=2))


