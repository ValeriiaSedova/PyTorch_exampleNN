import torch
from torch._C import import_ir_module

class ResNet(torch.nn.Module):

    def __init__(self):
        super(ResNet, self).__init__()

        self.layers = [
            torch.nn.Conv2d(3, 64, 7, 2),
            torch.nn.BatchNorm2d(64),
            torch.nn.LeakyReLU(),
            torch.nn.MaxPool2d(3, 2),
            ResBlock(64, 64, 1),
            ResBlock(64, 128, 2),
            ResBlock(128, 256, 2),
            ResBlock(256, 512, 2),
            torch.nn.AdaptiveAvgPool2d((1, 1)),
            torch.nn.Flatten(),
            torch.nn.Linear(512, 2),
            torch.nn.Sigmoid(),
            ]

        self.layers = torch.nn.ModuleList(self.layers)

    def forward(self, input_tensor):
        x = input_tensor
        for layer in self.layers:
            x = layer.forward(x)
        return x


 
class ResBlock(torch.nn.Module):

    def __init__(self, input_channels, output_channels, stride):
        super().__init__()
        self.identity_downsample = torch.nn.Sequential(
            torch.nn.Conv2d(input_channels, output_channels, kernel_size=1, stride=stride),
            torch.nn.BatchNorm2d(output_channels)
        )
        
        self.layers =[
            torch.nn.Conv2d(input_channels, output_channels, kernel_size = 3, stride = stride, padding = 1),
            torch.nn.BatchNorm2d(output_channels),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(output_channels, output_channels, kernel_size = 3, padding = 1),
            torch.nn.BatchNorm2d(output_channels),
            torch.nn.LeakyReLU()]

        self.layers = torch.nn.ModuleList(self.layers)

    def forward(self, input_tensor):
        x = input_tensor
        for i, layer in enumerate(self.layers):
            x = layer.forward(x)
            if i == 4:
                input_tensor = self.identity_downsample(input_tensor)
                x += input_tensor
        return x
    
        


