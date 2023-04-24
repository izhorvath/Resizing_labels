import sys
sys.path.insert(0,'/home/izabela/Documents/Code/Utils/helperfunctions')
import filehandling
import os 
import numpy as np


from PIL import Image # .resize as imresize
import cv2
from tqdm import tqdm
from shutil import copy

###FILL IN HERE:###

path_volume_in='/media/izabela/18TB_linux1/LNP/LNP_segm_DS/postprocessed.nii.gz' #3D Segmentation volume

path_slices_out_small='/media/izabela/18TB_linux1/LNP/LNP_segm_slices/slices_ds_2/' #path for the slices - small
path_slices_out_fullres='//media/izabela/18TB_linux1/LNP/LNP_segm_slices/slices_us_3/' # path for the slice - big
final_path = '/media/izabela/18TB_linux1/LNP/LNP_segm_slices/fullres_3/' #final output path

downsampling_factor=16 #in z direction ; x-y should be infered from the samples
slices_fullres='/media/izabela/18TB_linux1/LNP/C00/' #example for size

#1. Slice up the volume

vol=filehandling.readNifti(path_volume_in)
vol.shape

for myslice in range(vol.shape[2]):
    cv2.imwrite(path_slices_out_small+'label_Z'+str(downsampling_factor*myslice).zfill(4)+'.tif',(vol[:,:,myslice]).astype(np.uint8))

#Take example of how big the samples should be:
one_orig_file = os.listdir(slices_fullres)[0]
image = cv2.imread(slices_fullres + '/' + one_orig_file, 2)
img_dim = (image.shape[1],image.shape[0])

for sample in tqdm(os.listdir(path_slices_out_small)):
    if(os.path.isfile(path_slices_out_fullres + sample) is False):
        # upsample & copy file, if not already present
        gt_slice = cv2.imread(path_slices_out_small + sample, 2)
        image_ds = cv2.resize(gt_slice,img_dim, interpolation = cv2.INTER_NEAREST).astype(np.uint8)
        cv2.imwrite(path_slices_out_fullres + sample,image_ds)

#copy z-slices forward and back
for index in range(len(os.listdir(slices_fullres))):
    slice_number = index
    print(slice_number)
    if(os.path.isfile(final_path+'label_Z'+str(slice_number).zfill(4)+'.tif') is False):
        if(slice_number%downsampling_factor)<=downsampling_factor//2:
            copy(path_slices_out_fullres+'label_Z'+str((slice_number//downsampling_factor)*downsampling_factor).zfill(4)+'.tif',final_path+'label_Z'+str(slice_number).zfill(4)+'.tif')
        else:
            copy(path_slices_out_fullres+'label_Z'+str(((slice_number//downsampling_factor) + 1)*downsampling_factor).zfill(4)+'.tif',final_path+'label_Z'+str(slice_number).zfill(4)+'.tif')
