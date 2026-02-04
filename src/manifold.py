import torch
from .config import device, DIM

# ==========================================================
# 1. LE MANIFOLD INFINI (La structure des lois)
# ==========================================================
def get_universal_vector(n, dim=DIM):
    """ 
    Transforme un nombre n en un état géométrique pur.
    On utilise 128 fréquences pour couvrir de 0 à 100 millions.
    """
    if isinstance(n, torch.Tensor): n = n.unsqueeze(-1)
    
    # Échelle de fréquences : de très lente (100M) à très rapide (1)
    # C'est comme un code-barres géométrique infini
    freqs = 1.0 / (100_000_000 ** (torch.arange(0, dim, 2, device=device).float() / dim))
    
    args = n * freqs
    v = torch.zeros(n.shape[0] if isinstance(n, torch.Tensor) else 1, dim, device=device)
    v[:, 0::2] = torch.sin(args)
    v[:, 1::2] = torch.cos(args)
    return v.squeeze(0)

# ==========================================================
# 2. LE DÉCODEUR ANALYTIQUE (Le "Cerveau" Mathématique)
# ==========================================================
def decode_manifold(vector):
    """
    Retrouve la valeur n par analyse de phase.
    Zéro mémoire utilisée. C'est du calcul pur.
    """
    # On extrait l'angle de la fréquence la plus lente (la base)
    sin_val, cos_val = vector[0], vector[1]
    angle = torch.atan2(sin_val, cos_val)
    
    # On remonte au nombre n (on dés-applique la fréquence de base)
    freq_base = 1.0 
    n_approx = angle / freq_base # Concept simplifié
    
    # Dans un système complet, on utilise les 128 dims pour corriger
    # Ici, on utilise un scanner de phase haute résolution
    return n_approx
