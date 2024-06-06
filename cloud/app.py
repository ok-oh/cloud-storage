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



def add_permission_to_file(filename, username, permission):
    for user in filePermission_Collection[filename]:
        if username in user:
            filePermission_Collection[filename].remove(user)


    filePermission_Collection[filename].append({username:permission})


def set_permission_of_new_file(filename, exception):
    for user in username_collection:
        if user != exception:
            add_permission_to_file(filename,user,2)
        else:
            add_permission_to_file(filename,user,0)

def get_permission_of_the_file(filename, username):
    print(filename)
    print(filePermission_Collection)
    for user in filePermission_Collection[filename]:
        if username in user:
            return user[username]
    return None

def remove_permission_of_the_file(filename, username):
    add_permission_to_file(filename,username,2)

def get_root_user_of_the_file(filename):
    user_found = []
    for user in username_collection:
        if get_permission_of_the_file(filename,user) == 0:
            user_found.append(user)
    return user_found





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



    if resp.status < 300:
        os.remove(file_path)
        if file.filename not in fileName_Collection:
            fileName_Collection.append(file.filename)
            filePermission_Collection[file.filename] = []

        set_permission_of_new_file(file.filename, username)
        user_log[username].append('you upload the file: ' + file.filename)
        print(filePermission_Collection)
        return file.filename+' add success'
    else:
        return 'error'


#0最高权限(可删除），1下载权限

# 文件下载接口
@app.route('/download/<filename>/<username>', methods=['GET'])
def download_file(filename,username):
    download_path ='C:/Users/86189/Downloads/' + filename

    if get_permission_of_the_file(filename, username) < 2:
        resp = obsClient.getObject(bucket_name, filename, download_path)
        if resp.status < 300:

            for user in get_root_user_of_the_file(filename):
                user_log[user].append('your file(' + filename + ') was downloaded by ' + user)

            user_log[username].append('you download the file(' + filename + ')')
            return filename + 'download success'
        else:
            return 'error'
    else:
        return 'error'




@app.route('/delete/<filename>/<username>', methods=['DELETE'])
def delete_file(filename,username):

    if username in get_root_user_of_the_file(filename):
        resp = obsClient.deleteObject(bucket_name, filename)

        if resp.status < 300:
            for user in get_root_user_of_the_file(filename):
                user_log[user].append('your file(' + filename + ') was deleted by ' + username)
            fileName_Collection.remove(filename)
            del filePermission_Collection[filename]
            return filename + ' delete success'
        else:
            return 'error'
    else:
        return 'error'

    # for user in filePermission_Collection[filename]:
    #     if username in user and user[username] == 0:
    #         resp = obsClient.deleteObject(bucket_name, filename)
    #         for log_user in filePermission_Collection[filename]:
    #             if list(log_user.values())[0] == 0:
    #                 user_log[list(log_user.keys())[0]].append('your file(' + filename + ') was deleted by ' + username)
    #         fileName_Collection.remove(filename)
    #         del filePermission_Collection[filename]
    #
    #
    #         if resp.status < 300:
    #             return 'delete success', resp.status
    #         else:
    #             return 'error'



@app.route('/list/<username>', methods=['GET'])
def list_file(username):
    file_returned = []
    for filename in fileName_Collection:
        if get_permission_of_the_file(filename,username) < 2:
            file_returned.append(filename)
    return file_returned


@app.route('/addNewUser/<username>/<password>', methods=['POST'])
def addNewUser(username, password):
    if username in username_collection:
        return 'error: user already exist'
    else:
        username_collection.append(username)
        userpassword_collection.append(password)

        for file in fileName_Collection:
            add_permission_to_file(file,username,2)

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


@app.route('/addPermission/<operator>/<targetFile>/<targetUser>/<permission_level>',methods=['POST'])
def addPermission(operator,targetFile,targetUser,permission_level):
    if operator in get_root_user_of_the_file(targetFile):
        add_permission_to_file(targetFile, targetUser, int(permission_level))
        user_log[operator].append('you have given the user(' + targetUser + ') permission level_'+ permission_level +' of the file(' + targetFile + ')')
        user_log[targetUser].append('you have been given the permission level_' + permission_level + ' of the file(' + targetFile + ') by the user(' + operator + ')')
        return 'permission add success'
    else:
        return 'error'

    # for user in filePermission_Collection[targetFile]:
    #     if operator in user and user[operator] == 0:
    # #if operator in filePermission_Collection[targetFile]:
    #
    #         for target_user in fileName_Collection[targetFile]:
    #             if targetUser in target_user:
    #                 filePermission_Collection[targetFile].romove(target_user)
    #
    #         filePermission_Collection[targetFile].append({targetUser,permission_level})
    #         user_log[operator].append('you have given the user(' + targetUser + ') permission level_'+ permission_level +' of the file(' + targetFile + ')' )
    #         user_log[targetUser].append('you have been given the permission level_'+ permission_level +' of the file(' + targetFile + ') by the user(' + operator + ')')
    #
    #         return 'permission add success'
    #     else:
    #         return 'error'

@app.route('/deletePermission/<operator>/<targetFile>/<targetUser>',methods=['DELETE'])
def deletePermission(operator,targetFile,targetUser):
    if operator in get_root_user_of_the_file(targetFile):
        remove_permission_of_the_file(targetFile,targetUser)
        user_log[operator].append('you have cancelled the user(' + targetUser + ') permission of the file(' + targetFile + ')')
        user_log[targetUser].append('you have been cancelled the permission of the file(' + targetFile + ') by the user(' + operator + ')')
        return 'permission cancelled success'
    else:
        return 'error'
    # for user in filePermission_Collection[targetFile]:
    #     if operator in user and user[operator] == 0:
    #         filePermission_Collection[targetFile].remove(targetUser)
    #
    #         user_log[operator].append('you have cancelled the user(' + targetUser + ') permission of the file(' + targetFile + ')')
    #         user_log[targetUser].append('you have been cancelled the permission of the file(' + targetFile + ') by the user(' + operator + ')')
    #
    #         return 'permission delete success'
    #     else:
    #         return 'error'

@app.route('/getLog/<username>',methods=['GET'])
def getLog(username):
    return user_log[username]

if __name__ == '__main__':
    app.run(debug=True)
