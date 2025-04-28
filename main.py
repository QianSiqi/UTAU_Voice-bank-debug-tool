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
        #����ǻ�ȡ�ļ�����
        file=otolist[i][0]
        index = file.find('=')
        file = file[:index]
        #����ǻ�ȡ������
        alias=otolist[i][0]
        index = alias.find('=')
        alias = alias[index + 1:]
        comma_index = alias.find(',')
        alias = alias[:comma_index]
        #����ǻ�ȡ�������ݵ�
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
        #����׼����ֻǷд�룡������
        values.append([file,alias,a,b,c,d,e])
    return values
def find_wrong_oto(values, path):
    wrong_oto = []
    tmp_dir = os.path.join(path, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)  # ������ʱĿ¼

    for i, value in enumerate(values):
        file, alias = value[0], value[1]
        try:
            # ��ȡ��Ƶʱ��
            audio_path = os.path.join(path, file)
            audio_data, sr = librosa.load(audio_path)
            duration = len(audio_data) / sr * 1000
            print(audio_path)
            print(f"��Ƶʱ��: {duration} ����")

            # Offset ���
            offset = float(value[2])
            if offset < 0:
                wrong_oto.append(f"{file}:{alias}��Offset����")
                print(f"{file}��Offset����")
            else:
                print(f"{file}��Offset��ȷ,���������������")

            # cutoff ���
            cutoff = float(value[4])
            # ��ȡ����
            start_sample = int(offset * sr / 1000)
            end_sample = int((duration - cutoff) * sr / 1000)
            # ֱ�����ڴ��д�����д���ļ�
            cut_audio_data = audio_data[start_sample:end_sample]
            duration_cut = len(cut_audio_data) / sr * 1000
            if duration_cut < 20:
                wrong_oto.append(f"{file}:{alias}������̫����")
                print(f"{alias}������̫���ˣ���²���Ϊɶû������������������������ף���������")
            else:
                print(f"{alias}��������ȷ,���������������")

            # ��ȡ�ص���
            end_sample = int(float(value[3]) * sr / 1000)
            cut_audio_data = audio_data[start_sample:end_sample]
            # �ж������Ƿ�̫С
            if np.max(cut_audio_data) < 0.0001:
                wrong_oto.append(f"{file}:{alias}���ص���̫С��")
                print(f"{alias}���ص���̫С��")

        except Exception as e:
            pass

    # ɾ����ʱĿ¼
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)  # ʹ�� shutil.rmtree �������ɾ��Ŀ¼

    return wrong_oto

def main():
    path = input('���������wav�ļ�����Դ�ļ���·��(��ʽ��C:\\Users\\xxx\\Desktop\\xxx)��')
    oto=input('������ini�ļ���·����')
    coding = input('������ini�ļ��ı��룺')  
    try:
        oto_list = get_oto(oto, coding)
        values = get_value(oto_list)
        wrongs = find_wrong_oto(values, path)
        os.system('cls')
        if not wrongs:
            print('û�д���')
        else:
            print(f'�������{len(wrongs)}����') 
            for wrong in wrongs:
                print(wrong)
    except Exception as e:
        pass
    finally:
        os.system('pause')

if __name__ == '__main__':
    main()