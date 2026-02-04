import torch
import torch.nn.functional as F
from .config import device
from .manifold import get_universal_vector
from .model import LawNet

def train_model():
    """
    Trains the LawNet model to learn intrinsic laws of addition using sparse training.
    The function initializes the LawNet model and an AdamW optimizer. It then performs
    10,000 training steps where, in each step:
        - Random tensors 'a' and 'b' are generated, representing numbers in a wide range.
        - Their sum 'res' is computed.
        - Universal vector representations for 'a', 'b', and 'res' are obtained.
        - The model predicts the result vector from 'a' and 'b'.
        - The loss is calculated as the mean cosine similarity error between the prediction and the true result vector.
        - The optimizer updates the model parameters based on the loss.
    Progress is printed every 1,000 steps, showing the current structural error.
    Returns:
        LawNet: The trained LawNet model.
    """
    model = LawNet().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0005)

    # ==========================================================
    # 4. ENTRAÎNEMENT PAR LES RELATIONS (Sparse Training)
    # ==========================================================
    print(" L'IA apprend les lois intrinsèques de l'espace...")
    
    for step in range(1, 10001):
        # On lui montre des exemples PARTOUT (petits et grands)
        # pour qu'il comprenne que la loi est la même partout.
        a = torch.exp(torch.rand(128, device=device) * 15) # Nombres de 1 à 3 millions
        b = torch.exp(torch.rand(128, device=device) * 12)
        res = a + b
        
        v_a = get_universal_vector(a)
        v_b = get_universal_vector(b)
        v_res = get_universal_vector(res)
        
        optimizer.zero_grad()
        pred = model(v_a, v_b)
        
        loss = (1 - F.cosine_similarity(pred, v_res)).mean()
        loss.backward()
        optimizer.step()
        
        if step % 1000 == 0:
            print(f"Step {step} | Erreur de structure : {loss.item():.8f}")
            
    return model
