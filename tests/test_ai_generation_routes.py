import unittest

from backend.api.routes_ai import (
    build_ai_prompt,
    compose_generation_debug,
    get_generation_dimensions,
    sanitize_prompt,
    wants_arabic_script,
)


class AiGenerationRouteTests(unittest.TestCase):
    def test_signature_prompt_uses_signature_specific_negative_terms(self) -> None:
        prompt = build_ai_prompt("Signature for Baw Aliwin", "signature")

        self.assertIn("Professional handwritten signature", prompt)
        self.assertIn("no portrait", prompt)
        self.assertIn("no icon", prompt)
        self.assertIn("Baw Aliwin", prompt)

    def test_signature_prompt_preserves_arabic_script_when_requested(self) -> None:
        prompt = build_ai_prompt("Elegant Arabic signature for Mohammed", "signature", "توقيع عربي باسم محمد")

        self.assertIn("exact Arabic text", prompt)
        self.assertIn("محمد", prompt)
        self.assertIn("Do NOT transliterate", prompt)

    def test_signature_dimensions_use_landscape_ratio(self) -> None:
        self.assertEqual(get_generation_dimensions("signature"), (1536, 768))
        self.assertEqual(get_generation_dimensions("logo"), (1024, 1024))

    def test_sanitize_prompt_removes_arabic_prefixes_and_invisible_chars(self) -> None:
        self.assertEqual(sanitize_prompt("توقيع عربي باسم مح\u00adمد"), "محمد")

    def test_wants_arabic_script_detects_arabic_hints(self) -> None:
        self.assertTrue(wants_arabic_script("Elegant signature", "توقيع بخط عربي باسم محمد"))

    def test_compose_generation_debug_includes_signature_diagnostics(self) -> None:
        debug = compose_generation_debug(
            "Elegant Arabic signature for Mohammed",
            "signature",
            "توقيع عربي باسم محمد",
        )

        self.assertEqual(debug["section"], "signature")
        self.assertEqual(debug["display_name"], "محمد")
        self.assertTrue(debug["wants_arabic_script"])
        self.assertEqual(debug["width"], 1536)
        self.assertEqual(debug["height"], 768)
        self.assertIn("exact Arabic text", debug["final_prompt"])

    def test_compose_generation_debug_tracks_logo_subject_translation_inputs(self) -> None:
        debug = compose_generation_debug("Design a logo for Falcon", "logo", "Design a logo for Falcon")

        self.assertEqual(debug["section"], "logo")
        self.assertEqual(debug["sanitized_prompt"], "Falcon")
        self.assertEqual(debug["subject_source"], "Falcon")
        self.assertEqual(debug["translated_subject"], "Falcon")
        self.assertIn("Professional high-quality logo design of Falcon", debug["final_prompt"])

    def test_compose_generation_debug_extracts_signature_name_style_and_background(self) -> None:
        debug = compose_generation_debug(
            "توقيع الكتروني انيق ومزخرف باسم محمد على خلفيه داكنه",
            "signature",
            "توقيع الكتروني انيق ومزخرف باسم محمد على خلفيه داكنه",
        )

        self.assertEqual(debug["display_name"], "محمد")
        self.assertEqual(debug["style_hint"], "الكتروني انيق ومزخرف")
        self.assertEqual(debug["background_hint"], "dark")
        self.assertTrue(debug["background_conflict"])
        self.assertIn("dark charcoal background", debug["final_prompt"])
        self.assertIn("bright white or silver ink", debug["final_prompt"])


if __name__ == "__main__":
    unittest.main()
