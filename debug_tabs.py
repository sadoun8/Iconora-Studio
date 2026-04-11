from ui.main_window import MainWindow, TABS_AVAILABLE
print('TABS_AVAILABLE =', TABS_AVAILABLE)

# create window but do not call run (which enters mainloop)
try:
    win = MainWindow()
    print('MainWindow object created')
    # inspect tab_view children
    for child in win.root.winfo_children():
        print('root child:', child, type(child))
        # if this is a CTkTabview, try to list tabs or at least inspect attributes
        import customtkinter as _ctk
        if isinstance(child, _ctk.CTkTabview):
            print('  dir(tabview):', [a for a in dir(child) if not a.startswith('_')])
            # try to inspect internal _tabs property
            try:
                tabs = child._tabs
                print('  _tabs dict keys:', list(tabs.keys()))
            except Exception as e:
                print('  could not access _tabs:', e)
            # fallback: query underlying tk widget for tabs
            try:
                raw = child.tk.call(child._w, 'tabs')
                print('  tk tabs:', raw)
            except Exception as e:
                print('  could not call tk tabs', e)
        else:
            # fallback to check for generic tab_names method
            try:
                tabs = child.tab_names()
                print('  tab names:', tabs)
            except Exception:
                pass
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Exception during MainWindow creation:', e)
