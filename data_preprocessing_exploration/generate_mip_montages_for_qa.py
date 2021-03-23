import numpy as np
import nibabel as nib
import pathlib as pl
import matplotlib.pyplot as plt
import gc
from tqdm import tqdm

# set path to data
base_path = pl.Path.cwd().parent.parent.parent.parent / "nfs" / "masi" / "ramadak" / "BRATS"


# utility functions
def get_modality(img_idx, modality):
    
    img_idx = str(img_idx)
    
    img_path = base_path / ("BraTS20_Training_"+img_idx) / ("BraTS20_Training_"+img_idx+"_" + modality + ".nii.gz")
    
    return nib.load(img_path).get_fdata() 


def plot(axis, img, name):
    axis.axis("off")

    axis.imshow(np.rot90(np.rot90(np.rot90(img[:,:]))), cmap="gray", vmax=img.max(), vmin=img.min())
        
    axis.set_title(name)
        
        
### save all mips
def plot_mod(flair,t1,t2,t1ce,seg, brats_subj,ft2):
    
    
    f, axarr = plt.subplots(2,3)

    f.set_figheight(8)
    f.set_figwidth(12)

    plot(axarr[0,0], flair, "flair", )
    plot(axarr[0,1], t1,"t1", )
    #plot(axarr[0,2], np.zeros([240,240]), "placeholder", )
    plot(axarr[0,2], ft2, "flair + t2", )


    plot(axarr[1,0], t2,"t2", )
    plot(axarr[1,1], t1ce,"t1ce", )
    plot(axarr[1,2], seg, "mask",)
    
    
    plt.savefig(pl.Path.cwd() / "mips" / pl.Path("mips_"+str(brats_subj)+".png")  )
    
    plt.cla()
    plt.clf()
    gc.collect()
    
    
# get subj numbers
paths = [x for x in base_path.iterdir()]
subjs = []
for path in paths:
    subjs.append(int(str(path)[-3:]))
    
# generate the mips 
for brats_subj in tqdm(subjs):

    #load segmentation
    seg_path = base_path / ("BraTS20_Training_"+str(brats_subj)) / ("BraTS20_Training_"+str(brats_subj)+"_seg.nii.gz")
    seg = nib.load(seg_path).get_fdata()
    seg[seg>0] = 1

    # load modalities
    flair = get_modality(brats_subj, "flair")
    t1 = get_modality(brats_subj,"t1")
    t2 = get_modality(brats_subj,"t2")
    t1ce = get_modality(brats_subj,"t1ce")

    #normalize
    flair /= flair.max()
    t1 /= t1.max()
    t2 /= t2.max()
    t1ce /= t1ce.max()
    
    ft2 = flair+t2
    ft2 /= ft2.max()

    #make mips
    flair_mip = np.max(flair, axis=2)
    t1_mip = np.max(t1, axis=2)
    t2_mip = np.max(t2, axis=2)
    t1ce_mip = np.max(t1ce, axis=2)
    seg_mip = np.max(seg, axis=2)
    
    ft2_mip = np.max(ft2,axis=2)
    
    #save the mip montage
    plot_mod(flair_mip,
             t1_mip,
             t2_mip,
             t1ce_mip,
             seg_mip, 
             brats_subj,
             ft2_mip)
    

    


