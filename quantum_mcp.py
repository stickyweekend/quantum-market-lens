from rich.console import Console
from rich.panel import Panel
from datetime import datetime
from quantum_data_export import QuantumDataExporter

class QuantumMCPMonitor:
    def __init__(self):
        # Separate console for logs
        self.log_file = "quantum_training.log"
        self.log_console = Console(file=open(self.log_file, "a"))
        self.data_exporter = QuantumDataExporter()
        
    async def log_metrics(self, metrics, phase, validation_status):
        """Enhanced MCP logging with data export"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = Panel(
                f"[cyan]Phase: {phase}[/cyan]\n" +
                f"[green]Coherence: {metrics.get('coherence', 0):.3f}[/green]\n" +
                f"[yellow]Energy: {metrics.get('energy', 0):.3f}[/yellow]\n" +
                f"[magenta]Phase Metric: {metrics.get('phase', 0):.3f}[/magenta]",
                title=f"Quantum Metrics Update - {timestamp}"
            )
            
            # Write to separate log file
            self.log_console.print(log_entry)
            
            # Export metrics data
            self.data_exporter.log_training_event('metrics_history', {
                'phase': phase,
                'metrics': metrics,
                'validation_status': validation_status
            })
            
            # Track significant changes
            if self._is_significant_change(metrics):
                self._log_significant_change(metrics, phase, timestamp)
                
            # Enhanced validation logging
            if validation_status.get('transition_ready', False):
                await self._log_phase_transition(phase, metrics)
                
        except Exception as e:
            self.log_console.print(f"[red]Monitoring Error: {str(e)}[/red]")
            
    def _log_significant_change(self, metrics, phase, timestamp):
        """Log and export significant metric changes"""
        change_data = {
            'timestamp': timestamp,
            'metrics': metrics.copy(),
            'phase': phase
        }
        self.data_exporter.log_training_event('coherence_peaks', change_data)
        
        self.log_console.print(Panel(
            f"[bold yellow]Significant Change Detected[/bold yellow]\n" +
            f"Time: {timestamp}\n" +
            f"Phase: {phase}\n" +
            f"Metrics: {metrics}",
            title="Training Evolution"
        ))
        
    async def _log_phase_transition(self, current_phase, metrics):
        """Log and export phase transition events"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        transition_data = {
            'timestamp': timestamp,
            'from_phase': current_phase,
            'final_metrics': metrics.copy()
        }
        self.data_exporter.log_training_event('phase_transitions', transition_data)
        
        self.log_console.print(Panel(
            f"[bold blue]Phase Transition Event[/bold blue]\n" +
            f"Phase: {current_phase}\n" +
            f"Metrics: {metrics}",
            title="Training Progress"
        ))
        
    def _is_significant_change(self, metrics):
        """Check for significant metric changes"""
        if not self.data_exporter.training_data['coherence_peaks']:
            return True
            
        last_peak = self.data_exporter.training_data['coherence_peaks'][-1]['metrics']
        coherence_change = abs(metrics['coherence'] - last_peak['coherence'])
        return coherence_change > 0.05  # 5% change threshold

    def export_data(self, format='json'):
        """Export collected training data"""
        self.data_exporter.export_training_data(format)