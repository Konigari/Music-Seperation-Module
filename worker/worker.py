import os
from config import Config
import redis
from minio import Minio
from os import listdir
import io


def listen():
    print('Inside listen function...')
    while True:
        mp3_hash = redis_instance.blpop("worker")
        decoded_hash = mp3_hash[1].decode('utf-8')

        print("Retrieving the song from Minio... : ", decoded_hash)
        data = minio_client.get_object('input', decoded_hash)

        # write the data as an mp3 file into /data/input folder
        input_folder = '/data/input/'
        output_folder = '/data/output/'
        filename = f'temp{(decoded_hash)%1000}'

        with open(f"{input_folder}{filename}.mp3", "wb") as f:
            for d in data.stream(32*1024):
                f.write(d)

        cmd = f'python3 -m demucs.separate --mp3 --out {output_folder} {input_folder}{filename}.mp3'
        print('Executing demucs...')
        os.system(cmd)
        print('Completed demucs on the song')

        print('Writing the output of demucs into minio bucket')
        # # write the contents from /data/output/{filename} to the Minio output bucket
        outputPath = f"{output_folder}mdx_extra_q/{filename}/"
        # /data/output/mdx_extra_q/temp727

        for file in listdir(outputPath):
            print('File name : ', outputPath+file)
            file_data = open(outputPath+file, "rb").read()
            minio_client.put_object('output', f'mp3_hash{file}', io.BytesIO(file_data), len(file_data))

        print('Completed the copying of separated mp3 files into minio')

if __name__ == '__main__':
    
    # initialize the redis instance
    redis_instance = redis.Redis(host=Config.REDIS_SERVICE_HOST, port=Config.REDIS_SERVICE_PORT)

    # initialize the minio client for object storage and retrieval
    minio_host = f"{Config.MINIO_SERVICE_HOST}:{Config.MINIO_SERVICE_PORT}"
    minio_user = Config.MINIO_USER
    minio_passwd = Config.MINIO_PASSWD

    minio_client = Minio(minio_host,
                secure=False,
                access_key=minio_user,
                secret_key=minio_passwd)

    # test one mp3 file
    # print('Testing one mp3 file')
    # os.system('python3 -m demucs.separate --mp3 --out /data/output /data/input/short-hop.mp3')
    # print('Tested one mp3 file')

    print("Listenting to the worker queue...")
    listen()