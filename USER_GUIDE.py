"""
Iconora Studio - User Guide & Tutorial
دليل المستخدم والشرح التفصيلي

Complete step-by-step guide for all features
"""

USER_GUIDE = {
    "quick_start": {
        "title": "🚀 Quick Start Guide",
        "intro": "Get started with Iconora Studio in 5 minutes",

        "step_1": {
            "title": "Download & Install",
            "instructions": [
                "1. Visit https://iconora.com/download",
                "2. Click 'Download Demo' (free)",
                "3. Run the installer",
                "4. Follow on-screen instructions",
                "5. Launch the application"
            ],
            "time": "2 minutes"
        },

        "step_2": {
            "title": "First Project",
            "instructions": [
                "1. Click '💾 New Project'",
                "2. Name your project (e.g., 'My First Design')",
                "3. Choose a template or start blank",
                "4. You're ready to create!"
            ],
            "time": "1 minute"
        },

        "step_3": {
            "title": "Create Your First Icon",
            "instructions": [
                "1. Go to '💾 Icon Converter' tab",
                "2. Click 'Upload Icon'",
                "3. Select your image (PNG, JPG, SVG)",
                "4. Set output sizes (web: 32px, 64px, 128px)",
                "5. Click 'Export' to download all sizes"
            ],
            "time": "1 minute",
            "note": "Icon Converter available in Demo mode"
        },

        "step_4": {
            "title": "Upgrade to Pro (Optional)",
            "instructions": [
                "1. Click 'ℹ️ About' tab",
                "2. Click '🔓 Activate License'",
                "3. Enter your name",
                "4. Select 'Pro' edition",
                "5. Click 'Generate Key'",
                "6. Click 'Activate'",
                "7. App restarts with all features unlocked!"
            ],
            "time": "1 minute",
            "cost": "One-time $29"
        }
    },

    "features_guide": {
        "icon_converter": {
            "title": "💾 Icon Converter",
            "description": "Convert single icons to multiple sizes automatically",
            "available_in": ["Demo", "Pro", "Enterprise"],

            "steps": [
                {
                    "title": "Upload Icon",
                    "action": "Click 'Upload' button",
                    "formats": ["PNG", "JPG", "SVG", "GIF"],
                    "max_size": "50 MB"
                },
                {
                    "title": "Select Sizes",
                    "option": "Choose from presets or custom",
                    "presets": {
                        "web": "32, 64, 128, 256, 512 pixels",
                        "mobile": "48, 72, 96, 192 pixels",
                        "favicon": "16, 32, 64, 128 pixels",
                        "apple": "120, 152, 167, 180 pixels"
                    }
                },
                {
                    "title": "Export",
                    "formats": ["PNG", "JPG", "WebP"],
                    "output": "ZIP file with all sizes"
                }
            ],

            "tips": [
                "Use square images (512×512 is ideal)",
                "Transparent PNGs preserve background",
                "SVG files scale without quality loss",
                "Export as PNG for web, JPG for print"
            ]
        },

        "svg_converter": {
            "title": "🎨 SVG Converter",
            "description": "Convert raster images to scalable SVG format",
            "available_in": ["Pro", "Enterprise"],
            "pro_feature": True,

            "steps": [
                {
                    "title": "Upload Image",
                    "formats": ["PNG", "JPG", "BMP", "GIF"],
                    "tips": ["High contrast images work best", "Avoid noisy backgrounds"]
                },
                {
                    "title": "Adjust Settings",
                    "options": {
                        "color_depth": "Number of colors to preserve (1-256)",
                        "smoothness": "Smooth vs detailed paths",
                        "threshold": "Color detection sensitivity"
                    }
                },
                {
                    "title": "Preview",
                    "action": "See result before export",
                    "adjust": "Fine-tune settings if needed"
                },
                {
                    "title": "Export SVG",
                    "format": "Scalable Vector Graphics",
                    "uses": ["Web icons", "Print logos", "Animation assets"]
                }
            ],

            "use_cases": [
                "Convert logo mockups to vectors",
                "Create infinite-scale icons",
                "Prepare art for animation",
                "Professional design handoff"
            ]
        },

        "logo_designer": {
            "title": "🖼️ Logo Designer",
            "description": "Create professional logos in minutes",
            "available_in": ["Pro", "Enterprise"],
            "pro_feature": True,

            "steps": [
                {
                    "title": "Choose Style",
                    "styles": [
                        "Modern Minimalist",
                        "Classic Elegant",
                        "Bold Creative"
                    ]
                },
                {
                    "title": "Customize Design",
                    "options": {
                        "text": "Your company/brand name",
                        "colors": "Choose from 100+ color schemes",
                        "icon": "Pick from 1000+ icons",
                        "font": "Select from 220 professional fonts"
                    }
                },
                {
                    "title": "Advanced Options",
                    "features": {
                        "shadows": "Add depth with drop shadows",
                        "gradients": "Smooth color transitions",
                        "effects": "Blur, glow, emboss effects",
                        "layout": "Adjust spacing and alignment"
                    }
                },
                {
                    "title": "Export",
                    "formats": ["PNG", "SVG", "PDF", "JPG"],
                    "resolutions": ["1x (screen)", "2x", "4x (print)"]
                }
            ],

            "tips": [
                "Keep logos simple (works at any size)",
                "Avoid too many colors (2-3 is ideal)",
                "Test on both light and dark backgrounds",
                "Save multiple variations"
            ]
        },

        "signature_engine": {
            "title": "✍️ Signature Engine",
            "description": "Generate professional digital signatures",
            "available_in": ["Pro", "Enterprise"],
            "pro_feature": True,

            "styles": [
                "Handwritten script",
                "Formal calligraphy",
                "Modern geometric",
                "Artistic flourish",
                "Minimalist elegant"
            ],

            "customization": {
                "name": "Your full name or initials",
                "style": "Choose signature style",
                "pen": "Pen thickness and intensity",
                "color": "Ink color selection",
                "background": "Transparent or custom color"
            },

            "export": {
                "png": "For emails and documents",
                "svg": "For web and scaling",
                "pdf": "For printing",
                "gif": "Animated signature (Pro+)"
            },

            "use_cases": [
                "Email signature blocks",
                "Document authentication",
                "Contract signing",
                "Professional branding",
                "Legal documents"
            ],

            "tips": [
                "Initials-only signatures look more professional",
                "Match signature style to brand personality",
                "Test in Outlook/Gmail before use",
                "Remove background for emails"
            ]
        },

        "palette_generator": {
            "title": "🎯 Palette Generator",
            "description": "AI-powered color scheme generation",
            "available_in": ["Pro", "Enterprise"],
            "pro_feature": True,

            "features": [
                "6 palette sets per generation",
                "Harmony algorithms (complementary, analogous, triadic)",
                "Accessibility checking (WCAG compliance)",
                "Export to CSS, JSON, Figma",
                "Save favorites for future use"
            ],

            "how_to_use": [
                "1. Select base color (main brand color)",
                "2. Choose harmony type:",
                "   - Monochromatic: Shades of one color",
                "   - Complementary: Opposite color contrast",
                "   - Analogous: Similar adjacent colors",
                "   - Triadic: Three equally spaced colors",
                "3. Generate palette (AI creates smart sets)",
                "4. Export in preferred format",
                "5. Use in your designs!"
            ],

            "export_formats": {
                "css": "CSS variable format",
                "json": "JSON color codes",
                "figma": "Import directly to Figma",
                "figma_plugin": "1-click Figma import",
                "csv": "Excel/Google Sheets compatible",
                "tailwind": "Tailwind CSS configuration"
            },

            "tips": [
                "Use complementary colors for high contrast",
                "Test palettes in your actual designs",
                "Check WCAG accessibility scores",
                "Save successful palettes for consistency"
            ]
        },

        "project_manager": {
            "title": "📁 Project Manager",
            "description": "Organize and manage all your designs",
            "available_in": ["Pro", "Enterprise"],
            "pro_feature": True,

            "features": [
                "Create projects to organize designs",
                "Save design history and versions",
                "Tag and search designs",
                "Export project as ZIP",
                "Collaborate with team (Enterprise)",
                "Version control (auto-save every 5 minutes)"
            ],

            "workflow": [
                {
                    "step": "Create Project",
                    "action": "File → New Project",
                    "details": "Name, description, and color coding"
                },
                {
                    "step": "Save Designs",
                    "action": "File → Save",
                    "auto_save": "Every design change is auto-saved"
                },
                {
                    "step": "Organize",
                    "action": "Right-click → Add Tag",
                    "tags": "Client name, project type, status"
                },
                {
                    "step": "Export Project",
                    "action": "File → Export Project",
                    "output": "ZIP with all designs + metadata"
                }
            ]
        }
    },

    "license_guide": {
        "understanding_licenses": {
            "demo_edition": {
                "cost": "Free",
                "features": [
                    "Icon Converter (full)",
                    "Upload up to 5 icons per day",
                    "Basic export options"
                ],
                "limitations": [
                    "❌ SVG Converter",
                    "❌ Logo Designer",
                    "❌ Signature Engine",
                    "❌ Palette Generator",
                    "❌ Project Manager",
                    "❌ Batch Operations"
                ],
                "duration": "Forever",
                "upgrade_path": "Buy Pro license anytime"
            },

            "pro_edition": {
                "cost": "$29 one-time",
                "features": [
                    "✅ All Demo features",
                    "✅ SVG Converter",
                    "✅ Logo Designer (3 styles)",
                    "✅ Signature Engine (5 styles)",
                    "✅ Palette Generator (6 sets)",
                    "✅ Project Manager",
                    "✅ Batch Operations (10 items)",
                    "✅ Unlimited exports",
                    "✅ Premium fonts (220+)",
                    "✅ Lifetime updates"
                ],
                "best_for": "Freelancers, designers, entrepreneurs",
                "roi": "Pays for itself in 2-3 projects"
            },

            "enterprise_edition": {
                "cost": "$99 one-time",
                "features": [
                    "✅ All Pro features",
                    "✅ REST API access",
                    "✅ Priority support (1-hour response)",
                    "✅ Custom fonts upload",
                    "✅ Advanced batch (unlimited)",
                    "✅ Team collaboration",
                    "✅ Custom branding",
                    "✅ White-label option",
                    "✅ Dedicated account manager"
                ],
                "best_for": "Design agencies, corporations, teams",
                "annual_equivalent": "$120/year tool"
            }
        },

        "activation_guide": {
            "step_1": "Click ℹ️ About tab",
            "step_2": "Click 🔓 Activate License button",
            "step_3": "Enter your name",
            "step_4": "Select Pro or Enterprise",
            "step_5": "Click Generate Key button",
            "step_6": "Copy the license key",
            "step_7": "Click Activate button",
            "step_8": "Application restarts with features unlocked!",
            "success_message": "🎉 License activated! Enjoy all Pro features!"
        },

        "license_requirements": {
            "one_time_purchase": "No monthly fees or renewals",
            "lifetime_access": "Use forever once purchased",
            "automatic_updates": "Get all updates for free",
            "device_limit": "1 license per person (as per terms)",
            "family_use": "Family members can use on shared computer"
        }
    },

    "troubleshooting": {
        "app_wont_start": {
            "problem": "Application crashes on startup",
            "solutions": [
                "1. Ensure Windows 10+ is installed",
                "2. Update graphics drivers",
                "3. Disable antivirus temporarily (some block new software)",
                "4. Run as Administrator",
                "5. Check if port 5000 is available",
                "6. Contact support: support@iconora.com"
            ]
        },

        "export_fails": {
            "problem": "Cannot export designs",
            "solutions": [
                "1. Check disk space (need 100MB minimum)",
                "2. Verify output folder has write permissions",
                "3. Try different export format",
                "4. Close other applications using the file",
                "5. Restart the application",
                "6. Try export to Desktop instead"
            ]
        },

        "license_not_activating": {
            "problem": "License key won't activate",
            "solutions": [
                "1. Check internet connection (required for first activation)",
                "2. Ensure license.key file not corrupted (delete and try again)",
                "3. Use exact name from license generation",
                "4. Double-check key for typos",
                "5. Try offline mode (works after first activation)",
                "6. Contact support with key details"
            ]
        },

        "slow_performance": {
            "problem": "App running slowly",
            "optimizations": [
                "1. Close background applications",
                "2. Update to latest version",
                "3. Clear project cache: File → Settings → Clear Cache",
                "4. Disable visual effects: Windows → Theme → Light Mode",
                "5. Increase available RAM (close browser tabs)",
                "6. Check for Windows updates"
            ]
        }
    },

    "tips_and_tricks": [
        "✨ Keyboard Shortcut: Ctrl+S = Quick save",
        "✨ Undo/Redo: Ctrl+Z / Ctrl+Y",
        "✨ Copy/Paste: Ctrl+C / Ctrl+V to copy designs between projects",
        "✨ Zoom: Scroll wheel to zoom in/out",
        "✨ Dark Mode: Settings → Theme → Dark Mode",
        "✨ Batch Export: Design → Batch Export selected items",
        "✨ Template Library: Browse 100+ pre-made templates",
        "✨ Font Search: Type to filter fonts from 220+ options",
        "✨ Color History: Recently used colors appear in color picker",
        "✨ Favorite Designs: Star designs for quick access"
    ],

    "faqs": {
        "can_i_use_commercially": {
            "question": "Can I use created designs for commercial work?",
            "answer": "Yes! All designs you create are 100% yours to use commercially with Pro or Enterprise license."
        },

        "is_internet_required": {
            "question": "Do I need internet to use Iconora Studio?",
            "answer": "No, the application works offline. Internet is only needed for initial license activation."
        },

        "can_i_use_on_mac_linux": {
            "question": "Is there a Mac or Linux version?",
            "answer": "Currently Windows only. Mac version in development for 2026."
        },

        "whats_the_refund_policy": {
            "question": "What's the refund policy?",
            "answer": "30-day money-back guarantee on Pro and Enterprise licenses. No questions asked."
        },

        "can_i_get_support": {
            "question": "How do I get support?",
            "answer": "Pro users: Email support (24-48h). Enterprise: Priority (1-hour). All users: Knowledge base & FAQ."
        }
    }
}

if __name__ == "__main__":
    print("=" * 80)
    print("ICONORA STUDIO - COMPREHENSIVE USER GUIDE")
    print("=" * 80)

    print("\n🚀 Quick Start:")
    for step, content in USER_GUIDE["quick_start"].items():
        if "step" in step:
            print(f"   {content['title']} ({content['time']})")

    print("\n📚 Features Available:")
    for feature, details in USER_GUIDE["features_guide"].items():
        print(f"   • {details['title']} - {details['description']}")

    print("\n💳 License Options:")
    for license_type, details in USER_GUIDE["license_guide"]["understanding_licenses"].items():
        if "edition" in license_type:
            print(f"   • {details['cost']:>10} - {license_type.replace('_', ' ').title()}")

    print("\n📖 See full guide in USER_GUIDE.py")
    print("=" * 80)
