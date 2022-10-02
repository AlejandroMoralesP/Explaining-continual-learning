from PIL import Image
from torchvision import transforms
from gradcam.utils import visualize_cam
from gradcam import GradCAM

import os
import torch
import glob
import csv

from models.classifier import Classifier
from models.vae import AutoEncoder
from define_models import init_params

device = 'cpu'
# classes = [
#     'butterfly', #task1
#     'castle', #task3
#     'pear', #task4
#     ]

id_permutation = {26: 'apple',
86: 'aquarium_fish',
2: 'baby',
55: 'bear',
75: 'beaver',
93: 'bed',
16: 'bee',
73: 'beetle',
54: 'bicycle',
95: 'bottle',
53: 'bowl',
92: 'boy',
78: 'bridge',
13: 'bus',
7: 'butterfly',
30: 'camel',
22: 'can',
24: 'castle',
33: 'caterpillar',
8: 'cattle',
43: 'chair',
62: 'chimpanzee',
3: 'clock',
71: 'cloud',
45: 'cockroach',
48: 'couch',
6: 'crab',
99: 'crocodile',
82: 'cup',
76: 'dinosaur',
60: 'dolphin',
80: 'elephant',
90: 'flatfish',
68: 'forest',
51: 'fox',
27: 'girl',
18: 'hamster',
56: 'house',
63: 'kangaroo',
74: 'keyboard',
1: 'lamp',
61: 'lawn_mower',
42: 'leopard',
41: 'lion',
4: 'lizard',
15: 'lobster',
17: 'man',
40: 'maple_tree',
38: 'motorcycle',
5: 'mountain',
91: 'mouse',
59: 'mushroom',
0: 'oak_tree',
34: 'orange',
28: 'orchid',
50: 'otter',
11: 'palm_tree',
35: 'pear',
23: 'pickup_truck',
52: 'pine_tree',
10: 'plain',
31: 'plate',
66: 'poppy',
57: 'porcupine',
79: 'possum',
85: 'rabbit',
32: 'raccoon',
84: 'ray',
14: 'road',
89: 'rocket',
19: 'rose',
29: 'sea',
49: 'seal',
97: 'shark',
98: 'shrew',
69: 'skunk',
20: 'skyscraper',
94: 'snail',
72: 'snake',
77: 'spider',
25: 'squirrel',
37: 'streetcar',
81: 'sunflower',
46: 'sweet_pepper',
39: 'table',
65: 'tank',
58: 'telephone',
12: 'television',
88: 'tiger',
70: 'tractor',
87: 'train',
36: 'trout',
21: 'tulip',
83: 'turtle',
9: 'wardrobe',
96: 'whale',
67: 'willow_tree',
64: 'wolf',
47: 'woman',
44: 'worm'}

# NAME = ['ewc_task10_iteration5000of5000']


def load_checkpoint(model, model_dir, verbose=True, name=None, add_si_buffers=False):
    '''Load saved state (in form of dictionary) at [model_dir] (if name is None, use "model.name") to [model].'''
    # -path from where to load checkpoint
    name = model.name if name is None else name
    path = os.path.join(model_dir, name)
    # -if required, add buffers to [model] to make sure its 'state_dict' matches the 'state_dict' of model to be loaded
    if add_si_buffers:
        for n, p in model.named_parameters():
            if p.requires_grad:
                n = n.replace('.', '__')
                p_current = p.detach().clone()
                omega = p.detach().clone().zero_()
                model.register_buffer('{}_SI_prev_task'.format(n), p_current)
                model.register_buffer('{}_SI_omega'.format(n), omega)
    # load parameters (i.e., [model] will now have the state of the loaded model)
    checkpoint = torch.load(path, map_location='cpu')
    model.load_state_dict(checkpoint['state'], strict=False)
    # notify that we succesfully loaded the checkpoint
    # if verbose:
    #     print(' --> loaded checkpoint of {name} from {path}'.format(name=name, path=model_dir))
    

def load_model(model_name):
    if model_name.startswith('bi-r'):
        model = AutoEncoder(image_size=32, image_channels=3, classes=100, conv_type='standard', 
                depth=5, start_channels=16, reducing_layers=4,
                conv_bn = True, conv_nl ='relu', num_blocks = 2,
                global_pooling=False, no_fnl=True, convE=None, conv_gated=False,
                fc_layers=3, fc_units=2000, h_dim=2000,
                fc_drop=0.0, fc_bn=False, fc_nl='relu', excit_buffer=True, fc_gated=False,
                prior="GMM", z_dim=100, per_class=True, n_modes=1,
                recon_loss='MSE', network_output="none", deconv_type="standard", hidden=False,
                dg_gates=True, dg_type="class", dg_prop=0.0, tasks=10, scenario="task",
                device='cuda', classifier=True, classify_opt="beforeZ", lamda_pl=1.0,
                lamda_rcl=1.0, lamda_vl=1.0, excitability=False
        )
        return model
    elif model_name.startswith('ewc') or model_name.startswith('baseline'):
        model = Classifier(image_size=32, image_channels=3, classes=100, conv_type='standard', 
                depth=5, start_channels=16, reducing_layers=4,
                conv_bn = True, conv_nl ='relu', num_blocks = 2,
                global_pooling=False, no_fnl=True, conv_gated=False, fc_layers=3, fc_units=2000, h_dim=2000,
                fc_drop=0.0, fc_bn=False, fc_nl='relu', excit_buffer=True, fc_gated=False,
                bias=True, excitability=False, hidden=False
        )
        return model


def gradcam_extractor():
    classes = glob.glob(os.path.join('./cifar100_png/train/', '*'))
    model_names = glob.glob(os.path.join('./store/models/', '*.pt'))
    
    name_cp = ''
    for clas in classes:
        cla = clas[21:]
        for nam in model_names:
            n = nam[15:]
            if not os.path.exists('results/{}_{}'.format(cla, n)):
                os.makedirs('results/{}_{}'.format(cla, n))
                os.makedirs('results/{}_{}/heatmaps'.format(cla, n))
            model = load_model(n)
            load_checkpoint(model, './store/models', name=n)
            with open('results/{}_{}.csv'.format(cla, n), 'a', newline='') as file:
                img_dir = './cifar100_png/test/{}'.format(cla)
                for img in range(1,101):
                    if img < 10:
                        img_name = '000{}.png'.format(img)
                    elif 10 <= img < 100:
                        img_name = '00{}.png'.format(img)
                    else:
                        img_name = '0{}.png'.format(img)

                    img_path = os.path.join(img_dir, img_name)

                    pil_img = Image.open(img_path)



                    torch_img = transforms.Compose([
                        transforms.Resize((32, 32)),
                        # transforms.RandomHorizontalFlip(),
                        transforms.ToTensor(),
                    ])(pil_img).to(device)
                    normed_torch_img = transforms.Normalize(mean=[0.5071, 0.4865, 0.4409], std=[0.2673, 0.2564, 0.2761])(torch_img)[None]

                    ############## loop for model layers ###################
                    combinations = ['.conv', '.bn', '.nl']
                    for name, layer in model.named_modules():
                        if name.startswith('convE') and any(map(name.endswith, combinations)) and (int(name[15]) == 3 or int(name[15]) == 5):
                    ########################################################
                            model.eval()
                            target_layer = layer
                            gradcam = GradCAM(model, target_layer)
                            # print(model.name)
                            mask, _ = gradcam(normed_torch_img)
                            heatmap, result = visualize_cam(mask, torch_img)

                            im2 = transforms.ToPILImage()(result)
                            # im2.show()
                            pred = model(normed_torch_img)

                            layer_name = name.replace(".", "-")[6:]
                            pred_name = id_permutation[pred.argmax(dim=1).numpy()[0]]
                            heatmap_name = '{}{}_{}_{}.png'.format(img_name.replace(".png", ""), cla, layer_name, pred_name)

                            im2.save('./results/{}_{}/heatmaps/{}'.format(cla, n, heatmap_name))
                            writer = csv.writer(file)

                            if cla == pred_name:
                                success = True
                            else:
                                success = False
                            
                            if name_cp != '{}_{}.csv'.format(cla, n):
                                name_cp = '{}_{}.csv'.format(cla, n)
                                writer.writerow(["Image", "Label", "Layer", "Prediction", "Heatmap", "Success"])
                            writer.writerow([img_name, cla, layer_name, pred_name, heatmap_name, success])

                            # ind = ind + 1
                    # print(pred.argmax(dim=1).numpy()[0])
                writer.writerow(["\n"])
                

if __name__ == '__main__':
    gradcam_extractor()
