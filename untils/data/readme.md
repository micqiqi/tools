# -*- -——coding: utf-8 -*-
"""
Created on  11:13:37 2021-01-13

@author: wei
"""

COCO数据集解析（Common Objects in Context）

2014：训练集 + 验证集 + 测试集
2015：测试集
2017：训练集 + 验证集 + 测试集
details：./knowledgeimage/coco.jpg

目标检测与实例分割、人体关键点检测、材料识别、全景分割、图像描述

以“2014 Train/Val annotations”标注文件为例，
包括三类文件：
    captions为图像描述的标注文件、
    instances为目标检测与实例分割的标注文件、
    person_keypoints为人体关键点检测的标注文件
详见 coco结构0.jpg
字典数据结构，包括以下5个key-value对。其中info、images、licenses三个key是三种类型标注文件共享的，最后的annotations和categories按照不同的任务有所不同

详见  coco结构1.jpg
        {
            "info": {
                "description": "COCO 2017 Dataset",
                "url": "http://cocodataset.org",
                "version": "1.0",
                "year": 2017,
                "contributor": "COCO Consortium",
                "date_created": "2017/09/01"
            },
            "licenses": [
                {
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                    "id": 1,
                    "name": "Attribution-NonCommercial-ShareAlike License"
                },
                {
                    "url": "http://creativecommons.org/licenses/by-nc/2.0/",
                    "id": 2,
                    "name": "Attribution-NonCommercial License"
                },
                ...(太长，省略)
            ],    "categories": [        {            "supercategory": "person",            "id": 1,            "name": "person"        },        ...(太长，省略)    ],
            "images": [
                {
                    "license": 2,
                    "file_name": "000000000049.jpg",
                    "coco_url": "http://images.cocodataset.org/train2017/000000000049.jpg",
                    "height": 500,
                    "width": 381,
                    "date_captured": "2013-11-14 20:00:23",
                    "flickr_url": "http://farm4.staticflickr.com/3250/2883102207_bcba5527a7_z.jpg",
                    "id": 49
                }
            ],
            "annotations": [
                {
                    "segmentation": [
                        [
                            181.59,
                            363.43,
                            ...(太长，省略)
                        ]
                    ],
                    "area": 8451.22405,
                    "iscrowd": 0,
                    "image_id": 49,
                    "bbox": [
                        162.57,
                        226.56,
                        130.41,
                        184.43
                    ],
                    "category_id": 19,
                    "id": 56407
                },
                 ...(太长，省略)   
            ]
        }

（一）info字段：包括下图中的内容，很好理解，这里就不赘述了  详见 coco结构2.jpg
    info这个key指向的字典是一些基本信息，包括时间，版本，贡献者，网址链接等不重要，可以忽略。
（二）licenses字段：包括下图中的内容，里面集合了不同类型的licenses，并在images中按照id号被引用，基本不参与到数据解析过程中。 详见 coco结构3.jpg
    License这个key指向的信息也可以忽略不计
（三）images字段：包括下图中的内容，对应了每张图片的详细信息，其中的id号是被分配的唯一id 详见  coco结构4.jpg
    images字段列表元素的长度等同于划入训练集（或者测试集）的图片的数量；
    key指向的列表（注意是列表，上面info指向的是字典）是图片信息，列表中的每一个字典下存储一张图片的信息，license、coco_url、data_captured和flickr_url这几个key指向的信息大概了解下就行，在你已经下载到原图jpg文件的情况下，这些信息基本没用。接下来就是比较重要的几个信息了，首先是file_name，指向的是一个字符串，是jpg的文件名；其次是height和width指向的是该图片的高和宽，id指向的数字可能让大家比较迷惑，这个信息非常至关键，这一串数字是每张图片特有的一个标志，数字不重复，可以看作是图片的身份信息，就像身份证那一串数字一样。


（四）categories字段：包括下图中的内容。其中supercategory是父类，name是子类，id是类别id（按照子类统计）。比如下图中所示的。coco数据集共计有80个类别（按照name计算的） 详见 coco结构5.jpg
    categories字段列表元素的数量等同于类别的数量，coco为80（2017年）
（五）annotations字段：包括下图中的内容，每个序号对应一个注释，一张图片上可能有多个注释。 详见 coco结构6.jpg
    检测框+实例分割 Object Instance
    annotation{
                "id": int,    
                "image_id": int,
                "category_id": int,
                "segmentation": RLE or [polygon],
                "area": float,
                "bbox": [x,y,width,height],
                "iscrowd": 0 or 1,
                }
    annotations字段列表元素的数量等同于训练集（或者测试集）中bounding box的数量
    category_id：该注释的类别id；
    id：当前注释的id号
    image_id：该注释所在的图片id号
    area：区域面积
    bbox：目标的矩形标注框
    iscrowd：0或1。0表示标注的单个对象，此时segmentation使用polygon表示；1表示标注的是一组对象，此时segmentation使用RLE格式。
    segmentation：
        若使用polygon标注时，则记录的是多边形的坐标点，连续两个数值表示一个点的坐标位置，因此此时点的数量为偶数
        若使用RLE格式（Run Length Encoding（行程长度压缩算法））
    关键点标记的格式  Object Keypoint
    1，整体JSON文件格式
    {
    "info": info,
    "licenses": [license],
    "images": [image],
    "annotations": [annotation],
    "categories": [category]
    }
    images数组元素数量是划入训练集（测试集）的图片的数量；
    annotations是bounding box的数量，在这里只有人这个类别的bounding box；
    categories数组元素的数量为1，只有一个：person（2017年）；
    2，annotations字段
    annotation{
                "keypoints": [x1,y1,v1,...],
                "num_keypoints": int,
                "id": int,
                "image_id": int,
                "category_id": int,
                "segmentation": RLE or [polygon],
                "area": float,
                "bbox": [x,y,width,height],
                "iscrowd": 0 or 1,
                }
    keypoints是一个长度为3*k的数组，其中k是category中keypoints的总数量。每一个keypoint是一个长度为3的数组，第一
    第二个元素分别是x和y坐标值，第三个元素是个标志位v，v为0时表示这个关键点没有标注（这种情况下x=y=v=0），v为1时表
    这个关键点标注了但是不可见（被遮挡了），v为2时表示这个关键点标注了同时也可见
    num_keypoints表示这个目标上被标注的关键点的数量（v>0），比较小的目标上可能就无法标注关键点。
    例{
        "segmentation": [[125.12,539.69,140.94,522.43...]],
        "num_keypoints": 10,
        "area": 47803.27955,
        "iscrowd": 0,
        "keypoints": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,142,309,1,177,320,2,191,398...],
        "image_id": 425226,"bbox": [73.35,206.02,300.58,372.5],"category_id": 1,
        "id": 183126
    }
    3，categories字段
    对于每一个category结构体，相比Object Instance中的category新增了2个额外的字段，keypoints是一个长度为k的数组，包含了每个关键点的名字；skeleton定义了各个关键点之间的连接性（比如人的左手腕和左肘就是连接的，但是左手腕和右手腕就不是）。目前，COCO的keypoints只标注了person category （分类为人）
    {
        "id": int,
        "name": str,
        "supercategory": str,
        "keypoints": [str],
        "skeleton": [edge]
    }
    例
    {
    "supercategory": "person",
    "id": 1,
    "name": "person",
    "keypoints": ["nose","left_eye","right_eye","left_ear","right_ear","left_shoulder","right_shoulder","left_elbow","right_elbow","left_wrist","right_wrist","left_hip","right_hip","left_knee","right_knee","left_ankle","right_ankle"],
    "skeleton": [[16,14],[14,12],[17,15],[15,13],[12,13],[6,12],[7,13],[6,7],[6,8],[7,9],[8,10],[9,11],[2,3],[1,2],[1,3],[2,4],[3,5],[4,6],[5,7]]
    }
    Image Caption的标注格式
    {
        "info": info,
        "licenses": [license],
        "images": [image],
        "annotations": [annotation]
    }
    没有最后的categories字段
    2，annotations字段
    annotation{
                "id": int,
                "image_id": int,
                "caption": str
                }
-------------------------------------------------------------------------------------------------
labelme 数据解析
        {
          "version": "3.11.2",
          "flags": {},
          "shapes": [# 每个对象的形状
                        { # 第一个对象
                          "label": "malignant",
                          "line_color": null,
                          "fill_color": null,
                          "points": [# 边缘是由点构成，将这些点连在一起就是对象的边缘多边形
                            [
                              371, # 第一个点 x 坐标
                              257  # 第一个点 y 坐标
                            ],
                            ...
                            [
                              412,
                              255
                            ]
                          ],
                          "shape_type": "polygon"  # 形状类型：多边形
                        },
                        {
                          "label": "malignant",  # 第一个对象的标签
                          "line_color": null,
                          "fill_color": null,
                          "points": [# 第二个对象
                            [
                              522,
                              274
                            ],
                            ...
                            [
                              561,
                              303
                            ]
                          ],
                          "shape_type": "polygon"
                        },
                    {
                      "label": "malignant", # 第二个对象的标签
                      "line_color": null,
                      "fill_color": null,
                  "imagePath": "../../val2017/000001.jpg", # 原始图片的路径
                  "imageData":"something too long ",# 原图像数据 通过该字段可以解析出原图像数据
                  "imageHeight": 768,
                  "imageWidth": 1024
                    }
    "shapes"：存储标注instance的闭合多边形的信息，重点关注：label：类别名称；points：闭合多边形的每个点的x,y坐标
    "line_color"：闭合多边形的边界线颜色；
    "fill_color"：闭合多边形的填充颜色；
    "imagePath"：图片名称；
    "imageData"：图片路径（加密后）；
    "imageHeight"：图片高；
    "imageWidth"：图片宽；
------------------------------------------------------------------------------------------
xml数据集格式解析