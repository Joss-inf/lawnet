import torch.nn as nn
import torch.nn.functional as F
from .config import DIM

# ==========================================================
# 3. L'OPÉRATEUR DE RAISONNEMENT (LawNet)
# ==========================================================
class LawNet(nn.Module):
    """
    LawNet neural network module.
    This module models the relationship between two input vectors, learning how the '+' operation distorts the vector space.
    It concatenates two input vectors, processes them through a sequence of linear layers with GELU activations, and projects
    the result onto the surface of a manifold using L2 normalization.
    Attributes:
        op (nn.Sequential): Sequential neural network layers for processing concatenated input vectors.
    Methods:
        forward(v_a, v_b):
            Concatenates input vectors v_a and v_b, passes them through the network, and returns the normalized output vector.
            Args:
                v_a (torch.Tensor): First input vector of shape (..., DIM).
                v_b (torch.Tensor): Second input vector of shape (..., DIM).
            Returns:
                torch.Tensor: Output vector of shape (..., DIM), normalized to unit length.
    """
    def __init__(self):
        super().__init__()
        # Ce réseau apprend la RELATION entre les vecteurs.
        # Il apprend comment le signe '+' tord l'espace.
        self.op = nn.Sequential(
            nn.Linear(DIM * 2, 512),
            nn.GELU(),
            nn.Linear(512, 512),
            nn.GELU(),
            nn.Linear(512, DIM)
        )
        
    def forward(self, v_a, v_b):
        import torch
        x = torch.cat([v_a, v_b], dim=-1)
        # On projette le résultat sur la surface du Manifold
        return F.normalize(self.op(x), p=2, dim=-1)
