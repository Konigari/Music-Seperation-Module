from flask import Flask, request, Response, send_file
import jsonpickle
import json
import base64
import io
import os
import logging

from config import Config

import redis

from minio import Minio

# initialize Flask application
app = Flask(__name__)

@app.route('/apiv1/test', methods=['GET'])
def test():
    return Response(response="Hi from server!", status=200, mimetype="application/json")

# define all routes of the application below
@app.route('/apiv1/separate', methods=['POST'])
def separate():

    mp3  = request.json['mp3']
    callback = request.json['callback']
    unique_id = str(hash(mp3))
    decode_mp3 = base64.b64decode(mp3)
    # minio_client.put_object('input', unique_id, io.BytesIO(decode_mp3), len(decode_mp3))
    adding_files_to_minio(decode_mp3,unique_id)
    # queue the data
    redis_instance.rpush("worker", unique_id)
    print(f'Pushed {unique_id} to the redis worker queue')

    # construct the response to the client
    response = {'Song Hash' : unique_id}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

def adding_files_to_minio(file_to_add,key_value):
    print(" bucket name is ",bucketname)
    # client.make_bucket(bucketname)
    if not client.bucket_exists(bucketname):
        print(f"Create bucket {bucketname}")
        client.make_bucket(bucketname)

    print(f"Objects in {bucketname} are originally:")
    for thing in client.list_objects(bucketname, recursive=True):
        print(thing.object_name)
        
    try:
        # print(type(file_to_add))
        # print(file_to_add)
        client.put_object('input', key_value, io.BytesIO(file_to_add), len(file_to_add))

    except:
        print("Error when adding files the first time")

    print(f"Objects in {bucketname} are now:")
    for thing in client.list_objects(bucketname, recursive=True):
        print(thing.object_name)


@app.route('/apiv1/queue', methods=['GET'])
def queue():
    if app.debug:
        log.debug(f"Received {request} on queue endpoint")

    # read the queued requests and return it to the client
    queued_requests = [ x.decode('utf-8') for x in redis_instance.lrange("worker", 0, -1) ]
    print(queued_requests)
    return Response(json.dumps(queued_requests), status=200, mimetype="application/json");
    

@app.route('/apiv1/get_track', methods=['GET'])
def get_track():
    if app.debug:
        log.debug(f"Received {request} on get track by id endpoint")

    track_id = request.args['track']

    # fetch from Minio using track id
    data = minio_client.get_object('output', track_id)

    return send_file(
        io.BytesIO(data.data),
        mimetype='audio/mpeg',
        as_attachment=True,
        download_name='%s.mp3' % track_id)


@app.route('/apiv1/remove', methods=['GET'])
def remove_track():
    if app.debug:
        print(f"Received {request} on remove track by id endpoint")

    track_id = request.args['track']
    # delete by track id
    minio_client.remove_object('output', track_id)
    response = {'Successfully removed the track!'}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    # setup logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)

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

    # log list of buckets
    buckets = minio_client.list_buckets()
    for bucket in buckets:
        print(f"Bucket {bucket.name}, created {bucket.creation_date}")

    # start the application
    app.run(host="0.0.0.0", port=Config.FLASK_PORT)