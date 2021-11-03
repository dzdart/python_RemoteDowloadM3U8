# -*- coding: utf-8 -*-
import glob
import json
import os
import threading

from flask import Flask, render_template, request, make_response, send_from_directory

from Web.Public_funcation import L_json, DM3U8, GetID, conf

# ————————————————————#
work_dir = conf().conf_data['work_dir']
run_port = conf().conf_data['run_port']
last_dir = conf().conf_data['last_save']

if work_dir == '':
    work_dir = os.getcwd()
if run_port == '':
    run_port == 8090
else:
    try:
        run_port = int(run_port)
    except:
        run_port = 8090


# ————————————————————#

def create_task(task_list):
    L_J = L_json()
    while True:
        if len(task_list) > 0:
            tmp_task = task_list.pop(0)
            id = tmp_task[0]
            url = tmp_task[1]
            save_dir = tmp_task[2]
            save_name = tmp_task[3]
            print('开始任务')
            threading.Thread(target=DM3U8, args=[id, url, save_dir, save_name]).start()
            L_J.add(task_id=id, name=save_name, save_path=save_dir, save_bool=False, save_progress=0)


app = Flask(__name__)
task_list = []


@app.route('/')
def index():
    tmp_task_list = ''
    data = L_json().data
    for key in data.keys():
        tmp_task_list += render_template('task_enum.html',
                                         name=json.loads(data[key])['name'],
                                         url='/dd?id=' + key,
                                         )
    ret = render_template('download.html', work_dir=work_dir, task_list=tmp_task_list, last_save=last_dir)
    return ret


@app.route('/d', methods=['GET', 'POST'])
def c_d():
    id = GetID()
    m3u8_url = request.form.get('m3u8_url')
    # savr_dir = work_dir+'\\'+request.form.get('save_dir')
    saver_dir = os.sep.join([work_dir, request.form.get('save_dir')])
    save_name = request.form.get('save_name')
    tmp_args = [id, m3u8_url, saver_dir, save_name]
    task_list.append(tmp_args)
    return id


@app.route('/check', methods=['GET', 'POST'])
def check():
    d_bt = 'disabled="disabled"'
    dd_url = './dd?'
    L_J = L_json()
    check_id = request.form.get('id')
    try:
        tmp_data = L_J.get(check_id)

        if tmp_data['save_bool'] == 'True':
            d_bt = ''
            dd_url = dd_url + 'id=' + check_id
            path_file_number = tmp_data['save_progress']
        else:
            path_file = tmp_data['save_path'] + '\\' + tmp_data['name'] + '\\*.ts'
            path_file_number = str(len(glob.glob(pathname=path_file)))

        ret = render_template('check.html', video_name=tmp_data['name'],
                              video_bool=tmp_data['save_bool'],
                              video_progress=path_file_number + '\\' + tmp_data['save_progress'],
                              bt_bool=d_bt,
                              d_url=dd_url)
    except KeyError:
        ret = 'ID不存在！请检查'
    return ret


@app.route('/dd', methods=['GET'])
def get_file():
    gf_tmpdata = L_json().get(task_id=request.args.get('id'))
    d_dir = os.path.dirname(gf_tmpdata['save_path'])
    file_name = os.path.basename(gf_tmpdata['save_path'])
    ret_file_name = gf_tmpdata['name'] + '.' + file_name.split('.')[-1]

    try:
        response = make_response(
            send_from_directory(d_dir, file_name, as_attachment=True, attachment_filename=ret_file_name))
        return response
    except Exception as e:
        ret = '404 not found:请求的文件不存在：请主动检查数据库。'
        return ret


if __name__ == "__main__":
    # 运行这个服务器
    threading.Thread(target=create_task, args=[task_list]).start()
    app.run(host='127.0.0.1', port=run_port, debug=True)
