"""Sepia QwenPaw plugin: skill provider only.

Installs the packaged sepia skills (canonical router + five operation
shells, reached through the package's ``skills`` symlink to ``skills/``)
into every QwenPaw workspace.

No slash command is registered on purpose: the host's own ``/<skill-name>``
dispatch serves ``/sepia <text>`` and the five operation entries for any
installed skill, and it only answers a name no plugin has claimed — a
registered ``/sepia`` shadows that injection and its handler's reply ends
the turn without ever building an agent.
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger("qwenpaw.plugins.sepia")

PLUGIN_DIR = Path(__file__).resolve().parent

OPERATIONS = ("write", "review", "refactor", "recreate", "hemingway")

SKILLS_DIR = PLUGIN_DIR / "skills"

# The router plus the five operation shells: everything the package has to be
# able to read through its skills symlink.
PACKAGED_SKILLS = ("sepia",) + tuple(f"sepia-{op}" for op in OPERATIONS)


def _missing_packaged_skills() -> list[str]:
    """Names in PACKAGED_SKILLS whose ``SKILL.md`` cannot be read.

    Opened rather than stat'ed: the host reads these files after installing
    them, and a path that exists but cannot be opened would otherwise pass a
    ``is_file()`` check and land a provider whose skills fail further down.
    """
    missing = []
    for name in PACKAGED_SKILLS:
        try:
            with open(SKILLS_DIR / name / "SKILL.md", "rb"):
                pass
        except OSError:
            # FileNotFoundError (absent, or the flattened link that left the
            # tree unresolvable), NotADirectoryError, IsADirectoryError and
            # PermissionError all mean the same thing for this guard.
            missing.append(name)
    return missing


class SepiaPlugin:
    """Installs the packaged sepia skills into every QwenPaw workspace."""

    def register(self, api) -> None:
        missing = _missing_packaged_skills()
        if missing:
            # The host installs by shutil.copytree, which only follows the
            # skills symlink when the checkout kept it a link. A zip or a
            # symlink-stripped checkout would install zero skills and still
            # report success, so nothing is registered here: the "/<skill>"
            # dispatch the host provides natively keeps the names it has.
            logger.error(
                "✗ sepia: packaged skills cannot be read under %s (missing: "
                "%s). Check their permissions; a zip install or a checkout "
                "without symlink support also lands here, and that one needs a "
                "git clone instead.",
                SKILLS_DIR,
                ", ".join(missing),
            )
            return
        api.register_skill_provider(
            skills_dir=SKILLS_DIR,
            enabled_by_default=True,
            channels=["all"],
        )
        logger.info("✓ sepia skills registered from %s", SKILLS_DIR)


plugin = SepiaPlugin()
