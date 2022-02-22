from skimage import io
import numpy as np
from skimage.transform import rescale, resize, downscale_local_mean
import os
from tqdm import tqdm
import h5py


def preprocessing(image_path, shape):
    # opens the image
    img = io.imread(image_path)

    # expands the image to a square shape
    height, width = img.shape
    if width == height:
        pass
    elif width > height:
        missing = int((width - height) / 2)
        img = np.pad(img, ((missing, missing), (0, 0),))
    else:
        missing = int((height - width) / 2)
        img = np.pad(img, ((0, 0), (missing, missing),))

    # resizes the image to shape x shape
    img = resize(img, (shape, shape), anti_aliasing=True)

    return np.array(img)

#calculating the amount of valid samples i have
#i have all samples from the AWS s3 bucket of domoritz label generator
n_samples = 0
for file in tqdm(os.listdir(r"D:\studium_tests\amazon\acl_anthology\img")):
    if not file[-4] == "x.png":
        path1 = os.path.join(r"D:\studium_tests\amazon\acl_anthology\img", file)
        path2 = os.path.join(r"D:\studium_tests\amazon\acl_anthology\text-masked", file[:-4] + "-label.png")

        if os.path.exists(path1) and os.path.exists(path2):
            n_samples += 1

#creating indices for the sets
shuffled_indices = np.random.permutation(n_samples)
testset_inds = shuffled_indices[:int(n_samples / 10)]
validationset_inds = shuffled_indices[int(n_samples / 10):int(n_samples / 10) * 2]
trainingset_inds = shuffled_indices[int(n_samples / 10) * 2:]

#going through all files and if there is some picture and a mask,
#preprocess it and put it in the right set
testset = []
trainset = []
validationset = []
x = 0
for i, file in enumerate(tqdm(os.listdir(r"D:\studium_tests\amazon\acl_anthology\img"))):
    if not file[-4] == "x.png":
        try:
            path = os.path.join(r"D:\studium_tests\amazon\acl_anthology\img", file)
            img = preprocessing(path, 256)

            path = os.path.join(r"D:\studium_tests\amazon\acl_anthology\text-masked", file[:-4] + "-label.png")
            label = preprocessing(path, 64)

            flat_img = np.array(img.flatten(), dtype=np.float32)
            flat_label = np.array(label.flatten(), dtype=np.float32)
            img_label = np.concatenate([flat_img, flat_label])
            if i in testset_inds:
                testset.append(img_label)
            elif i in trainingset_inds:
                trainset.append(img_label)
            elif i in validationset_inds:
                validationset.append(img_label)
        except:
            pass


# saving the arrays
train_arrays = np.array(trainset, dtype=np.float32)
test_arrays = np.array(testset, dtype=np.float32)
validation_arrays = np.array(validationset, dtype=np.float32)
with h5py.File(
        r"C:\Users\fabio\Google_Drive\AI_Studium\practical_work\reverse_engineering_vis\my_pipeline\domoritz_data\anthology_for_colab32.h5py",
        "w") as f:
    f.create_dataset(r"testset", data=test_arrays)
    f.create_dataset(r"trainset", data=train_arrays)
    f.create_dataset(r"validationset", data=validation_arrays)
print("everything completed")