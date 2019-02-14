import os
from bottle import route, request, static_file, run

root_adress = 'http://localhost:8080'
root_path = '/home/nicolas/cloud/'

@route('/')
def root():
    return static_file('Upload.html', root='.')

@route('/upload', method='POST')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)

    save_path = "/tmp/{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)


@route('/cloud/')
def list_root():
    file_list = sort(os.listdir(combined_path))
    file_list_html = ""
    for entry in os.listdir(root_path):
        file_list_html += '<a href="' + root_adress + '/cloud/' + entry + '">' + entry + '</a> <br>'
    return file_list_html

@route('/cloud/<path:path>')
def try_dl(path):
    combined_path = root_path + path
    if os.path.isfile(combined_path):
        filename = os.path.basename(combined_path)
        return static_file(path, root=root_path, download=filename)
    else:
        file_list = sort(os.listdir(combined_path))
        file_list_html = "";
        for entry in file_list:
            file_list_html += '<a href="' + root_adress + '/cloud/' + path + '/' + entry + '">' + entry + '</a> <br>'
        return file_list_html



if __name__ == '__main__':
    run(host='localhost', port=8080)