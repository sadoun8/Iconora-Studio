"""
Iconora Studio - Performance Enhancement Patches
تحسينات الأداء المتقدمة

This file contains optimized versions of key functions
that use the new TaskExecutor for better performance.
"""

import customtkinter as ctk
from tkinter import messagebox
from core.task_executor import TaskExecutor, ProgressCallback
import time
import os


class EnhancedIconConverter:
    """تحسينات محرك تحويل الأيقونات - Enhanced Icon Converter functions"""

    @staticmethod
    def create_progress_bar(parent) -> tuple:
        """أنشئ شريط تقدم احترافي - Create professional progress bar"""

        frame = ctk.CTkFrame(parent)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="⚙️ Processing...",
            font=("Segoe UI Variable Display", 14, "bold")
        )
        title.pack(pady=(10, 5))

        # Progress bar
        progress_bar = ctk.CTkProgressBar(frame)
        progress_bar.set(0)
        progress_bar.pack(fill="x", padx=20, pady=5)

        # Percentage text
        percent_label = ctk.CTkLabel(
            frame,
            text="0%",
            font=("Segoe UI Variable Text", 11),
            text_color=("#667EEA", "#667EEA")
        )
        percent_label.pack(pady=2)

        # Status message
        status_label = ctk.CTkLabel(
            frame,
            text="Starting...",
            font=("Segoe UI Variable Text", 10),
            text_color="gray"
        )
        status_label.pack()

        # Time estimate
        time_label = ctk.CTkLabel(
            frame,
            text="",
            font=("Segoe UI Variable Text", 9),
            text_color="gray"
        )
        time_label.pack()

        # Cancel button
        cancel_btn = ctk.CTkButton(
            frame,
            text="Cancel",
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            height=32,
            corner_radius=8
        )
        cancel_btn.pack(pady=10)

        return frame, progress_bar, percent_label, status_label, time_label, cancel_btn

    @staticmethod
    def convert_with_progress(
        converter,
        output_path: str,
        selected_sizes: list,
        quality: int,
        progress_callback: ProgressCallback = None,
        on_complete=None
    ):
        """تحويل مع شريط تقدم - Convert icons with progress tracking"""

        try:
            total_steps = len(selected_sizes) + 2

            if progress_callback:
                progress_callback.update(0, "Loading image...")

            # Step 1: Reset and apply logic
            converter.reset_image()

            if progress_callback:
                progress_callback.update(1, " التحضير...")

            time.sleep(0.1)  # Let UI update

            # Step 2: Convert each size
            size_tuples = [(s, s) for s in selected_sizes]

            for i, size_tuple in enumerate(size_tuples):
                if progress_callback:
                    progress_callback.update(
                        i + 2,
                        f"Converting to {size_tuple[0]}×{size_tuple[1]}..."
                    )
                time.sleep(0.05)  # Simulate processing, real work happens in convert_to_ico

            # Step 3: Actual conversion
            converter.convert_to_ico(output_path, sizes=size_tuples, quality=quality)

            if progress_callback:
                progress_callback.update(total_steps, "Complete!")

            return {
                "success": True,
                "path": output_path,
                "message": f"Icon saved at:\n{output_path}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def export_pngs_with_progress(
        converter,
        output_folder: str,
        progress_callback: ProgressCallback = None
    ):
        """تصدير PNG مع شريط تقدم - Export PNGs with progress tracking"""

        try:
            if progress_callback:
                progress_callback.update(0, "Preparing...")

            converter.reset_image()

            if progress_callback:
                progress_callback.update(10, "Processing sizes...")

            time.sleep(0.1)

            converter.export_all_sizes(output_folder)

            if progress_callback:
                progress_callback.update(100, "Complete!")

            return {
                "success": True,
                "folder": output_folder,
                "message": f"PNGs saved in:\n{output_folder}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# ─────────────────────────────────────────────────────────────────────────────
# PATCH FUNCTIONS - استخدمها لتحديث الدوال الموجودة
# ─────────────────────────────────────────────────────────────────────────────

def patch_icon_tab_convert(icon_tab_instance):
    """
    طبّق تحسينات التحويل - Apply conversion enhancements to IconConverterTab

    Usage:
        from legacy_ui.icon_tab import IconConverterTab
        from core.enhancement_patches import patch_icon_tab_convert

        tab = IconConverterTab(parent)
        patch_icon_tab_convert(tab)  # Now it uses the new system!
    """

    original_convert = icon_tab_instance._convert
    executor = TaskExecutor(max_workers=2)
    icon_tab_instance._executor = executor

    def _convert_enhanced(self):
        if not self.input_path:
            from tkinter import messagebox
            messagebox.showwarning("Warning", "Select image first")
            return

        selected_sizes = [s for s, v in self.size_vars.items() if v.get()]
        if not selected_sizes:
            messagebox.showwarning("Warning", "Select at least one size")
            return

        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            defaultextension=".ico",
            filetypes=[("Icon", "*.ico")],
            initialfile=os.path.splitext(os.path.basename(self.input_path))[0] + ".ico"
        )

        if not path:
            return

        # Create progress bar
        prog_frame, progress_bar, percent_label, status_label, time_label, cancel_btn = \
            EnhancedIconConverter.create_progress_bar(self.controls_frame)
        prog_frame.pack(fill="x", padx=15, pady=10)

        # Track progress
        progress = ProgressCallback(len(selected_sizes) + 2)
        start_time = time.time()

        def update_progress(data):
            def _apply_ui_update():
                if not self.winfo_exists():
                    return
                progress_bar.set(data["percentage"] / 100.0)
                percent_label.configure(text=f"{data['percentage']}%")
                status_label.configure(text=data["message"])

                # Estimate remaining time
                elapsed = time.time() - start_time
                if data["percentage"] > 0:
                    total_est = (elapsed / data["percentage"]) * 100
                    remaining = int(total_est - elapsed)
                    time_label.configure(text=f"⏱️  Remaining: ~{remaining}s")

            self.after(0, _apply_ui_update)

        progress.add_listener(update_progress)

        # Cancel functionality
        cancelled = False
        def on_cancel():
            nonlocal cancelled
            cancelled = True
            cancel_btn.configure(state="disabled")

        cancel_btn.configure(command=on_cancel)

        # Submit task
        quality = int(self.quality_slider_attr.get())

        def conversion_task():
            self._reapply_logic()
            return EnhancedIconConverter.convert_with_progress(
                self.converter,
                path,
                selected_sizes,
                quality,
                progress
            )

        def on_complete(result):
            def _finalize_ui():
                if not self.winfo_exists():
                    return
                prog_frame.destroy()
                self.btn_convert.configure(state="normal", text="🚀 Generate ICO")

                if result.success:
                    messagebox.showinfo("Success", result.result["message"])
                else:
                    messagebox.showerror("Error", result.result["error"])

            self.after(0, _finalize_ui)

        self.btn_convert.configure(state="disabled", text="Processing...")
        executor.submit_task(conversion_task, on_complete=on_complete)

    # Replace the method
    import types
    icon_tab_instance._convert = types.MethodType(_convert_enhanced, icon_tab_instance)


def patch_icon_tab_export_pngs(icon_tab_instance):
    """طبّق تحسينات التصدير - Apply export enhancements"""

    executor = icon_tab_instance._executor if hasattr(icon_tab_instance, '_executor') else TaskExecutor(max_workers=2)
    icon_tab_instance._executor = executor

    def _export_pngs_enhanced(self):
        if not self.input_path:
            from tkinter import messagebox
            messagebox.showwarning("Warning", "Select image first")
            return

        from tkinter import filedialog
        folder = filedialog.askdirectory(title="Select Output Folder")
        if not folder:
            return

        # Create progress bar
        prog_frame, progress_bar, percent_label, status_label, time_label, cancel_btn = \
            EnhancedIconConverter.create_progress_bar(self.controls_frame)
        prog_frame.pack(fill="x", padx=15, pady=10)

        progress = ProgressCallback(100)

        def update_progress(data):
            def _apply_ui_update():
                if not self.winfo_exists():
                    return
                progress_bar.set(data["percentage"] / 100.0)
                percent_label.configure(text=f"{data['percentage']}%")
                status_label.configure(text=data["message"])

            self.after(0, _apply_ui_update)

        progress.add_listener(update_progress)

        def export_task():
            self._reapply_logic()
            return EnhancedIconConverter.export_pngs_with_progress(
                self.converter,
                folder,
                progress
            )

        def on_complete(result):
            def _finalize_ui():
                if not self.winfo_exists():
                    return
                prog_frame.destroy()
                self.btn_export_png.configure(state="normal")

                if result.success:
                    messagebox.showinfo("Success", result.result["message"])
                else:
                    messagebox.showerror("Error", result.result["error"])

            self.after(0, _finalize_ui)

        self.btn_export_png.configure(state="disabled")
        executor.submit_task(export_task, on_complete=on_complete)

    import types
    icon_tab_instance._export_pngs = types.MethodType(_export_pngs_enhanced, icon_tab_instance)


# ─────────────────────────────────────────────────────────────────────────────
# Performance monitoring utilities
# ─────────────────────────────────────────────────────────────────────────────

class PerformanceMonitor:
    """مراقب الأداء - Monitor application performance"""

    def __init__(self):
        self.metrics = {
            "conversions": 0,
            "exports": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
        }

    def record_operation(self, operation_type: str, duration: float):
        """سجّل عملية - Record an operation"""
        self.metrics["total_time"] += duration

        if operation_type == "conversion":
            self.metrics["conversions"] += 1
        elif operation_type == "export":
            self.metrics["exports"] += 1

        total_ops = self.metrics["conversions"] + self.metrics["exports"]
        if total_ops > 0:
            self.metrics["avg_time"] = self.metrics["total_time"] / total_ops

    def get_stats(self) -> dict:
        """احصل على الإحصائيات - Get statistics"""
        return dict(self.metrics)

    def print_report(self):
        """اطبع تقرير - Print performance report"""
        stats = self.get_stats()
        print(f"\n{'='*50}")
        print(f"📊 Performance Report")
        print(f"{'='*50}")
        print(f"Total Conversions: {stats['conversions']}")
        print(f"Total Exports: {stats['exports']}")
        print(f"Total Time: {stats['total_time']:.2f}s")
        print(f"Average Time per Op: {stats['avg_time']:.2f}s")
        print(f"{'='*50}\n")


# Create global monitor
performance_monitor = PerformanceMonitor()
