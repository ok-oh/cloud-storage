from flask import Flask, request
from flask_cors import CORS
from obs import ObsClient
import os


app = Flask(__name__)
CORS(app)

bucket_name = 'cloud-storage-d994'

fileName_Collection = []
filePermission_Collection = {}

username_collection = []
userpassword_collection = []

user_log = {}

obsClient = ObsClient(
    access_key_id='J2ELVMDQAOQBQ7KYMSDB',#刚刚下载csv文件里面的Access Key Id
    secret_access_key='BUwKduv2wVNYfvNy5K49daABqB5NSRwYHfKqf9rK',#刚刚下载csv文件里面的Secret Access Key
    server='obs.cn-east-3.myhuaweicloud.com'#这里的访问域名就是我们在桶的基本信息那里记下的东西
)


# 确保临时目录存在
TEMP_DIR = os.path.join(os.getcwd(), 'tmp')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/')
def home():
    return "Hello, Flask with OBS!"


# 文件上传接口
@app.route('/upload/<username>', methods=['POST'])
def upload_file(username):
    if 'file' not in request.files:
        return 'error'
    file = request.files['file']
    if file.filename == '':
        return 'error'

    file_path = os.path.join(TEMP_DIR, file.filename)
    file.save(file_path)

    resp = obsClient.putFile(bucket_name, file.filename , file_path)

    fileName_Collection.append(file.filename)
    filePermission_Collection[file.filename] = [username]

    if resp.status < 300:
        os.remove(file_path)

        user_log[username].append('you upload the file: ' + file.filename)

        return file.filename+' add success'
    else:
        return 'error'




# 文件下载接口
@app.route('/download/<filename>/<username>', methods=['GET'])
def download_file(filename,username):
    download_path = os.path.join(os.getcwd(), 'download' ,filename)


    for user in filePermission_Collection[filename]:
        user_log[user].append('your file(' + filename +') was downloaded by ' + username)


    if filename in fileName_Collection:
        if username in filePermission_Collection[filename]:
            resp = obsClient.getObject(bucket_name, filename, download_path)
            if resp.status < 300:
                return filename+' download success', resp.status
            else:
                return 'error'

    else:
        return 'error'



@app.route('/delete/<filename>/<username>', methods=['DELETE'])
def delete_file(filename,username):

    if username in filePermission_Collection[filename]:
        resp = obsClient.deleteObject(bucket_name, filename)

        for user in filePermission_Collection[filename]:
            user_log[user].append('your file(' + filename + ') was deleted by ' + username)


        fileName_Collection.remove(filename)
        del filePermission_Collection[filename]



        if resp.status < 300:
            return 'delete success', resp.status
        else:
            return 'error'
    else:
        return 'error'




@app.route('/list/<username>', methods=['GET'])
def list_file(username):
    file_returned = []
    for filename in fileName_Collection:
        if username in filePermission_Collection[filename]:
            file_returned.append(filename)

    return file_returned


@app.route('/addNewUser/<username>/<password>', methods=['POST'])
def addNewUser(username, password):
    if username in username_collection:
        return 'error: user already exist'
    else:
        username_collection.append(username)
        userpassword_collection.append(password)

        user_log[username] = []
        return 'user add success'

@app.route('/login/<username>/<password>',methods=['GET'])
def checkLogin(username, password):
    if username in username_collection:
        index = username_collection.index(username)
        if userpassword_collection[index] == password:
            return 'login pass'
        else:
            return 'permission denied'

    else:
        return 'permission denied'


@app.route('/addPermission/<operator>/<targetFile>/<targetUser>',methods=['POST'])
def addPermission(operator,targetFile,targetUser):
    if operator in filePermission_Collection[targetFile]:
        filePermission_Collection[targetFile].append(targetUser)

        user_log[operator].append('you have given the user(' + targetUser + ') permission to manage the file(' + targetFile + ')' )
        user_log[targetUser].append('you have been given the permission to manage the file(' + targetFile + ') by the user(' + operator + ')')

        return 'permission add success'
    else:
        return 'error'

@app.route('/deletePermission/<operator>/<targetFile>/<targetUser>',methods=['DELETE'])
def deletePermission(operator,targetFile,targetUser):
    if operator in filePermission_Collection[targetFile]:
        filePermission_Collection[targetFile].remove(targetUser)

        user_log[operator].append('you have cancelled the user(' + targetUser + ') permission to manage the file(' + targetFile + ')')
        user_log[targetUser].append('you have been cancelled the permission to manage the file(' + targetFile + ') by the user(' + operator + ')')

        return 'permission delete success'
    else:
        return 'error'


@app.route('/getLog/<username>',methods=['GET'])
def getLog(username):
    return user_log[username]

if __name__ == '__main__':
    app.run(debug=True)
