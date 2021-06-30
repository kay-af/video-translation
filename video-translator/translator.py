import torch.nn as nn
import torch
import numpy as np
from PIL import Image
import torchvision
from models import Generator
import torchvision.transforms as transforms

def tensor2PIL(tensor):
    image = 127.5*(tensor.detach().cpu().float().numpy() + 1.0)
    image = np.einsum('ijk->jki', image)
    return Image.fromarray(image.astype(np.uint8))

generator = Generator(3, 3)

device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
print('I Using', device)

def set_model(path):
    generator.load_state_dict(torch.load(path, map_location=device))

def translate(images, include_logs=True):
    transform = transforms.ToTensor()
    images = [transform(image) for image in images]
    b = torch.stack(images).to(device)
    if include_logs:
        print('I Batch transformation starts')
    out = generator(b)
    out = out.detach()
    outs = []
    for tensorImg in out:
        outs.append(tensor2PIL(tensorImg))
    if include_logs:
        print('I Batch transformed')
    return outs