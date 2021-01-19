# -*- -——coding: utf-8 -*-
"""
Created on  11:13:37 2021-01-13

@author: wei
"""


# 标注时带图片ImageData信息

import os
import json
import numpy as np
import glob
import shutil
from sklearn.model_selection import train_test_split
import utils
 
np.random.seed(41)
 
#0为背景
classname_to_id = {"car": 1,"bic":2,"per":3}
 
class Lableme2CoCo:
 
    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
 
    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # indent=2 更加美观显示
 
    # 由json文件构建COCO
    def to_coco(self, json_path_list):
        self._init_categories()
        for json_path in json_path_list:
            obj = self.read_jsonfile(json_path)
            self.images.append(self._image(obj, json_path))
            shapes = obj['shapes']
            for shape in shapes:
                annotation = self._annotation(shape)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance
 
    # 构建类别
    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)
 
    # 构建COCO的image字段
    def _image(self, obj, path):
        image = {}
 
        img_x = utils.img_b64_to_arr(obj['imageData'])
        h, w = img_x.shape[:-1]
        image['height'] = h
        image['width'] = w
        image['id'] = self.img_id
        image['file_name'] = os.path.basename(path).replace(".json", ".jpg")
        return image
 
    # 构建COCO的annotation字段
    def _annotation(self, shape):
        label = shape['label']
        points = shape['points']
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = int(classname_to_id[label])
        annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = annotation['bbox'][-1]*annotation['bbox'][-2]
        return annotation
 
    # 读取json文件，返回一个json对象
    def read_jsonfile(self, path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
 
    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return [min_x, min_y, max_x - min_x, max_y - min_y]
 
 
if __name__ == '__main__':
    #将一个文件夹下的照片和labelme的标注文件，分成了train和val的coco json文件和照片
    labelme_path = '/EVEN/test/mmdetection-2.8.0/untils/data/lableme'
    train_img_out_path='/EVEN/test/mmdetection-2.8.0/untils/data/lableme/train_img'
    val_img_out_path = '/EVEN/test/mmdetection-2.8.0/untils/data/lableme/val_img'
    if not (os.path.exists(train_img_out_path) and os.path.exists(val_img_out_path)):
        os.mkdir(train_img_out_path)
        os.mkdir(val_img_out_path)
 
    # 获取images目录下所有的joson文件列表
    json_list_path = glob.glob(labelme_path + "/*.json")
    print('json_list_path=', json_list_path)
    # 数据划分,这里没有区分val2017和tran2017目录，所有图片都放在images目录下
    train_path, val_path = train_test_split(json_list_path, test_size=0.5)
    print("train_n:", len(train_path), 'val_n:', len(val_path))
    print('train_path=',train_path)
    # 把训练集转化为COCO的json格式
    l2c_train = Lableme2CoCo()
    train_instance = l2c_train.to_coco(train_path)
    l2c_train.save_coco_json(train_instance, '/EVEN/test/mmdetection-2.8.0/untils/data/lableme/train.json')
 
    # 把验证集转化为COCO的json格式
    l2c_val = Lableme2CoCo()
    val_instance = l2c_val.to_coco(val_path)
    l2c_val.save_coco_json(val_instance, '/EVEN/test/mmdetection-2.8.0/untils/data/lableme/val.json')
 
 
    for file in train_path:
        shutil.copy(file.replace("json",'jpg'),train_img_out_path)
    for file in val_path:
        shutil.copy(file.replace("json",'jpg'),val_img_out_path)

        

# 标注时图片不带ImageData信息
# import os
# import json
# import numpy as np
# import glob
# import shutil
# from sklearn.model_selection import train_test_split
# from labelme import utils
# import cv2
 
# np.random.seed(41)
 
# # 0为背景
# classname_to_id = {"person": 1,"bus": 6}
 
# class Lableme2CoCo:
 
#     def __init__(self):
#         self.images = []
#         self.annotations = []
#         self.categories = []
#         self.img_id = 0
#         self.ann_id = 0
 
#     def save_coco_json(self, instance, save_path):
#         json.dump(instance, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # indent=2 更加美观显示
 
#     # 由json文件构建COCO
#     def to_coco(self, json_path_list):
#         self._init_categories()
#         for json_path in json_path_list:
#             obj = self.read_jsonfile(json_path)
#             self.images.append(self._image(obj, json_path))
#             shapes = obj['shapes']
#             for shape in shapes:
#                 annotation = self._annotation(shape)
#                 self.annotations.append(annotation)
#                 self.ann_id += 1
#             self.img_id += 1
#         instance = {}
#         instance['info'] = 'spytensor created'
#         instance['license'] = ['license']
#         instance['images'] = self.images
#         instance['annotations'] = self.annotations
#         instance['categories'] = self.categories
#         return instance
 
#     # 构建类别
#     def _init_categories(self):
#         for k, v in classname_to_id.items():
#             category = {}
#             category['id'] = v
#             category['name'] = k
#             self.categories.append(category)
 
#     # 构建COCO的image字段
#     def _image(self, obj, path):
#         image = {}
#         img_path = path.replace(".json", ".jpg")
#         # img_x = utils.img_b64_to_arr(obj['imageData'])
#         # h, w = img_x.shape[:-1]
#         # print("img_path:",img_path)
#         img_x = cv2.imread(img_path)
#         h, w = img_x.shape[:-1]
#         image['height'] = h
#         image['width'] = w
#         image['id'] = self.img_id
#         image['file_name'] = os.path.basename(path).replace(".json", ".jpg")
#         return image
 
#     # 构建COCO的annotation字段
#     def _annotation(self, shape):
#         label = shape['label']
#         points = shape['points']
#         annotation = {}
#         annotation['id'] = self.ann_id
#         annotation['image_id'] = self.img_id
#         annotation['category_id'] = int(classname_to_id[label])
#         annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
#         annotation['bbox'] = self._get_box(points)
#         annotation['iscrowd'] = 0
#         annotation['area'] = annotation['bbox'][-1] * annotation['bbox'][-2]
#         return annotation
 
#     # 读取json文件，返回一个json对象
#     def read_jsonfile(self, path):
#         with open(path, "r", encoding='utf-8') as f:
#             return json.load(f)
 
#     # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
#     def _get_box(self, points):
#         min_x = min_y = np.inf
#         max_x = max_y = 0
#         for x, y in points:
#             min_x = min(min_x, x)
#             min_y = min(min_y, y)
#             max_x = max(max_x, x)
#             max_y = max(max_y, y)
#         return [min_x, min_y, max_x - min_x, max_y - min_y]
 
 
# if __name__ == '__main__':
#     # 将一个文件夹下的照片和labelme的标注文件，分成了train和val的coco json文件和照片
#     labelme_path = './data'
#     train_img_out_path = './train_img'
#     val_img_out_path = './val_img'
#     if not (os.path.exists(train_img_out_path) and os.path.exists(val_img_out_path)):
#         os.mkdir(train_img_out_path)
#         os.mkdir(val_img_out_path)
 
#     # 获取images目录下所有的joson文件列表
#     json_list_path = glob.glob(labelme_path + "/*.json")
#     print('json_list_path=', json_list_path)
#     # 数据划分,这里没有区分val2017和tran2017目录，所有图片都放在images目录下
#     train_path, val_path = train_test_split(json_list_path, test_size=0)
#     print("train_n:", len(train_path), 'val_n:', len(val_path))
#     print('train_path=', train_path)
#     # 把训练集转化为COCO的json格式
#     l2c_train = Lableme2CoCo()
#     train_instance = l2c_train.to_coco(train_path)
#     l2c_train.save_coco_json(train_instance, 'train.json')
 
#     # 把验证集转化为COCO的json格式
#     l2c_val = Lableme2CoCo()
#     val_instance = l2c_val.to_coco(val_path)
#     l2c_val.save_coco_json(val_instance, 'val.json')
 
#     for file in train_path:
#         shutil.copy(file.replace("json", "jpg"), train_img_out_path)
#     for file in val_path:
#         shutil.copy(file.replace("json",  "jpg"), val_img_out_path)



