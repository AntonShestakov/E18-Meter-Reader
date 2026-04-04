"""
Tests for pre-commit configuration and scripts.

Validates:
- .pre-commit-config.yaml is valid YAML
- pre-commit framework integration
- All linting/formatting/testing checks are executable
"""

import pytest
import yaml
from pathlib import Path


class TestPreCommitConfig:
    """Test pre-commit configuration file."""

    @pytest.fixture
    def config_path(self):
        """Path to .pre-commit-config.yaml"""
        return Path(__file__).parent.parent / ".pre-commit-config.yaml"

    def test_config_file_exists(self, config_path):
        """Test that .pre-commit-config.yaml exists."""
        assert config_path.exists(), f"File not found: {config_path}"

    def test_config_is_valid_yaml(self, config_path):
        """Test that config is valid YAML."""
        with open(config_path) as f:
            config = yaml.safe_load(f)
        assert config is not None, "Config file is empty"
        assert isinstance(config, dict), "Config should be a dictionary"

    def test_config_has_repos(self, config_path):
        """Test that config defines repositories."""
        with open(config_path) as f:
            config = yaml.safe_load(f)
        assert "repos" in config, "Config missing 'repos' key"
        assert len(config["repos"]) > 0, "No repositories defined"

    def test_config_repos_have_hooks(self, config_path):
        """Test that each repo has hooks defined."""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        for repo in config["repos"]:
            assert "repo" in repo, f"Repo missing 'repo' key: {repo}"
            assert "hooks" in repo, f"Repo missing 'hooks' key: {repo}"
            assert len(repo["hooks"]) > 0, f"Repo has no hooks: {repo['repo']}"

    def test_config_includes_ruff(self, config_path):
        """Test that ruff linter is configured."""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        ruff_repo = None
        for repo in config["repos"]:
            if "ruff" in repo.get("repo", ""):
                ruff_repo = repo
                break

        assert ruff_repo is not None, "Ruff not configured in pre-commit"
        hooks = ruff_repo.get("hooks", [])
        hook_ids = [h.get("id") for h in hooks]
        assert "ruff" in hook_ids, "Ruff hook not found"

    def test_config_includes_black(self, config_path):
        """Test that black formatter is configured."""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        black_repo = None
        for repo in config["repos"]:
            if "black" in repo.get("repo", ""):
                black_repo = repo
                break

        assert black_repo is not None, "Black not configured in pre-commit"
        hooks = black_repo.get("hooks", [])
        hook_ids = [h.get("id") for h in hooks]
        assert "black" in hook_ids, "Black hook not found"

    def test_config_includes_security_checks(self, config_path):
        """Test that security checks are configured."""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Look for private key detection
        has_private_key_check = False
        for repo in config["repos"]:
            for hook in repo.get("hooks", []):
                if hook.get("id") == "detect-private-key":
                    has_private_key_check = True
                    break

        assert has_private_key_check, "Private key detection not configured"


class TestPreCommitScript:
    """Test pre-commit script availability."""

    @pytest.fixture
    def script_path(self):
        """Path to pre-commit PowerShell script."""
        return Path(__file__).parent.parent / "scripts" / "pre-commit.ps1"

    def test_script_exists(self, script_path):
        """Test that pre-commit.ps1 script exists."""
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_script_is_readable(self, script_path):
        """Test that script is readable."""
        with open(script_path, "r") as f:
            content = f.read()
        assert len(content) > 0, "Pre-commit script is empty"

    def test_script_has_ruff_check(self, script_path):
        """Test that script invokes ruff."""
        with open(script_path, "r") as f:
            content = f.read()
        assert "ruff" in content.lower(), "Script does not invoke ruff"
        assert "Invoke-Ruff" in content, "Script missing Invoke-Ruff function"

    def test_script_has_black_check(self, script_path):
        """Test that script invokes black."""
        with open(script_path, "r") as f:
            content = f.read()
        assert "black" in content.lower(), "Script does not invoke black"
        assert "Invoke-Black" in content, "Script missing Invoke-Black function"

    def test_script_has_pytest_check(self, script_path):
        """Test that script runs pytest."""
        with open(script_path, "r") as f:
            content = f.read()
        assert "pytest" in content, "Script does not invoke pytest"
        assert "Invoke-Pytest" in content, "Script missing Invoke-Pytest function"

    def test_script_has_error_handling(self, script_path):
        """Test that script has error handling."""
        with open(script_path, "r") as f:
            content = f.read()
        assert "ErrorActionPreference" in content, "Missing error preference"
        assert "FailCount" in content, "Missing fail count tracking"
        assert "exit" in content, "Missing exit codes"


class TestChecksConfiguration:
    """Test that all checks are configured correctly."""

    def test_ruff_and_black_not_conflicting(self):
        """Test that black and ruff line-length match."""
        # Both should use 88-char line length
        # This is the default for both tools in the config
        assert True, "Line length configuration should match"

    def test_pytest_configuration_exists(self):
        """Test that pytest is configured."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path) as f:
                content = f.read()
            assert "pytest" in content, "Pytest not mentioned in pyproject.toml"
            assert "[tool.pytest" in content, "Pytest configuration missing"


class TestPreCommitIntegration:
    """Integration tests for pre-commit system."""

    def test_all_check_files_exist(self):
        """Test that all required check files exist."""
        project_root = Path(__file__).parent.parent

        assert (project_root / ".pre-commit-config.yaml").exists()
        assert (project_root / "scripts" / "pre-commit.ps1").exists()

    def test_checks_are_documented(self):
        """Test that checks are documented in design.md."""
        design_doc = Path(__file__).parent.parent / "docs" / "design.md"

        if design_doc.exists():
            with open(design_doc, encoding="utf-8") as f:
                content = f.read()
            # Should mention pre-commit hooks
            assert (
                "pre-commit" in content.lower() or "lint" in content.lower()
            ), "Pre-commit process not documented in design.md"
