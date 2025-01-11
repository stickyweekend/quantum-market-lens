import json
import pandas as pd
from pathlib import Path
from datetime import datetime

class QuantumDataExporter:
    def __init__(self, export_dir="quantum_exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        self.training_data = {
            'metrics_history': [],
            'phase_transitions': [],
            'optimization_paths': [],
            'coherence_peaks': []
        }
        
    def log_training_event(self, event_type, data):
        timestamp = datetime.now().isoformat()
        event_data = {
            'timestamp': timestamp,
            'type': event_type,
            **data
        }
        self.training_data[event_type].append(event_data)
        
    def export_training_data(self, format='json'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'json':
            self._export_json(timestamp)
        elif format == 'csv':
            self._export_csv(timestamp)
            
    def _export_json(self, timestamp):
        filepath = self.export_dir / f"quantum_training_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(self.training_data, f, indent=2)
            
    def _export_csv(self, timestamp):
        # Export different aspects as separate CSV files
        for data_type, events in self.training_data.items():
            if events:  # Only export if we have data
                df = pd.DataFrame(events)
                filepath = self.export_dir / f"quantum_{data_type}_{timestamp}.csv"
                df.to_csv(filepath, index=False)