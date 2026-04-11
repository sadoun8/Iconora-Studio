# core/progress.py - Professional Progress Tracking System

class ProgressTracker:
    """Tracks and broadcasts progress updates for long-running tasks."""

    def __init__(self, total_steps: int = 100):
        self.total = total_steps
        self.current = 0
        self.listeners = []
        self.last_message = ""

    def on_progress(self, callback):
        """Register a callback to be called on progress updates."""
        self.listeners.append(callback)

    def update(self, step: int, message: str = ""):
        """Updates the current progress and notifies all listeners."""
        self.current = step
        self.last_message = message
        
        # Calculate percentage
        percentage = 0
        if self.total > 0:
            percentage = int((self.current / self.total) * 100)
            percentage = max(0, min(100, percentage))
            
        # Prepare update packet
        update_data = {
            "percentage": percentage / 100.0, # 0.0 to 1.0 for CTkProgressBar
            "percent_label": f"{percentage}%",
            "message": message,
            "step": step,
            "total": self.total
        }
        
        # Notify listeners
        for listener in self.listeners:
            try:
                listener(update_data)
            except Exception as e:
                print(f"Progress listener error: {e}")

    def increment(self, amount: int = 1, message: str = None):
        """Increments current progress by a specific amount."""
        self.update(self.current + amount, message or self.last_message)

    def complete(self, message: str = "Complete!"):
        """Sets progress to 100%."""
        self.update(self.total, message)
