"""Unit tests for .qwenpaw-plugin/plugin.py.

The risk carried here is ``register()``'s payload guard: the host installs a
plugin with ``shutil.copytree``, which only follows the package's ``skills``
symlink when the checkout kept it a link, and the host reports a successful
install even when it lands zero skills. The guard makes that failure loud and
registers nothing.

The healthy case also asserts that no slash command is registered: the
host's own ``/<skill-name>`` dispatch only answers names no plugin has
claimed, so registering ``/sepia`` would shadow the injection that actually
builds an agent.

Standard library only, like the rest of the suite. The module is imported by
path and the host API is a recording stub, so ``agentscope`` never enters the
picture.  python3 -m unittest discover -s tests
"""
import importlib.util
import logging
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT / ".qwenpaw-plugin" / "plugin.py"


def load_plugin():
    """Import the plugin entry file without QwenPaw present."""
    spec = importlib.util.spec_from_file_location("sepia_plugin", PLUGIN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


plugin = load_plugin()


class RecordingApi:
    """Stand-in for PluginApi, recording what the plugin registers."""

    def __init__(self):
        self.providers = []
        self.commands = []

    def register_skill_provider(self, skills_dir=None, **kwargs):
        self.providers.append((Path(skills_dir), kwargs))

    def register_slash_command(self, name=None, **kwargs):
        self.commands.append((name, kwargs))


def build_package(root, skills, follow_symlink=True):
    """Lay out a clone-shaped package whose skills entry points at skills/."""
    canonical = root / "skills"
    for name in skills:
        skill_dir = canonical / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
    package = root / ".qwenpaw-plugin"
    package.mkdir()
    link = package / "skills"
    if follow_symlink:
        link.symlink_to("../skills")
    else:
        # What git writes into a checkout without symlink support: a plain
        # file holding the link text, which the host then copies as-is.
        link.write_text("../skills", encoding="utf-8")
    return link


class RegisterCase(unittest.TestCase):
    """What the payload guard registers, healthy and broken."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def register_with(self, follow_symlink=True, skills=None):
        skills = skills or list(plugin.PACKAGED_SKILLS)
        skills_dir = build_package(self.root, skills, follow_symlink)
        api = RecordingApi()
        with mock.patch.object(plugin, "SKILLS_DIR", skills_dir):
            plugin.SepiaPlugin().register(api)
        return api

    def test_resolvable_package_registers_skills_and_no_command(self):
        api = self.register_with()
        self.assertEqual(len(api.providers), 1)
        enabled = api.providers[0][1]
        self.assertTrue(enabled["enabled_by_default"])
        self.assertEqual(enabled["channels"], ["all"])
        # The host's own /<skill-name> dispatch serves /sepia and the five
        # operation entries, but only while no plugin claims the name.
        self.assertEqual(api.commands, [])

    def test_flattened_symlink_registers_nothing(self):
        # Silent zero-skill installs are the failure being guarded: the host
        # would log a warning and report success.
        with self.assertLogs(plugin.logger, level=logging.ERROR) as logs:
            api = self.register_with(follow_symlink=False)
        self.assertEqual(api.providers, [])
        self.assertEqual(api.commands, [])
        self.assertIn("git clone", "\n".join(logs.output))

    def test_partial_package_names_the_missing_skills(self):
        skills = [n for n in plugin.PACKAGED_SKILLS if n != "sepia-hemingway"]
        with self.assertLogs(plugin.logger, level=logging.ERROR) as logs:
            api = self.register_with(skills=skills)
        self.assertEqual(api.providers, [])
        # The skill name has to be identified on its own: the path in the same
        # message contains "sepia" for every skill, so a looser assertion would
        # pass even when the list came out empty or wrong.
        self.assertIn("(missing: sepia-hemingway)", "\n".join(logs.output))

    @unittest.skipUnless(
        hasattr(os, "geteuid") and os.geteuid() != 0,
        "chmod 000 does not stop root from reading the file",
    )
    def test_unreadable_skill_registers_nothing(self):
        # The guard opens the files rather than stat'ing them: a SKILL.md that
        # exists but cannot be read would otherwise land a provider whose skill
        # fails only when the host gets around to reading it.
        skills_dir = build_package(self.root, list(plugin.PACKAGED_SKILLS))
        victim = skills_dir / "sepia-review" / "SKILL.md"
        victim.chmod(0o000)
        self.addCleanup(victim.chmod, 0o644)
        api = RecordingApi()
        with self.assertLogs(plugin.logger, level=logging.ERROR) as logs:
            with mock.patch.object(plugin, "SKILLS_DIR", skills_dir):
                plugin.SepiaPlugin().register(api)
        self.assertEqual(api.providers, [])
        self.assertEqual(api.commands, [])
        self.assertIn("(missing: sepia-review)", "\n".join(logs.output))


class RepositoryPackageCase(unittest.TestCase):
    """The package in this checkout is the one users install."""

    @unittest.skipUnless(
        (ROOT / ".qwenpaw-plugin" / "skills" / "sepia" / "SKILL.md").is_file(),
        "this checkout has no symlink support, so the package cannot resolve",
    )
    def test_every_advertised_skill_ships(self):
        self.assertEqual(plugin._missing_packaged_skills(), [])


if __name__ == "__main__":
    unittest.main()
