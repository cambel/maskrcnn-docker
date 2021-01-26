import xmltodict
import pprint
import random
import json
import glob


def load_xml(filename):
    with open(filename, 'r') as xml_file:
        dict_data = xmltodict.parse(xml_file.read())
    return dict_data


def fill_obj(obj):
    return {"id": random.randint(500000000, 599999999),
            "classId": clss.get(obj["name"]),
            "description": "",
            "geometryType": "rectangle",
            "labelerLogin": "cambel07",
            "createdAt": "2020-12-16T08:40:08.266Z",
            "updatedAt": "2020-12-16T08:40:11.370Z",
            "tags": [],
            "classTitle": obj["name"],
            "points": {
        "exterior": [
            [
                float(obj['bndbox']['xmin']),
                float(obj['bndbox']['ymin'])
            ],
            [
                float(obj['bndbox']['xmax']),
                float(obj['bndbox']['ymax'])
            ]
        ],
        "interior": []
    }}


def to_supervisely(data):
    ann = {
        "description": "",
        "tags": [],
        "size": {
            "height": float(data["annotation"]["size"]["height"]),
            "width":  float(data["annotation"]["size"]["width"])
        },
    }
    objects = []
    if isinstance(data['annotation']['object'], list):
        for obj in data['annotation']['object']:
            objects.append(fill_obj(obj))
    else:
        objects.append(fill_obj(data['annotation']['object']))
    ann["objects"] = objects
    return ann


target_folder = "/home/cambel/dev/object_detection/datasets/assembly_manuals/ds0/ann/"
file_list = glob.glob("/home/cambel/dev/object_detection/datasets/1220assembly_manuals-PascalVOC-export/Annotations/*.xml")

with open("object_detection/datasets/assembly_manuals/meta.json") as f:
    metadata = json.load(f)

clss = {}
for classes in metadata["classes"]:
    clss[classes['title']] = classes['id']

for filepath in file_list:
    print(filepath)
    data = load_xml(filepath)
    res = to_supervisely(data)
    filename = filepath.split('/')[-1].replace(".xml", '.jpg.json')
    with open(target_folder+filename, 'w') as json_file:
        json.dump(res, json_file)
