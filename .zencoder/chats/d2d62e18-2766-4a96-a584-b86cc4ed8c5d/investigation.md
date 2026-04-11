# Investigation: Interaction, Signature Bug, and Localization

## 1. Signature Generator Bug
- **Bug**: `'SignatureTab' object has no attribute '_sep'`
- **Root Cause**: The `SignatureTab._build_ui` method calls `self._sep(ctrl)` multiple times, but `_sep` is not defined within the `SignatureTab` class.
- **Solution**: Implement a `_sep` method in `SignatureTab` that adds a vertical separator or padding to the control panel, similar to how it's likely intended to look based on other tabs.

## 2. Localization
- **Issue**: Many UI strings in `LogoDesignerTab`, `SignatureTab`, and potentially others are hardcoded in English.
- **Affected Components**:
    - `ui/signature_tab.py`: Hardcoded section headers like "Typography Settings", "Artistic Adjustments", etc.
    - `ui/logo_tab.py`: Hardcoded labels like "General Settings", "Typography & Position", "Effects", etc.
- **Solution**: 
    - Add missing keys to `i18n.py`.
    - Replace hardcoded strings in `.py` files with `tr("key")`.

## 3. Mouse Interaction (Dragging)
- **Feature**: Ability to move text/elements by dragging the mouse over the preview.
- **Implementation Strategy**:
    - **Logo Designer**: 
        - Bind `<Button-1>`, `<B1-Motion>`, and `<ButtonRelease-1>` to the preview label (`self.preview_label`).
        - In `<Button-1>`, record the starting mouse position.
        - In `<B1-Motion>`, calculate the delta and update the `x_slider` and `y_slider` values.
        - Updating sliders will automatically trigger `_preview()`, providing real-time feedback.
    - **Icon Converter**: Similar approach for text overlay if applicable.
    - **Signature Generator**: Similar approach for text positioning if needed (need to check if `SignatureEngine` supports offsets).

## Implementation Notes
1.  **Signature Bug Fix**: Implemented `_sep` and `_hex` helpers in `SignatureTab`.
2.  **Localization**: 
    - Updated `i18n.py` with missing keys for Logo and Signature tabs.
    - Replaced hardcoded strings in `LogoDesignerTab`, `SignatureTab`, and `IconConverterTab`.
    - Localized labels for Canvas size, Typography settings, Artistic adjustments, etc.
3.  **Mouse Interaction**:
    - Implemented drag-to-move for Logo Designer preview.
    - Bound `<Button-1>`, `<B1-Motion>`, and `<ButtonRelease-1>` events.
    - Updating sliders in real-time during drag for instant visual feedback.
    - Added bilingual drag hint to Logo Designer tab.
