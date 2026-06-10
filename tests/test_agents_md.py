"""
Tests for AGENTS.md structure and content.

AGENTS.md is a documentation file that cloud agents rely on to discover
how to work with this repository. These tests ensure the document contains
all required sections and accurately describes the current state of the
repository so that automated agents receive correct guidance.
"""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_MD_PATH = os.path.join(REPO_ROOT, "AGENTS.md")


def _read_agents_md():
    with open(AGENTS_MD_PATH, encoding="utf-8") as fh:
        return fh.read()


class TestAgentsMdExists(unittest.TestCase):
    """Basic file existence and readability checks."""

    def test_file_exists(self):
        self.assertTrue(
            os.path.isfile(AGENTS_MD_PATH),
            "AGENTS.md must exist at the repository root",
        )

    def test_file_is_not_empty(self):
        content = _read_agents_md()
        self.assertGreater(len(content.strip()), 0, "AGENTS.md must not be empty")

    def test_file_ends_with_newline(self):
        """Standard Unix convention: text files end with a trailing newline."""
        content = _read_agents_md()
        self.assertTrue(
            content.endswith("\n"),
            "AGENTS.md should end with a trailing newline",
        )


class TestAgentsMdHeadings(unittest.TestCase):
    """Verify all required Markdown headings are present."""

    def setUp(self):
        self.content = _read_agents_md()

    def _assert_heading(self, heading):
        self.assertIn(
            heading,
            self.content,
            f"Required heading '{heading}' not found in AGENTS.md",
        )

    def test_h1_title(self):
        self._assert_heading("# AGENTS.md")

    def test_h2_project_status(self):
        self._assert_heading("## Project status")

    def test_h2_cursor_cloud_instructions(self):
        self._assert_heading("## Cursor Cloud specific instructions")

    def test_h3_services(self):
        self._assert_heading("### Services")

    def test_h3_dependency_installation(self):
        self._assert_heading("### Dependency installation")

    def test_h3_lint_test_run(self):
        self._assert_heading("### Lint / test / run")

    def test_h3_vm_tooling(self):
        self._assert_heading("### VM tooling (pre-installed)")

    def test_h3_gotchas(self):
        self._assert_heading("### Gotchas")

    def test_no_empty_headings(self):
        """Every heading line must have non-whitespace text after the hashes."""
        for lineno, line in enumerate(self.content.splitlines(), start=1):
            if re.match(r"^#{1,6}\s*$", line):
                self.fail(
                    f"Empty heading found on line {lineno}: {line!r}"
                )


class TestAgentsMdProjectStatus(unittest.TestCase):
    """Validate the Project status section content."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_mentions_project_name(self):
        self.assertIn(
            "micro-skansen",
            self.content,
            "AGENTS.md must reference the project name 'micro-skansen'",
        )

    def test_describes_stub_status(self):
        self.assertIn(
            "stub repository",
            self.content,
            "Project status section must describe the repo as a stub repository",
        )

    def test_mentions_readme_as_only_file(self):
        self.assertIn(
            "README.md",
            self.content,
            "Project status must mention README.md as the only current file",
        )

    def test_no_application_source_code_claim(self):
        """The document must state there is no application source code yet."""
        self.assertIn(
            "no application source code",
            self.content,
            "Project status must state there is no application source code",
        )


class TestAgentsMdServicesTable(unittest.TestCase):
    """Validate the Services table structure and rows."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_table_header_service_column(self):
        self.assertIn("| Service |", self.content)

    def test_table_header_required_column(self):
        self.assertIn("| Required? |", self.content)

    def test_table_header_notes_column(self):
        self.assertIn("| Notes |", self.content)

    def test_table_separator_row(self):
        """The GFM table must have a separator row with dashes."""
        self.assertIn("|---------|", self.content)

    def test_table_row_application_server(self):
        self.assertIn("Application server", self.content)

    def test_table_row_database_cache(self):
        self.assertIn("Database / cache", self.content)

    def test_table_row_docker_compose(self):
        self.assertIn("Docker Compose", self.content)

    def test_all_service_rows_marked_na(self):
        """All three service rows should currently be marked N/A."""
        na_count = len(re.findall(r"\|\s*N/A\s*\|", self.content))
        self.assertGreaterEqual(
            na_count,
            3,
            "Each of the three service rows must contain a 'N/A' cell",
        )


class TestAgentsMdVmTooling(unittest.TestCase):
    """Validate the VM tooling section lists all required runtimes."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_nodejs_listed(self):
        self.assertIn("Node.js", self.content)

    def test_nvm_mentioned(self):
        self.assertIn("nvm", self.content)

    def test_python_listed(self):
        self.assertIn("Python 3.12", self.content)

    def test_go_listed(self):
        self.assertIn("Go 1.22", self.content)

    def test_rust_listed(self):
        self.assertIn("Rust", self.content)

    def test_node_npm_pnpm_yarn_mentioned(self):
        for tool in ("npm", "pnpm", "yarn"):
            with self.subTest(tool=tool):
                self.assertIn(tool, self.content)

    def test_python_pip_mentioned(self):
        self.assertIn("pip", self.content)

    def test_go_cargo_rustc_mentioned(self):
        for tool in ("cargo", "rustc"):
            with self.subTest(tool=tool):
                self.assertIn(tool, self.content)

    def test_version_verification_commands_present(self):
        """The section must document how to verify each runtime version."""
        expected_commands = (
            "node -v",
            "python3 --version",
            "go version",
            "rustc --version",
        )
        for cmd in expected_commands:
            with self.subTest(command=cmd):
                self.assertIn(
                    cmd,
                    self.content,
                    f"Version verification command '{cmd}' not found",
                )


class TestAgentsMdGotchas(unittest.TestCase):
    """Validate the Gotchas section lists all known caveats."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_no_monorepo_assumption_warning(self):
        self.assertIn(
            "monorepo",
            self.content,
            "Gotchas must warn agents not to assume a monorepo setup",
        )

    def test_no_docker_assumption_warning(self):
        self.assertIn(
            "Docker",
            self.content,
            "Gotchas must warn agents not to assume a Docker setup",
        )

    def test_main_branch_only_noted(self):
        self.assertIn(
            "main",
            self.content,
            "Gotchas must note that only the main branch exists",
        )

    def test_future_agents_rediscovery_note(self):
        self.assertIn(
            "Future agents",
            self.content,
            "Gotchas must instruct future agents to re-run environment discovery",
        )

    def test_gotchas_is_bulleted_list(self):
        """Each gotcha item should use a Markdown list marker (- or *)."""
        lines = self.content.splitlines()
        in_gotchas = False
        gotcha_bullets = []
        for line in lines:
            if line.strip() == "### Gotchas":
                in_gotchas = True
                continue
            if in_gotchas:
                if line.startswith("#"):
                    break
                if re.match(r"^\s*[-*]\s+", line):
                    gotcha_bullets.append(line)
        self.assertGreaterEqual(
            len(gotcha_bullets),
            1,
            "The Gotchas section must contain at least one bullet-list item",
        )


class TestAgentsMdDependencyInstallation(unittest.TestCase):
    """Validate the Dependency installation section."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_no_dependencies_stated(self):
        self.assertIn(
            "no project dependencies",
            self.content,
            "Dependency installation section must state there are no dependencies",
        )

    def test_example_install_commands_present(self):
        """The section should give example commands for when code lands."""
        for cmd in ("pnpm install", "pip install", "uv sync"):
            with self.subTest(command=cmd):
                self.assertIn(
                    cmd,
                    self.content,
                    f"Example install command '{cmd}' should be mentioned",
                )


class TestAgentsMdLintTestRun(unittest.TestCase):
    """Validate the Lint / test / run section."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_no_commands_defined_yet(self):
        self.assertIn(
            "No lint, test, or dev-server commands are defined yet",
            self.content,
        )

    def test_references_future_config_files(self):
        """Section should point agents to where commands will appear later."""
        for filename in ("package.json", "Makefile", "CONTRIBUTING.md"):
            with self.subTest(filename=filename):
                self.assertIn(
                    filename,
                    self.content,
                    f"Lint/test/run section should reference '{filename}'",
                )


class TestAgentsMdBoundaryAndRegression(unittest.TestCase):
    """Boundary and regression tests to strengthen confidence."""

    def setUp(self):
        self.content = _read_agents_md()

    def test_minimum_line_count(self):
        """The document should have at least 40 lines of meaningful content."""
        lines = [l for l in self.content.splitlines() if l.strip()]
        self.assertGreaterEqual(
            len(lines),
            10,
            "AGENTS.md appears truncated; expected at least 10 non-empty lines",
        )

    def test_no_placeholder_todo_text(self):
        """The document must not contain unresolved placeholder markers."""
        forbidden = ("TODO", "FIXME", "PLACEHOLDER", "XXX")
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(
                    marker,
                    self.content,
                    f"AGENTS.md should not contain unresolved marker '{marker}'",
                )

    def test_uses_markdown_bold_for_emphasis(self):
        """Key terms should be bolded using ** syntax."""
        self.assertRegex(
            self.content,
            r"\*\*.+?\*\*",
            "AGENTS.md should use **bold** Markdown for emphasis",
        )

    def test_no_windows_line_endings(self):
        """File must use Unix line endings only."""
        self.assertNotIn(
            "\r\n",
            self.content,
            "AGENTS.md must not contain Windows-style CRLF line endings",
        )

    def test_headings_use_atx_style(self):
        """All headings must use ATX style (leading #), not setext style (=== / ---)."""
        lines = self.content.splitlines()
        for i, line in enumerate(lines[1:], start=2):  # setext affects prior line
            self.assertNotRegex(
                line,
                r"^[=]{3,}\s*$",
                f"Setext H1 marker found on line {i}; use ATX style instead",
            )
            self.assertNotRegex(
                line,
                r"^[-]{3,}\s*$",
                f"Setext H2 marker found on line {i}; use ATX style instead",
            )

    def test_inline_code_used_for_commands(self):
        """Commands and filenames should be wrapped in backtick code spans."""
        # At minimum the document should use backticks somewhere
        self.assertIn(
            "`",
            self.content,
            "AGENTS.md should use inline code (backticks) for commands and filenames",
        )

    def test_section_order_matches_spec(self):
        """Sections must appear in the documented order."""
        expected_order = [
            "## Project status",
            "## Cursor Cloud specific instructions",
            "### Services",
            "### Dependency installation",
            "### Lint / test / run",
            "### VM tooling (pre-installed)",
            "### Gotchas",
        ]
        positions = []
        for heading in expected_order:
            pos = self.content.find(heading)
            self.assertNotEqual(
                pos,
                -1,
                f"Required section '{heading}' not found",
            )
            positions.append(pos)
        self.assertEqual(
            positions,
            sorted(positions),
            "Sections are not in the expected order",
        )


if __name__ == "__main__":
    unittest.main()
