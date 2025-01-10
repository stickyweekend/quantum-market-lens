import os
from dotenv import load_dotenv

class SecureConfig:
    @staticmethod
    def load_api_key():
        load_dotenv()
        return os.getenv('ALPHA_VANTAGE_API_KEY')

    @staticmethod
    def get_quantum_params():
        return {
            'micro_lag': float(os.getenv('QUANTUM_MICRO_LAG', '0.000009')),
            'wavelet_base': int(os.getenv('QUANTUM_WAVELET_BASE', '17')),
            'compton_base': float(os.getenv('QUANTUM_COMPTON_BASE', '43.00826')),
            'entropy_weight': float(os.getenv('QUANTUM_ENTROPY_WEIGHT', '0.85')),
            'coherence_threshold': float(os.getenv('QUANTUM_COHERENCE_THRESHOLD', '1.014000')),
            'hma_length': int(os.getenv('QUANTUM_HMA_LENGTH', '53'))
        }