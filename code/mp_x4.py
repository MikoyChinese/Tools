#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:32:49 2018

@author: chenzhm
"""

import time
import numpy as np
import os
import cv2
import pandas as pd
from multiprocessing import Pool

s0="""<annotation>
	<folder>VOC2007</folder>
	<filename>{0}</filename>
	<source>
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
		<flickrid>341012865</flickrid>
	</source>
	<owner>
		<flickrid>xxxxxx</flickrid>
		<name>xxxxxx</name>
	</owner>
	<size>
		<width>{1}</width>
		<height>{2}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
"""
s1="""<object>
		<name>{0}</name>
		<pose>Left</pose>
		<truncated>1</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{1}</xmin>
			<ymin>{2}</ymin>
			<xmax>{3}</xmax>
			<ymax>{4}</ymax>
		</bndbox>
	</object>
"""
s2="</annotation>"

combinattxt_path = '/media/commaai/188B55AD658BD5B6/huapu/combinat.txt'
output_log_path = '/media/commaai/188B55AD658BD5B6/huapu/log.txt'
    

class Combination(object):
    
    def __init__(self):
        self.input_image_path = '/media/commaai/188B55AD658BD5B6/huapu/images/'
        self.input_mask_path = '/media/commaai/188B55AD658BD5B6/huapu/mask/'
        self.back_path = '/media/commaai/e9a82959-f258-4132-994c-90eedf3aa58a/450sku/bgim/'
        self.output_mask_path = '/media/commaai/188B55AD658BD5B6/huapu/VOC/Masks/'
        self.output_xml_path = '/media/commaai/188B55AD658BD5B6/huapu/VOC/Annotations/'
        self.output_image_path = '/media/commaai/188B55AD658BD5B6/huapu/VOC/JPEGImages/'
        self.combinat_num = 4
        self.stride = 35
        self.over_rate = [0,0.15]
        self.back_list = os.listdir(self.back_path)
        self.num_mask = len(self.over_rate)
        self.num_back = len(self.back_list)
        
    def _subimage(self,back,shape):
        (box_hei,box_wid) = shape
        height,width = back.shape[0],back.shape[1]
        if float(width)/float(height) > float(box_wid)/ float(box_hei):
            hei1 = height
            wid1 = int(hei1*box_wid/box_hei)
            k = np.random.randint(0, width - wid1+1)
            subImage = back[:, k:k+wid1]
            subImage = cv2.resize(subImage,(box_wid, box_hei),interpolation = cv2.INTER_AREA)
        else:
            wid1 = width
            hei1 = int(wid1*box_hei/box_wid)
            k = np.random.randint(0, height - hei1+1)
            subImage = back[k:k+hei1, :]
            subImage = cv2.resize(subImage, (box_wid, box_hei), interpolation = cv2.INTER_AREA)
        return subImage
        
    def _research(self, input_mask):
        mask_0 = input_mask[0]
        area_0 = np.where(mask_0 !=0 )
        core_0 = [int((max(area_0[0]) + min(area_0[0]))*0.5),int((max(area_0[1]) + min(area_0[1]))*0.5)]
        l = 2400
        r = 1200
        research_map = np.zeros((l,l), dtype = int)
        research_map[tuple([area_0[0]-core_0[0]+r, area_0[1]-core_0[1]+r])] = 1
        
        for i in range(len(input_mask)-1):
            i+=1
            area = np.where(input_mask[i] != 0)
            core = [int((max(area[0]) + min(area[0]))*0.5),int((max(area[1]) + min(area[1]))*0.5)]
            label = i+1
            #max_index = np.amax(research_map)
            completion = False
            for j in range(500):
                if completion:
                    break
                shift_core = [[r-self.stride*j, r-self.stride*j],[r-self.stride*j,r],
                              [r-self.stride*j,r+self.stride*j],[r,r-self.stride*j],
                              [r,r+self.stride*j],[r+self.stride*j,r-self.stride*j],
                              [r+self.stride*j,r],[r+self.stride*j,r+self.stride*j]]
                np.random.shuffle(shift_core)

                for k in range(8):
                    shift_map = np.zeros((l,l), dtype = int)
                    shift_map[tuple([area[0]-core[0]+shift_core[k][0],area[1]-core[1]+shift_core[k][1]])] = label
                    count_map = research_map + shift_map
                    overlap_area = np.where(count_map>label)
                    if len(overlap_area[0])==0:
                        research_map = count_map
                        research_map[overlap_area] = label
                        completion = True
                        break
        area_map = np.where(research_map!=0)
        resize_map = research_map[min(area_map[0])-10-np.random.randint(60):max(area_map[0])+10+np.random.randint(60),
                                  min(area_map[1])-10-np.random.randint(60):max(area_map[1])+10+np.random.randint(60)]
        return resize_map
    
    def drawMap(self, input_mask_image_path_name):

        input_mask = [cv2.imread(self.input_mask_path+input_mask_image_path_name[i].split('_')[0]+
                                 '/'+input_mask_image_path_name[i],0) for i in range(self.combinat_num)]
        input_image = [cv2.imread(self.input_image_path+input_mask_image_path_name[i].split('_')[0]+
                                  '/'+input_mask_image_path_name[i].split('_')[3]+
                                  '/'+input_mask_image_path_name[i].split('_')[4]+
                                  '/'+input_mask_image_path_name[i].split('_mask')[0]+'.jpg') for i in range(self.combinat_num)]
        comb_name = input_mask_image_path_name[-1]

        mask_map = self._research(input_mask)
        image_size = mask_map.shape
        image_map = np.zeros((image_size[0], image_size[1], 3))
        
        xml = s0.format(comb_name + '.jpg', image_size[1], image_size[0])
        bg = cv2.imread(self.back_path + self.back_list[np.random.randint(self.num_back)])
        bg = self._subimage(bg,image_size)
        image_map[np.where(mask_map == 0)] = bg[np.where(mask_map == 0)]
        for i in range(len(input_image)):
            area_i = np.where(mask_map == i+1)
            image_map[area_i] = input_image[i][np.where(input_mask[i] != 0)]
            obj_name = input_mask_image_path_name[i].split('_')[0]
            #cv2.rectangle(image_map, (min(area_i[1]), min(area_i[0])), (max(area_i[1]), max(area_i[0])), (0,0,255), 2)
            #cv2.putText(image_map, obj_name, (min(area_i[1]), min(area_i[0])), 0, 0.5, (255,0,0), 2)
            #cv2.rectangle(mask_map, (min(area_i[1]), min(area_i[0])), (max(area_i[1]), max(area_i[0])), 255, 2)
            #cv2.putText(mask_map, obj_name, (min(area_i[1]), min(area_i[0])), 0, 0.5, 255, 2)
            obj = s1.format(obj_name, min(area_i[1]), min(area_i[0]), max(area_i[1]), max(area_i[0]))
            xml = xml+'\n'+obj
                        
        xml += s2
        cv2.imwrite(self.output_mask_path + comb_name+'.png', mask_map*50)
        cv2.imwrite(self.output_image_path + comb_name+'.jpg', image_map)
        f_xml = open(self.output_xml_path + comb_name+'.xml', 'w')
        f_xml.write(xml)
        f_xml.close()

def cobination_mutipro(input_mask_image_path_name):
    Comb = Combination()
    Comb.drawMap(input_mask_image_path_name)
        
if __name__ == '__main__':
    num_0 = 0
    num_1 = -1
    input_mask_image_path_name = pd.read_table(combinattxt_path,header=None,delim_whitespace=True)
    data = np.array(input_mask_image_path_name).tolist()
    num_all = len(data) 
    data = data[num_0:num_1]   
    #Comb = Combination()
    #Comb.drawMap(data[0])

    pool = Pool(48)
    startTime = time.time()
    _ = pool.map(cobination_mutipro, data[:])
    pool.close()
    pool.join()
    print("used time is:%f"%(time.time() - startTime))
    f = open(output_log_path, 'w')
    f.write("used time is: %d \n"%(time.time() - startTime))
    f.write("start:%d  end:%d  all:%d"%(num_0,num_1,num_all))
    f.close()    
