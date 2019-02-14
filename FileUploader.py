import os
from bottle import route, request, static_file, run

root_adress = 'http://localhost:8080'
root_path = '/home/nicolas/cloud/'
root_link_html = '<a href=" ' + root_adress + ' ">Back to the landing page</a> <br>'

@route('/')
def root():
    html = '<a href="' + root_adress + '/cloud/">Download</a> <br>'
    html += '<a href="' + root_adress + '/uploader/">Upload</a> <br>'
    return html


@route('/uploader/')
def load_uploader():
    return static_file('Upload.html', root='.')


@route('/upload', method='POST')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')

    save_path = root_path + "{category}".format(category=category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path) + '<br>' + root_link_html


@route('/cloud/')
def list_root():
    file_list = sort_filelist(root_path)
    file_list_html = root_link_html
    for entry in file_list:
        file_list_html += '<a href="' + root_adress + '/cloud/' + entry + '">' + entry + '</a> <br>'
    return file_list_html


@route('/cloud/<path:path>')
def try_dl(path):
    combined_path = root_path + path
    if os.path.isfile(combined_path):
        filename = os.path.basename(combined_path)
        return static_file(path, root=root_path, download=filename)
    else:
        file_list = sort_filelist(combined_path)
        file_list_html = root_link_html
        file_list_html += '<a href="' + root_adress + '/cloud/' + os.path.split(path)[0] + '">/.../</a> <br>'
        for entry in file_list:
            file_list_html += '<a href="' + root_adress + '/cloud/' + path + '/' + entry + '">' + entry + '</a> <br>'
        return file_list_html


def sort_filelist(path):
    dir_list = os.listdir(path)
    folders = []
    files = []
    for entry in dir_list:
        if os.path.isfile(path + entry):
            files.append(entry)
        else:
            folders.append(entry)
    return folders + files


if __name__ == '__main__':
    run(host='localhost', port=8080)
