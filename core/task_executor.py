"""
Iconora Studio - Advanced Task Execution System
نظام تنفيذ المهام المتقدم

This module provides a professional threading architecture for
handling heavy operations without freezing the UI.
"""

from threading import Thread, Lock
from queue import Queue, Empty
from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass
import uuid
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    """نتيجة المهمة - Result of task execution"""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration: float = 0.0

    def __post_init__(self):
        if self.result is None:
            self.result = {}


class ProgressCallback:
    """نموذج التقدم - Progress tracking system"""

    def __init__(self, total_steps: int = 100):
        self.total = max(1, total_steps)
        self.current = 0
        self.listeners = []
        self.lock = Lock()

    def add_listener(self, callback: Callable[[Dict], None]):
        """أضف مستمع - Add progress listener"""
        self.listeners.append(callback)

    def update(self, step: int, message: str = ""):
        """حدّث التقدم - Update progress"""
        with self.lock:
            self.current = min(step, self.total)
            percentage = int((self.current / self.total) * 100)

            progress_data = {
                "percentage": percentage,
                "message": message,
                "step": self.current,
                "total": self.total,
            }

            for listener in self.listeners:
                try:
                    listener(progress_data)
                except Exception as e:
                    logger.error(f"Progress listener error: {e}")


class TaskExecutor:
    """
    معالج المهام المتقدم - Advanced Task Executor

    Executes heavy operations in background threads without
    freezing the main UI thread.
    """

    def __init__(self, max_workers: int = 4, on_error: Callable = None):
        """Initialize TaskExecutor"""
        self.max_workers = max_workers
        self.task_queue: Queue = Queue()
        self.result_callbacks: Dict[str, Callable] = {}
        self.progress_callbacks: Dict[str, ProgressCallback] = {}
        self.active_tasks: Dict[str, Dict] = {}
        self.on_error = on_error
        self.lock = Lock()
        self.running = True

        # Start worker threads
        self.workers = []
        self._start_workers()

        logger.info(f"TaskExecutor started with {max_workers} workers")

    def _start_workers(self):
        """بدء خيوط العمل - Start worker threads"""
        for i in range(self.max_workers):
            worker = Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)

    def _worker_loop(self):
        """حلقة العامل - Main worker loop"""
        while self.running:
            try:
                try:
                    task = self.task_queue.get(timeout=1)
                except Empty:
                    continue

                if task is None:
                    self.task_queue.task_done()
                    break

                task_id, func, args, kwargs = task
                start_time = time.time()

                with self.lock:
                    if task_id in self.active_tasks:
                        self.active_tasks[task_id]["status"] = "running"

                try:
                    # Execute task
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time

                    result_obj = TaskResult(
                        task_id=task_id,
                        success=True,
                        result=result,
                        duration=duration
                    )

                except Exception as e:
                    duration = time.time() - start_time
                    result_obj = TaskResult(
                        task_id=task_id,
                        success=False,
                        error=str(e),
                        duration=duration
                    )

                    if self.on_error:
                        try:
                            self.on_error(result_obj)
                        except Exception as callback_error:
                            logger.error(f"on_error callback failed: {callback_error}")

                # Call result callback
                with self.lock:
                    callback = self.result_callbacks.pop(task_id, None)
                    self.progress_callbacks.pop(task_id, None)
                    self.active_tasks.pop(task_id, None)

                if callback:
                    try:
                        callback(result_obj)
                    except Exception as e:
                        logger.error(f"Result callback error: {e}")

                self.task_queue.task_done()

            except Exception as e:
                logger.error(f"Worker loop error: {e}")

    def submit_task(
        self,
        func: Callable,
        args: tuple = (),
        kwargs: Dict = None,
        on_complete: Callable = None,
        task_id: str = None,
        name: str = None
    ) -> str:
        """أرسل مهمة للمعالجة - Submit task for execution"""
        task_id = task_id or str(uuid.uuid4())
        kwargs = kwargs or {}

        with self.lock:
            if task_id in self.active_tasks:
                logger.warning(f"Task {task_id} already exists")
                return task_id

            self.active_tasks[task_id] = {
                "status": "queued",
                "name": name or func.__name__,
                "created": time.time()
            }

            if on_complete:
                self.result_callbacks[task_id] = on_complete

        self.task_queue.put((task_id, func, args, kwargs))
        return task_id

    def create_progress_tracker(self, task_id: str, total_steps: int = 100) -> ProgressCallback:
        """أنشئ متتبع تقدم - Create progress tracker for task"""
        tracker = ProgressCallback(total_steps)
        with self.lock:
            self.progress_callbacks[task_id] = tracker
        return tracker

    def get_progress(self, task_id: str) -> Optional[Dict]:
        """احصل على التقدم - Get task progress"""
        with self.lock:
            if task_id in self.progress_callbacks:
                tracker = self.progress_callbacks[task_id]
                percentage = int((tracker.current / tracker.total) * 100)
                return {
                    "percentage": percentage,
                    "step": tracker.current,
                    "total": tracker.total,
                }
        return None

    def shutdown(self, wait: bool = True):
        """إيقاف المعالج - Shutdown executor"""
        self.running = False

        # Send shutdown signals
        for _ in range(self.max_workers):
            self.task_queue.put(None)

        if wait:
            for worker in self.workers:
                worker.join(timeout=5)

        logger.info("TaskExecutor shutdown")
