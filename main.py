import librosa
import os
import soundfile as sf
import numpy as np
import shutil  

def get_oto(path, coding):
    oto = open(path, 'r', encoding=coding)
    oto = oto.readlines()
    oto_len = len(oto)
    otolist = []
    for i in range(oto_len):
        try:
            otolist.append(oto[i].split('\n'))
            del otolist[i][-1]
        except:
            pass
    del otolist[-1]
    return otolist    
def get_value(otolist):
    values = []
    for i in range(len(otolist)):
        #这个是获取文件名的
        file=otolist[i][0]
        index = file.find('=')
        file = file[:index]
        #这个是获取别名的
        alias=otolist[i][0]
        index = alias.find('=')
        alias = alias[index + 1:]
        comma_index = alias.find(',')
        alias = alias[:comma_index]
        #这个是获取后面数据的
        a,b,c,d,e=0,0,0,0,0
        vl=otolist[i][0]
        index=vl.find(',')
        vl=vl[index+1:]
        vl=vl.split(',')
        a=vl[0]
        b=vl[1]
        c=vl[2]
        d=vl[3]
        e=vl[4]
        #数据准备，只欠写入！！！！
        values.append([file,alias,a,b,c,d,e])
    return values
def find_wrong_oto(values, path):
    wrong_oto = []
    tmp_dir = os.path.join(path, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)  # 创建临时目录

    for i, value in enumerate(values):
        file, alias = value[0], value[1]
        try:
            # 获取音频时长
            audio_path = os.path.join(path, file)
            audio_data, sr = librosa.load(audio_path)
            duration = len(audio_data) / sr * 1000
            print(audio_path)
            print(f"音频时长: {duration} 毫秒")

            # Offset 检查
            offset = float(value[2])
            if offset < 0:
                wrong_oto.append(f"{file}:{alias}的Offset错误")
                print(f"{file}的Offset错误")
            else:
                print(f"{file}的Offset正确,继续检查其他参数")

            # cutoff 检查
            cutoff = float(value[4])
            # 截取音节
            start_sample = int(offset * sr / 1000)
            end_sample = int((duration - cutoff) * sr / 1000)
            # 直接在内存中处理，不写入文件
            cut_audio_data = audio_data[start_sample:end_sample]
            duration_cut = len(cut_audio_data) / sr * 1000
            if duration_cut < 20:
                wrong_oto.append(f"{file}:{alias}的音节太短了")
                print(f"{alias}的音节太短了，你猜猜它为啥没声？如果你这是连续音更离谱！！！！！")
            else:
                print(f"{alias}的音节正确,继续检查其他参数")

            # 截取重叠音
            end_sample = int(float(value[3]) * sr / 1000)
            cut_audio_data = audio_data[start_sample:end_sample]
            # 判断声音是否太小
            if np.max(cut_audio_data) < 0.0001:
                wrong_oto.append(f"{file}:{alias}的重叠音太小了")
                print(f"{alias}的重叠音太小了")

        except Exception as e:
            pass

    # 删除临时目录
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)  # 使用 shutil.rmtree 更方便地删除目录

    return wrong_oto

def main():
    path = input('请输入包含wav文件的音源文件的路径(格式：C:\\Users\\xxx\\Desktop\\xxx)：')
    oto=input('请输入ini文件的路径：')
    coding = input('请输入ini文件的编码：')  
    try:
        oto_list = get_oto(oto, coding)
        values = get_value(oto_list)
        wrongs = find_wrong_oto(values, path)
        os.system('cls')
        if not wrongs:
            print('没有错误')
        else:
            print(f'错误的有{len(wrongs)}个：') 
            for wrong in wrongs:
                print(wrong)
    except Exception as e:
        pass
    finally:
        os.system('pause')

if __name__ == '__main__':
    main()