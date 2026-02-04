from src.train import train_model
from tests.test_extensive import run_tests

if __name__ == "__main__":
    # Train the model
    model = train_model()
    
    # Run the extensive test suite
    run_tests(model)