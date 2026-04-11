# Plan: Enhance Interaction, Fix Signature Bug, and Localize Menus

## Tasks
1.  **Fix Signature Generator Bug**: Resolve `'SignatureTab' object has no attribute '_sep'`.
2.  **Localize Internal Menus**: Translate menus and UI elements to Arabic.
3.  **Mouse Interaction**: Implement dragging/moving of text and elements using the mouse.

## Workflow Steps

### [x] Step: Investigation and Planning
Analyze the requirements and code to design solutions.
1.  Investigate `SignatureTab` for the `_sep` attribute error.
2.  Identify hardcoded strings in menus and UI that need localization.
3.  Research how to implement mouse dragging on `customtkinter` or `tkinter` canvas/widgets for the logo/icon preview.
4.  Propose technical solutions for each.

### [x] Step: Implementation - Phase 1: Bug Fix and Localization
1.  Fix the `SignatureTab` bug.
2.  Update `i18n.py` and UI files to ensure all menus are localized.
3.  Verify fixes.

### [x] Step: Implementation - Phase 2: Mouse Interaction
1.  Implement mouse event bindings for moving text/elements in the Logo/Icon tabs.
2.  Update the processing logic to account for the new positions.

### [x] Step: Implementation - Phase 3: Advanced Enhancements
1.  **Signature Studio**: Add manual-style ornaments (diagonal lines, curved strokes).
2.  **Icon Studio**: Implement mouse dragging for text and optimize performance.
3.  **Logo Designer**: Upgrade color templates with professional gradients (Gold, Luxury Green, etc.).
4.  **Localization**: Conduct a final audit for any remaining English strings.

### [x] Step: Verification
1.  Test new ornaments in Signature Generator.
2.  Verify mouse dragging and performance in Icon Tab.
3.  Check new professional templates in Logo Designer.
4.  Verify final localization.
5.  Run build and verify in the executable.

### [x] Step: Implementation - Phase 4: Creative Tools and Universal Input
1.  **Touchscreen Support**: Ensure all interactive previews respond to touch events (drag, tap-to-select).
2.  **Universal Control**: Implement a unified manipulation system (mouse & touch) for all designers (Logo, Icon, Signature).
3.  **Creative Templates**: Implement a template gallery for quick design presets.
4.  **Visual Effects**: Add support for shadows, glows, and background textures in designing tabs.
5.  **Decorative Fonts**: Integrate additional high-quality, decorative Arabic fonts.

### [x] Step: Implementation - Phase 5: Advanced Connectivity and Format Support
1.  **Multi-Format Support**: Add WebP and PDF export options to Icon, Logo, and Signature designers. [COMPLETED]
2.  **SVG Pro**: Enhance the SVG converter with path color selection and background transparency control. [COMPLETED]
3.  **Signature Library**: Implement a local gallery to save and reuse signatures. [COMPLETED]
4.  **Logo Watermarking**: Add a feature to quickly apply generated logos as watermarks on images. [COMPLETED]
