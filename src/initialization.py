import asyncio
from typing import Dict, Any
from .visualization.monitoring import QuantumAgentMonitor
from .training.enhanced_training import EnhancedTrainingCoordinator

class SystemInitializer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.monitor = QuantumAgentMonitor(config)
        self.training_coordinator = EnhancedTrainingCoordinator()
        
    async def initialize_system(self):
        # Initialize visualization
        await self.monitor.initialize_visualization()
        
        # Start monitoring
        monitor_task = asyncio.create_task(
            self.monitor.start_agents()
        )
        
        # Initialize training
        training_task = asyncio.create_task(
            self.training_coordinator.coordinate_enhanced_training(self.config['market_data'])
        )
        
        # Wait for both tasks
        await asyncio.gather(monitor_task, training_task)

# Example usage
async def main():
    config = {
        'api_key': 'GC7TAP6TZJ91HA84',
        'quantum_params': {
            'micro_lag': 0.000009,
            'wavelet_base': 17,
            'compton_base': 43.00826,
            'entropy_weight': 0.85,
            'coherence_threshold': 1.014000,
            'hma_length': 53
        },
        'market_data': {}  # Will be populated with API data
    }
    
    initializer = SystemInitializer(config)
    await initializer.initialize_system()

if __name__ == "__main__":
    asyncio.run(main())