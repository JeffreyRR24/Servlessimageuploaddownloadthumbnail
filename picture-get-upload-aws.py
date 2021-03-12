import json
import requests 
import re
object_id = ''
user = ''
catcolour = ''
picture = ''
#replace api_id with the api id when the cloudformation template is create_complete
api_id = 'gxnrnjmu19'

print('What do you want to do?')
print()
print('1)list objects')
print('2)list metadata')
print('3)download original image')
print('4)download thumbnail')
print('5)upload')
print('6)exit')
print()

what=str(input("please enter the number of the function you want to use: "))
while not re.match("^^[1-6]$", what):
    print ("Error! Make sure you only input 1-6")
    what = (input())

if what < "6":
    class catconnect():
        '''
        this class contains our available api endpoints and a sample of how to interact with our services
        '''
        def __init__(self, object_id, user, catcolour, picture, api_id):
            '''
            construct all the variables and endpoints for easy use.
            '''
            self.object_id = object_id
            self.user = user
            self.catcolour = catcolour
            self.picture = picture
            self.list_of_objects = []
            self.list_of_meta = []
            self.list_url = 'https://'+api_id+'.execute-api.eu-west-1.amazonaws.com/development/list'
            self.upload_url = 'https://'+api_id+'.execute-api.eu-west-1.amazonaws.com/development/upload'
            self.download_url = 'https://'+api_id+'.execute-api.eu-west-1.amazonaws.com/development/download'
            self.thumbnail_url = 'https://'+api_id+'.execute-api.eu-west-1.amazonaws.com/development/thumbnail'
            self.metadata_url = 'https://'+api_id+'.execute-api.eu-west-1.amazonaws.com/development/metadata'

        def list_objects(self):
            '''
            gets a list of objects and prints it to the console 
            '''
            request_api = requests.request(method='get', url=self.list_url)
            response = json.loads(request_api.content)
            self.list_of_objects.append(response['body'])
            print(self.list_of_objects)

        def list_metadata(self):
            '''
            gets a list of objects with metadata and prints it to the console
            '''
            request_api = requests.request(method='get', url=self.metadata_url)
            response = json.loads(request_api.content)
            self.list_of_meta.append(response['body'])
            print(self.list_of_meta)
            
        def download_thumbnail(self):
            '''
            gets a presigned url of the object_id specified,
            downloads a small thumbnail of a specified object and saves it under TN_object_id.jpg
            '''
            object_id = {"object_id" : self.object_id}
            data = json.dumps(object_id)
            request_api = requests.request(method='put', url=self.thumbnail_url, data=data)
            json_response = json.loads(request_api.content)
            presign_url = json_response['body']
            request_get = requests.request(method='get', url=presign_url)
            img_data = request_get.content
            img_id = json.loads(data)
            thumb = 'TN_'+img_id['object_id']
            with open(thumb, 'wb')as fp:
                fp.write(img_data)
            print('succes', thumb, ' saved')

        def download(self):
            '''
            gets a presigned url of the object_id specified, 
            downloads the picture of a specified object_id and saves it under object_id.jpg
            '''
            object_id = {"object_id" : self.object_id}
            data = json.dumps(object_id)
            request_api = requests.request(method='put', url=self.download_url, data=data)
            json_response = json.loads(request_api.content)
            presign_url = json_response['body']
            request_get = requests.request(method='get', url=presign_url)
            img_data = request_get.content
            img_id = json.loads(data)
            with open(img_id['object_id'], 'wb')as fp:
                fp.write(img_data)
            print('succes', img_id['object_id'], ' saved')

        def upload(self):
            '''
            sends user_id & catcolour to the api endpoint, gets back a presigned url with the correct metafields
            uploads the data of picture to the presigned url
            '''
            data = {"user_id": self.user, "cat_colour": self.catcolour}
            c = json.dumps(data)
            request_api = requests.request(method='put', url=self.upload_url, data=c)
            jsonresp = json.loads(request_api.content)
            presigned = jsonresp['body']
            print(presigned)
            with open(self.picture ,'rb') as fp:
                bins = fp.read()
            post = requests.put(url=presigned, data=bins, headers={"Content-Type":"image/jpeg"})
            print(post)


    if __name__ == "__main__":
        if what == "1":
            catconnect(object_id, user, catcolour, picture, api_id).list_objects()
        if what == "2":
            catconnect(object_id, user, catcolour, picture, api_id).list_metadata()
        if what == "3":
            object_id = input('insert a object id:')
            catconnect(object_id, user, catcolour, picture, api_id).download()
        if what == "4":
            object_id = input('insert a object id:')
            catconnect(object_id, user, catcolour, picture, api_id).download_thumbnail()
        if what == "5":
            user = input('input user_id :')
            catcolour = input('input the cats colour, or something :')
            picture = input('input picture path :')
            catconnect(object_id, user, catcolour, picture, api_id).upload()
        #invoke the class catconnect and pass along all the needed __init__ fields. these can be empty if they dont apply.
        #invoke function. available; .list_objects() .list_metadata() .download() .download_thumbnail() .upload()
        #catconnect(object_id, user, catcolour, picture ,api_id).list_objects() # lists only the object names that are in the bucket.
        #catconnect(object_id, user, catcolour, picture ,api_id).list_metadata() # all fields can stay empty, returns a list of metadata and objects
        #catconnect(object_id, user, catcolour, picture ,api_id).download() #  all fields except object id can stay empty, object id should be a valid object in the bucket
        #catconnect(object_id, user, catcolour, picture ,api_id).download_thumbnail() # all fields except object id can stay empty, object id should be a valid object in the bucket
        #catconnect(object_id, user, catcolour, picture ,api_id).upload() # object id can stay empty, user catcolour and picture should be included, user and catcolour are string, picture is string and should be a file whitin the script folder.
