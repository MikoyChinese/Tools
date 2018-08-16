import os
import numpy as np

combination_num = 4
mask_path = '/media/commaai/188B55AD658BD5B6/huapu/mask'
output_combinattxt = '/media/commaai/188B55AD658BD5B6/huapu/combinat.txt'

def get_mask(mask_path):
    sku = os.listdir(mask_path)
    sample_num = 768
    mask_list = []
    for f in sku:
        one_mask = os.listdir(mask_path+'/'+f)
        if len(one_mask)==sample_num:
            mask_list += one_mask
        elif len(one_mask)<sample_num:
            k = int(sample_num/len(one_mask))
            mask_list += one_mask*k
            rk = sample_num-k*len(one_mask)
            for i in range(rk):
                mask_list.append(mask_list[np.random.randint(rk)])
        else:
            np.random.shuffle(one_mask)
            mask_list += one_mask[:sample_num]
    print('mask_num: %d'%len(mask_list))
    return mask_list

def combination_array(mask_list, combination_num):
    mask_x = []
    name = []
    for i in range(combination_num):
        mask_list_i = mask_list + []
        np.random.shuffle(mask_list_i)
        mask_x.append(mask_list_i)

    for i in range(len(mask_list)):
        text = ''
        for j in range(len(mask_x)):
            text = text + mask_x[j][i].split('_')[0] + '_'        
        name_endding = 1
        name_i = text + str(name_endding)
        while(name_i in name):
            name_endding += 1
            name_i = text + str(name_endding)
        name.append(name_i)
    mask_x.append(name)

    print('mask_x: %d,%d'%(len(mask_x),len(mask_x[0])))
    return mask_x

def main():
    mask_list = get_mask(mask_path)
    mask_x = combination_array(mask_list, combination_num)
    combinat_txt = open(output_combinattxt, 'w')
    for i in range(len(mask_x[0])):
        text = ''
        for j in range(len(mask_x)):
            text = text + mask_x[j][i] + ' '
        combinat_txt.write(text+'\n')
    combinat_txt.close()

if __name__ == '__main__':
    main()
    import pandas as pd
    data = pd.read_table(output_combinattxt,header=None,delim_whitespace=True) 
    x = np.array(data).tolist()
    print(x[0])
    
        
