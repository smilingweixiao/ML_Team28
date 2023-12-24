import numpy as np
import cv2
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from torchvision.transforms import (
    Compose,
    Normalize,
    Resize,
    ToPILImage,
    ToTensor,
)

def cnn_detection(labels, png_path):
    if torch.cuda.is_available():
        device = torch.device('cuda')
        torch.backends.cudnn.benchmark = True
    else:
        device = torch.device('cpu')
        
    normalize = Normalize(mean=[0.3117, 0.3117, 0.3117], std=[0.1215, 0.1215, 0.1215])
    test_transform = Compose(
        [
            ToPILImage(),
            Resize((224,224)),
            ToTensor(),
            normalize,
        ]
    )
    print(device)
    normalize = Normalize(mean=[0.3117, 0.3117, 0.3117], std=[0.1215, 0.1215, 0.1215])
    model2 = models.resnext50_32x4d(weights='IMAGENET1K_V2')
    model2.fc = nn.Linear(in_features=model2.fc.in_features,out_features=2,bias=True)
    model2 = model2.to(device)
    checkpoint = torch.load("resnext_newyolo__checkpoint_best.pth", map_location=device)
    model2.load_state_dict(checkpoint["model_state"]) 
    
    new_labels = labels
    for i, lab in enumerate(labels):
        image = cv2.imread(png_path + 'crop' + str(i+1) + '.png')
        data = test_transform(image)
        data = data.reshape((1,) + data.shape)
        with torch.no_grad():
            data = data.to(device)
            outputs = model2(data)
            softmax_output = F.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs.data, 1)
            if predicted[0].item() == 1:
                new_labels[i]['cnnSays'] = 'mass'
                new_labels[i]['pngIndex'] = i+1
                print (i+1, "mass")
            else:
                new_labels[i]['cnnSays'] = 'background'
                new_labels[i]['pngIndex'] = i+1
                print (i+1, "background")
                
    return new_labels