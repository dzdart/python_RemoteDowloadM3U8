import math
import os
import threading
from multiprocessing import cpu_count
import requests
from Main import L_json


class DM3U8:
    def __init__(self,id:str, url: str, save_dir: str, save_name: str):
        self.url = url
        self.save_dir = save_dir
        self.save_name = save_name
        self.id=id
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

    def d_ts(self, task_list):
        error_list = []
        for item in task_list:
            save_path = self.save_dir + '\\' + str(item).split('/')[-1]
            try:
                tmp_data = requests.get(item, timeout=20).content
                with open(save_path, 'wb') as f:
                    f.write(tmp_data)
                    f.flush()
                    f.close()
                    self.ts_path_list.append(save_path)
                print(str(item).split('/')[-1], '下载完成\n')
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
        mp4_path=self.save_dir+'\\'+str(self.save_name)
        cmd = ffmpeg_path + ' -i ' + ts_command + ' -c copy ' + mp4_path + '.mp4'
        os.system(cmd)
        for item in ts_list:
            os.remove(item)
        L_json.add(id=self.id,name=self.save_name,save_path=mp4_path,save_bool=True,save_progress=100)
        print('合并完成')

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


if __name__ =='__main__':
    url = 'https://t10.cdn2020.com:12335/video/m3u8/2021/07/29/da6f972b/index.m3u8'
    #url = 'http://localhost/dd/index.m3u8'
    DM3U8(url=url, save_dir='F:\\tmp1111', save_name='aaa')
