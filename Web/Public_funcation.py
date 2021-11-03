import json
import math
import os
import random
import string
import threading
import time
from multiprocessing import cpu_count
from shutil import rmtree

import requests


class L_json:
    def __init__(self):
        self.data_path = os.getcwd() + '\\templates\\data.json'
        self.data = {}
        self.data_read()


    def data_read(self):
        data = open(self.data_path, 'rb').read()
        if not data == b'':
            # data = base64.b64decode(data).decode('utf-8')
            self.data = json.loads(data)
        else:
            print('表空！')
        return self.data

    def data_write(self):
        tmp_data = json.dumps(self.data)
        tmp_data = tmp_data.encode('utf-8')
        # tmp_data = base64.b64encode(tmp_data)
        with open(self.data_path, 'wb+') as f:
            f.write(tmp_data)

    def add(self, task_id, name, save_path, save_bool, save_progress):
        tmp_id = str(task_id)
        tmp_dic = {}
        tmp_dic['name'] = name
        tmp_dic['save_path'] = save_path
        tmp_dic['save_bool'] = save_bool
        tmp_dic['save_progress'] = save_progress
        tmp_data = json.dumps(tmp_dic)
        self.data[tmp_id] = tmp_data
        self.data_write()

    def get(self, task_id):
        get_tmpdata = self.data[task_id]
        get_tmpdata = str(get_tmpdata).replace('\'', '"')
        return json.loads(get_tmpdata)

    def up(self, task_id, name='', save_path='', save_bool='', save_progress=''):
        tmp_data = self.get(task_id)
        if not name == '':
            tmp_data['name'] = name
        if not save_path == '':
            tmp_data['save_path'] = save_path
        if not save_bool == '':
            tmp_data['save_bool'] = save_bool
        if not save_progress == '':
            tmp_data['save_progress'] = save_progress
        self.data[task_id] = json.dumps(tmp_data)
        self.data_write()

    def clear(self):
        self.data.clear()
        self.data_write()
        print('表已经清空！')


class DM3U8:
    def __init__(self, id: str, url: str, save_dir: str, save_name: str):
        self.url = url
        self.save_dir = save_dir
        self.tmp_dir = ''
        self.save_name = save_name
        self.id = id
        self.ts_path_list = []
        self.m3u8_data = []
        self.father_url = ''
        self.check_path()
        self.make_father_url()
        self.d_m3()
        self.start_thread()

    def check_path(self):
        """
        检查存储目录是否存在，不存在就创建
        """
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def make_father_url(self):
        self.father_url = self.url.replace(self.url.split('/')[-1], '')

    def d_m3(self):
        tmp_data = requests.get(self.url).content.decode('utf-8').split('\n')
        for item in tmp_data:
            if item.find('.ts') > 0:
                self.m3u8_data.append(self.father_url + item)
        L_json().up(task_id=self.id,save_progress=str(len(self.m3u8_data)))

    def d_ts(self, task_list):
        error_list = []
        for item in task_list:
            self.tmp_dir = self.save_dir + '\\' + str(self.save_name)
            if not os.path.exists(self.tmp_dir):
                os.makedirs(self.tmp_dir)
            save_path = self.save_dir + '\\' + str(self.save_name) + '\\' + str(item).split('/')[-1]
            print(save_path)
            try:
                tmp_data = requests.get(item, timeout=20).content
                with open(save_path, 'wb') as f:
                    f.write(tmp_data)
                    f.flush()
                    f.close()
                    self.ts_path_list.append(save_path)
                # print(str(item).split('/')[-1], '下载完成\n')
            except requests.exceptions.RequestException:
                error_list.append(item)
        if len(error_list) > 0:
            print(len(error_list), '个下载超时，正在重试')
            self.d_ts(error_list)

    def make_mp4(self):
        print('开始合并MP4')
        ffmpeg_path = os.getcwd() + '\\ffmpeg.exe'
        self.ts_path_list.sort()
        ts_list = self.ts_path_list
        ts_command = '\"concat:'
        for item in ts_list:
            ts_command = ts_command + str(item) + '|'
        ts_command = ts_command + '\"'
        mp4_path = self.save_dir + '\\' + str(self.id) + str(self.save_name) + '.mp4'
        if os.path.exists(mp4_path):
            os.remove(mp4_path)
        cmd = ffmpeg_path + ' -i ' + ts_command + ' -c copy ' + mp4_path
        os.system(cmd)
        for item in ts_list:
            os.remove(item)
        L_json().up(task_id=str(self.id), save_path=mp4_path, save_bool='True', save_progress='100')
        print('合并完成')

    def readonly_handler(func, path, execinfo):
        os.chmod(path, os.stat.S_IWRITE)
        func(path)

    def start_thread(self):
        thread_list = []
        task_list = []
        lin_num = cpu_count() * 2
        print(lin_num)
        task_num = math.ceil(len(self.m3u8_data) / lin_num)
        for i in range(lin_num):
            task_star, task_end = [int(i * task_num), int((i + 1) * task_num)]
            if task_end > len(self.m3u8_data):
                task_end = len(self.m3u8_data)

            task_list.append(self.m3u8_data[task_star: task_end])
        for item in task_list:
            a_t = threading.Thread(target=self.d_ts, args=[item])
            a_t.start()
            thread_list.append(a_t)
        for t in thread_list:
            t.join()
        self.make_mp4()
        time.sleep(1)
        rmtree(self.tmp_dir, onerror=self.readonly_handler)


class conf:
    def __init__(self):
        self.conf_data = {}
        self.red()

    def red(self):
        self.conf_data = json.loads(open('config.json', 'r').read())

    def up(self, *args):
        """

        :param args: 每一对变量使用=连接
        :return:
        """
        for item in args:
            item = str(item).split('=')
            for item1 in self.conf_data.keys():
                if item[0] == str(item1):
                    self.conf_data[item1] = item[1]
        tmp_data = json.dumps(self.conf_data)
        print(tmp_data)
        open('config.json', 'w+').write(tmp_data)


def GetID(length=10):
    # 随机出数字的个数
    numOfNum = random.randint(1, length - 1)
    numOfLetter = length - numOfNum
    # 选中numOfNum个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    # 选中numOfLetter个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    # 打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    # 生成密码
    ID = ''.join([i for i in slcChar])
    return ID
