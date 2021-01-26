import json
import numpy as np
from pathlib import Path
import glob

def get_image_filepath(jsonfile):
    a = jsonfile.split('/')[-1]
    b = jsonfile.replace(a, '') + '../img/'
    c = a.replace(".json", '')
    return c, b + c


def extract_info(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)

    img_name, imgfile = get_image_filepath(jsonfile)
    size = [data['size']['width'], data['size']['height']]
    filesize = Path(imgfile).stat().st_size

    objs = []
    for o in data['objects']:
        p = o['points']['exterior']
        # class_name, mins, maxs
        obj = [o['classTitle'], p[0][:], p[1][:]]
        objs.append(obj)

    print(objs, size)
    return size, objs, img_name, filesize


def create_vgg_format(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)

    img_name, imgfile = get_image_filepath(jsonfile)
    size = [data['size']['width'], data['size']['height']]
    filesize = Path(imgfile).stat().st_size

    if data['tags'][0]['name'] == "train":
        vgg = vgg_train
    else:
        vgg = vgg_val

    vgg[img_name+str(filesize)] = {
        "filename": img_name,
        "size": filesize,
        "regions": {
        }
    }

    objs = []
    for o in data['objects']:
        if o['classTitle'] != "bg":
            p = o['points']['exterior']
            # class_name, mins, maxs
            region = {
                "shape_attributes": {
                    "name": "rect",
                    "x": int(p[0][0]),
                    "y": int(p[0][1]),
                    "width": int(p[1][0] - p[0][0]),
                    "height": int(p[1][1] - p[0][1])
                },
                "region_attributes": {"name": o['classTitle']}
            }
            objs.append(region)

    vgg[img_name+str(filesize)]["regions"] = objs

def compute_bboxs(size, objs, relative=True, format='normal'):
    # TODO account for all the possible objects
    idx = None
    for i, o in enumerate(objs):
        if o[0] == 'workspace':
            idx = i
            break
    obj_bbox = objs[idx][1:]
    print(objs[idx])
    xmin = float(obj_bbox[0][0]) / float(size[0]) if relative else float(obj_bbox[0][0])
    xmax = float(obj_bbox[1][0]) / float(size[0]) if relative else float(obj_bbox[1][0])
    ymin = float(obj_bbox[0][1]) / float(size[1]) if relative else float(obj_bbox[0][1])
    ymax = float(obj_bbox[1][1]) / float(size[1]) if relative else float(obj_bbox[1][1])

    if format == 'normal':
        return np.array([xmin, ymin, xmax, ymax], dtype=np.float32)
    elif format == 'tf':
        return np.array([[ymin, xmin, ymax, xmax]], dtype=np.float32)
    else:
        pass

vgg_train = dict()
vgg_val = dict()
file_list = glob.glob("/media/cambel/Extra/research/fujifilm/endoscope-human/bbox-dataset/pipe-coating-train2_001/ds0/ann/*.json")
file_list = glob.glob("/media/cambel/Extra/research/fujifilm/endoscope-human/bbox-dataset/pipe_realsense/ds0/ann/*.json")
file_list = glob.glob("/media/cambel/Extra/research/fujifilm/endoscope-human/bbox-dataset/pipe-train-final/ds0/ann/*.json")
file_list = glob.glob("/root/dev/object_detection/assembly_manuals_train/ds0/ann/*.json")
for filename in file_list:
# filename = '/media/cambel/Extra/research/fujifilm/endoscope-human/bbox-dataset/pipe-coating-train2_001/ds0/ann/phone-001.png.json'
    create_vgg_format(filename)

with open('vgg_train.json', 'w') as json_file:
    json.dump(vgg_train, json_file)

with open('vgg_val.json', 'w') as json_file:
    json.dump(vgg_val, json_file)
# s, o, _ = extract_info(filename)
# print(compute_bboxs(s, o))
