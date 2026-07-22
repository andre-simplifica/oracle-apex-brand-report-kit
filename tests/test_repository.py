from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "build-apex-brand-reports"
SCRIPTS = SKILL / "scripts"
EXAMPLE = ROOT / "examples" / "synthetic-company"


def run_script(name: str, *args: str, cwd: Path = ROOT, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *map(str, args)],
        cwd=cwd,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": str(SCRIPTS)},
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"{name} returned {result.returncode}, expected {expected}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def copy_config_fixture(directory: Path) -> Path:
    shutil.copy2(EXAMPLE / "brand-profile.json", directory / "brand-profile.json")
    shutil.copy2(EXAMPLE / "report-kit.yaml", directory / "report-kit.yaml")
    return directory / "report-kit.yaml"


class SkillTests(unittest.TestCase):
    def test_frontmatter_and_line_limit(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(text.splitlines()), 500)
        frontmatter = text.split("---", 2)[1]
        metadata = yaml.safe_load(frontmatter)
        self.assertEqual(set(metadata), {"name", "description"})
        self.assertEqual(metadata["name"], "build-apex-brand-reports")
        self.assertIn("Oracle APEX", metadata["description"])
        self.assertIn("XLSX", metadata["description"])

    def test_openai_metadata(self) -> None:
        metadata = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        interface = metadata["interface"]
        self.assertTrue(25 <= len(interface["short_description"]) <= 64)
        self.assertIn("$build-apex-brand-reports", interface["default_prompt"])

    def test_python_is_optional_tooling_not_an_apex_runtime_requirement(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        generic = (ROOT / "adapters" / "generic" / "README.md").read_text(encoding="utf-8")
        agent_native = (SKILL / "references" / "agent-native-workflow.md").read_text(encoding="utf-8")
        self.assertIn("Python is not required by Oracle APEX", readme)
        self.assertIn("Never require Python", skill)
        self.assertIn("Python is not a minimum capability", generic)
        self.assertNotIn("Run Python commands", generic)
        self.assertIn("Python is not a prerequisite", agent_native)

    def test_optional_oracle_apex_echarts_integration_preserves_core_contract(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        reference = (SKILL / "references" / "oracle-apex-echarts.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        contract = "\n".join((skill, reference, readme))

        self.assertIn("$oracle-apex-echarts", contract)
        self.assertIn("releases/tag/v1.0.1", contract)
        self.assertIn("PK_APEX_ECHARTS.FUNC_CHART_INLINE", reference)
        self.assertIn("PK_APEX_ECHARTS.FUNC_CHART_AJAX", reference)
        self.assertIn("RUNTIME_ONLY", reference)
        self.assertIn("textual or tabular fallback", reference)
        self.assertIn("fully usable without ECharts", " ".join(reference.split()))
        self.assertIn("Never copy an ECharts bundle", skill)
        self.assertEqual(list(SKILL.rglob("echarts-*.min.js")), [])

    def test_release_metadata_matches_current_skill_version(self) -> None:
        kit_source = (SCRIPTS / "_kit.py").read_text(encoding="utf-8")
        version_match = re.search(r'^SKILL_VERSION = "([^"]+)"$', kit_source, re.MULTILINE)
        self.assertIsNotNone(version_match)
        version = version_match.group(1)
        artifact = f"build-apex-brand-reports-{version}.zip"

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        codex_adapter = (ROOT / "adapters" / "codex" / "README.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        validation = (ROOT / "tests" / "VALIDATION.md").read_text(encoding="utf-8")
        release_workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

        self.assertIn(artifact, readme)
        self.assertIn(artifact, codex_adapter)
        self.assertIn(f"## [{version}]", changelog)
        self.assertIn(f"# Validation evidence for v{version}", validation)
        self.assertIn('VERSION="${GITHUB_REF_NAME#v}"', release_workflow)
        self.assertIn('test "${VERSION}" = "${SKILL_VERSION}"', release_workflow)

    def test_packaging_is_deterministic_and_installable(self) -> None:
        self.assertEqual((ROOT / "requirements.txt").read_bytes(), (SKILL / "requirements.txt").read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.zip"
            second = Path(tmp) / "second.zip"
            run_script("package_skill.py", "--output", first)
            run_script("package_skill.py", "--output", second)
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(), hashlib.sha256(second.read_bytes()).digest())
            with zipfile.ZipFile(first) as archive:
                names = set(archive.namelist())
                self.assertIn("build-apex-brand-reports/SKILL.md", names)
                self.assertIn("build-apex-brand-reports/requirements.txt", names)
                self.assertIn("build-apex-brand-reports/assets/schemas/report-profile.schema.json", names)


class SchemaAndThemeTests(unittest.TestCase):
    def test_valid_theme(self) -> None:
        run_script("validate_theme.py", EXAMPLE / "brand-profile.json")

    def test_invalid_theme_contrast(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profile = json.loads((EXAMPLE / "brand-profile.json").read_text(encoding="utf-8"))
            profile["colors"]["semantic"]["text"] = "#FFFFFF"
            path = Path(tmp) / "invalid.json"
            path.write_text(json.dumps(profile), encoding="utf-8")
            result = run_script("validate_theme.py", path, expected=1)
            self.assertIn("Contrast", result.stderr)

    def test_invalid_focus_contrast(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profile = json.loads((EXAMPLE / "brand-profile.json").read_text(encoding="utf-8"))
            profile["colors"]["screen"]["focus"] = "#E8F0F7"
            path = Path(tmp) / "invalid-focus.json"
            path.write_text(json.dumps(profile), encoding="utf-8")
            result = run_script("validate_theme.py", path, expected=1)
            self.assertIn("Contrast focus/surface", result.stderr)

    def test_all_schemas_are_valid_json(self) -> None:
        for path in sorted((ROOT / "schemas").glob("*.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")


class ScaffoldTests(unittest.TestCase):
    def test_primary_runtime_contract_is_native_dynamic_content(self) -> None:
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        apex_reference = (SKILL / "references" / "oracle-apex.md").read_text(encoding="utf-8")
        blueprint = (SKILL / "assets" / "apex-modal-blueprint" / "page-designer.md.tpl").read_text(encoding="utf-8")
        engine_body = (SKILL / "assets" / "runtime" / "plsql" / "report_engine.pkb.tpl").read_text(encoding="utf-8")
        contract = "\n".join((skill_text, apex_reference, blueprint)).lower()

        self.assertIn("dynamic content", contract)
        self.assertIn("return existing_package.func_report_html", contract)
        self.assertIn("external frontend server", contract)
        self.assertIn("proprietary plug-in", contract)
        self.assertIn('<div class="abrk__document">', engine_body)
        self.assertNotIn("abrk__print-shell", engine_body)
        self.assertNotIn("<iframe", engine_body.lower())
        self.assertNotIn("http://", engine_body.lower())
        self.assertNotIn("https://", engine_body.lower())

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            result = run_script("scaffold_project.py", "--target", target, "--config", config, "--platform", "apex", "--dry-run")
            self.assertIn("DRY-RUN", result.stdout)
            self.assertFalse(target.exists())

    def test_initial_create_manifest_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config, "--installed-at", "2026-07-22T12:00:00Z")
            run_script("validate_scaffold.py", target)
            manifest = json.loads((target / ".apex-brand-report-kit" / "installation-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["runtime_version"], "0.1.1")
            self.assertEqual(manifest["skill_version"], "0.1.2")
            self.assertEqual(manifest["theme"], {"id": "acme-harbor", "version": "1.0.0"})
            self.assertEqual(len(manifest["managed_files"]["engine"]), 4)
            self.assertEqual(len(manifest["managed_files"]["theme"]), 4)
            self.assertEqual(len(manifest["project_files"]), 3)

    def test_required_values_and_schema_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config_path = copy_config_fixture(fixture)
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            del config["packages"]["owner"]
            config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
            result = run_script("scaffold_project.py", "--target", Path(tmp) / "consumer", "--config", config_path, expected=1)
            self.assertIn("Schema validation failed", result.stderr)

    def test_existing_file_protection_and_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            collision = target / "db" / "report-kit" / "pk_abrk_engine.pks"
            collision.parent.mkdir(parents=True)
            collision.write_text("user content", encoding="utf-8")
            result = run_script("scaffold_project.py", "--target", target, "--config", config, expected=1)
            self.assertIn("Files already exist", result.stderr)
            run_script("scaffold_project.py", "--target", target, "--config", config, "--force", "--installed-at", "2026-07-22T12:00:00Z")
            self.assertIn("create or replace package PK_ABRK_ENGINE", collision.read_text(encoding="utf-8"))

    def test_second_initial_create_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config)
            result = run_script("scaffold_project.py", "--target", target, "--config", config, expected=1)
            self.assertIn("use --update", result.stderr)

    def test_update_preserves_theme_and_business_and_detects_engine_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config, "--installed-at", "2026-07-22T12:00:00Z")
            theme = target / "web" / "report-kit" / "report-theme.css"
            business = target / "docs" / "report-kit" / "report-function-example.sql"
            theme.write_text(theme.read_text(encoding="utf-8") + "\n/* consumer theme change */\n", encoding="utf-8")
            business.write_text(business.read_text(encoding="utf-8") + "\n-- consumer business change\n", encoding="utf-8")
            run_script("scaffold_project.py", "--target", target, "--config", config, "--update")
            self.assertIn("consumer theme change", theme.read_text(encoding="utf-8"))
            self.assertIn("consumer business change", business.read_text(encoding="utf-8"))
            engine = target / "web" / "report-kit" / "report-kit.js"
            engine.write_text(engine.read_text(encoding="utf-8") + "\n/* local engine change */\n", encoding="utf-8")
            result = run_script("scaffold_project.py", "--target", target, "--config", config, "--update", expected=1)
            self.assertIn("Engine conflicts detected", result.stderr)
            run_script("scaffold_project.py", "--target", target, "--config", config, "--update", "--force")
            self.assertNotIn("local engine change", engine.read_text(encoding="utf-8"))
            self.assertIn("consumer theme change", theme.read_text(encoding="utf-8"))
            self.assertIn("consumer business change", business.read_text(encoding="utf-8"))

    def test_no_unresolved_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config)
            run_script("validate_scaffold.py", target)

    def test_validation_is_scoped_to_manifest_declared_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config)
            legacy = target / "legacy" / "unrelated-template.sql"
            legacy.parent.mkdir(parents=True)
            legacy.write_text(
                "select '{{LEGITIMATE_LEGACY_PLACEHOLDER}}' from dual;\n" +
                "password = \"" + "legacy-value-not-owned-by-this-kit" + "\"\n",
                encoding="utf-8",
            )
            run_script("validate_scaffold.py", target)

    def test_config_fields_and_brand_tokens_are_operational(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config)
            engine = (target / "db" / "report-kit" / "pk_abrk_engine.pkb").read_text(encoding="utf-8")
            theme = (target / "db" / "report-kit" / "pk_acme_theme.pkb").read_text(encoding="utf-8")
            export_doc = (target / "docs" / "report-kit" / "server-side-export.md").read_text(encoding="utf-8")
            for marker in (
                'data-header-size="', 'data-toolbar-position="', 'data-density="',
                'data-economy-print="', 'data-repeat-table-header="', 'data-abrk-action="xlsx"',
                'print-color-adjust:exact', 'l_has_actions boolean',
            ):
                self.assertIn(marker, engine)
            self.assertIn("linear-gradient(135deg,#123C69,#1D5B91)", theme)
            self.assertIn("--abrk-focus:#326FD1", theme)
            self.assertIn("--abrk-card-radius:16px", theme)
            self.assertIn("--abrk-soft:#F5F8FB", theme)
            self.assertIn("ABRK_EXPORT_XLSX", export_doc)
            self.assertNotIn("NOT_CONFIGURED", export_doc)

    def test_pt_br_runtime_and_project_examples_are_localized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config_path = copy_config_fixture(fixture)
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            config["locale"] = {"language": "pt-BR", "timezone": "America/Fortaleza"}
            config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config_path)
            engine_spec = (target / "db" / "report-kit" / "pk_abrk_engine.pks").read_text(encoding="utf-8")
            engine_body = (target / "db" / "report-kit" / "pk_abrk_engine.pkb").read_text(encoding="utf-8")
            report_example = (target / "docs" / "report-kit" / "report-function-example.sql").read_text(encoding="utf-8")
            blueprint = (target / "docs" / "report-kit" / "apex-modal-page-900.md").read_text(encoding="utf-8")
            self.assertIn("c_runtime_version constant varchar2(20) := '0.1.1'", engine_spec)
            self.assertIn("Ações do relatório", engine_body)
            self.assertIn("Salvar em PDF", engine_body)
            self.assertIn("Emitido em", engine_body)
            self.assertIn("DD/MM/YYYY HH24:MI TZH:TZM", engine_body)
            self.assertIn('lang="pt-BR"', engine_body)
            self.assertIn("Relatório indisponível", engine_body)
            self.assertIn("Título do relatório", report_example)
            self.assertIn("relatorio.pdf", report_example)
            self.assertIn("If, and only if, the confirmed function is argument-free", blueprint)

    def test_english_runtime_remains_the_default_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config)
            engine = (target / "db" / "report-kit" / "pk_abrk_engine.pkb").read_text(encoding="utf-8")
            self.assertIn("Report actions", engine)
            self.assertIn("Save as PDF", engine)
            self.assertIn("Generated at", engine)
            self.assertIn('lang="en-US"', engine)

    def test_disabled_exports_emit_no_invalid_process_block_or_empty_toolbar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config_path = copy_config_fixture(fixture)
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            config["features"] = {name: False for name in ("fullscreen", "print", "pdf", "xlsx", "csv")}
            config["packages"]["export_process"] = None
            config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
            target = Path(tmp) / "consumer"
            run_script("scaffold_project.py", "--target", target, "--config", config_path)
            engine = (target / "db" / "report-kit" / "pk_abrk_engine.pkb").read_text(encoding="utf-8")
            export_doc = (target / "docs" / "report-kit" / "server-side-export.md").read_text(encoding="utf-8")
            self.assertIn("l_toolbar <> 'custom' and not l_has_actions", engine)
            self.assertIn("false or false or false or false or false", engine)
            self.assertIn("No export page process is required", export_doc)
            self.assertNotIn("begin\n    DISABLED", export_doc)

    def test_css_token_injection_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "fixture"
            fixture.mkdir()
            config = copy_config_fixture(fixture)
            profile_path = fixture / "brand-profile.json"
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            profile["components"]["cards"]["tokens"]["radius"] = "1px;}</style><script>alert(1)</script>"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            result = run_script("scaffold_project.py", "--target", Path(tmp) / "consumer", "--config", config, expected=1)
            self.assertIn("Unsafe CSS token value", result.stderr)


class SecurityTests(unittest.TestCase):
    def test_repository_sensitive_scan(self) -> None:
        run_script("validate_sensitive_data.py", ROOT)

    def test_detects_secret_assignment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.txt"
            path.write_text("api_" + "key = \"this-value-must-not-ship\"", encoding="utf-8")
            result = run_script("validate_sensitive_data.py", path, expected=1)
            self.assertIn("secret assignment", result.stderr)


class ArtifactTests(unittest.TestCase):
    def test_pdfs_and_all_rendered_pages_exist(self) -> None:
        pdfinfo = shutil.which("pdfinfo")
        self.assertIsNotNone(pdfinfo, "pdfinfo is required for PDF validation")
        output = EXAMPLE / "output"
        for stem in ("acme-harbor-portrait", "acme-harbor-landscape", "acme-harbor-long-table"):
            pdf = output / f"{stem}.pdf"
            self.assertTrue(pdf.is_file(), pdf)
            info = subprocess.run([pdfinfo, str(pdf)], text=True, capture_output=True, check=True).stdout
            pages = int(next(line.split(":", 1)[1] for line in info.splitlines() if line.startswith("Pages:")).strip())
            rendered = sorted((output / "rendered").glob(f"{stem}-*.png"))
            self.assertEqual(len(rendered), pages)
            self.assertGreater(pdf.stat().st_size, 10_000)
            pdftotext = shutil.which("pdftotext")
            if pdftotext:
                extracted = subprocess.run([pdftotext, str(pdf), "-"], text=True, capture_output=True, check=True).stdout
                self.assertNotIn("Page 0", extracted)

    def test_xlsx_openxml_types_and_safe_text(self) -> None:
        path = EXAMPLE / "output" / "acme-harbor-operations.xlsx"
        self.assertTrue(path.is_file())
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            self.assertIn("xl/workbook.xml", names)
            self.assertIn("xl/worksheets/sheet1.xml", names)
            workbook = archive.read("xl/workbook.xml").decode("utf-8")
            sheet = archive.read("xl/worksheets/sheet1.xml").decode("utf-8")
            strings = "".join(
                archive.read(name).decode("utf-8")
                for name in names
                if name in {"xl/sharedStrings.xml", "xl/worksheets/sheet1.xml"}
            )
            self.assertIn("Operations", workbook)
            self.assertIn("Atenção", strings)
            self.assertIn("=2+3", strings)
            table_xml = "".join(
                archive.read(name).decode("utf-8") for name in names if name.startswith("xl/tables/")
            )
            self.assertIn("autoFilter", table_xml)
            self.assertIn('r="A7"', sheet)
            self.assertIn('t="n"', sheet)
            self.assertNotIn("<f>", sheet)
            self.assertGreater(path.stat().st_size, 5_000)


if __name__ == "__main__":
    unittest.main()
