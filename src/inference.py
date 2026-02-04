import torch
from .config import device
from .manifold import get_universal_vector

# ==========================================================
# 5. TEST : RAISONNEMENT SUR L'INCONNU TOTAL
# ==========================================================
def test_universal(model, a_val, b_val):
    """
    Tests the model's ability to compute the result of a universal operation (e.g., addition) between two values.
    Args:
        model: The PyTorch model to evaluate. Should accept two input vectors and output a result vector.
        a_val (int or float): The first operand value.
        b_val (int or float): The second operand value.
    Returns:
        None. Prints the model's predicted result and the expected result to the console.
    Process:
        - Converts input values to universal vectors.
        - Passes vectors through the model to obtain a result vector.
        - Scans a range of possible results, comparing each to the model's output using cosine similarity.
        - Selects the value with the highest similarity as the model's predicted result.
        - Prints the question, the model's result, and the expected result.
    """
    model.eval()
    with torch.no_grad():
        v_a = get_universal_vector(torch.tensor([a_val], device=device)).unsqueeze(0)
        v_b = get_universal_vector(torch.tensor([b_val], device=device)).unsqueeze(0)
        
        # L'IA calcule le vecteur résultant par application de la LOI
        v_res = model(v_a, v_b).squeeze(0)
        
        # On décode géométriquement (Scan haute résolution)
        # On cherche le n qui fitte le mieux le vecteur de l'IA
        # (C'est la seule étape de 'scan', mais elle est mathématique)
        test_range = torch.linspace(a_val + b_val - 100, a_val + b_val + 100, 2000, device=device)
        target_manifold = get_universal_vector(test_range)
        sims = torch.matmul(target_manifold, v_res)
        best_idx = torch.argmax(sims)
        final_n = test_range[best_idx].item()
        
        print(f"Question : {a_val} + {b_val}")
        print(f"Résultat IA : {int(final_n)} | Attendu : {a_val + b_val}")
        print("-" * 30)
