import torch
"""
Configuration module for setting up device and dimensionality.
Attributes:
    device (torch.device): The device to be used for computations, either CUDA if available or CPU.
    DIM (int): Number of dimensions, set to 128 for GPS-level precision.
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DIM = 128 # 128 dimensions pour une précision "GPS"
