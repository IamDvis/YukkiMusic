#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config

from ..logging import LOGGER

loop = asyncio.get_event_loop_policy().get_event_loop()


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return loop.run_until_complete(install_requirements())

def git():
    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = config.UPSTREAM_REPO

    try:
        repo = Repo()
        LOGGER(__name__).info("Git Client Found [VPS DEPLOYER]")
    except GitCommandError:
        LOGGER(__name__).info("Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("origin", UPSTREAM_REPO) if "origin" not in repo.remotes else repo.remote("origin")
        origin.fetch()
        repo.create_head(config.UPSTREAM_BRANCH, origin.refs[config.UPSTREAM_BRANCH])
        repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(origin.refs[config.UPSTREAM_BRANCH])
        repo.heads[config.UPSTREAM_BRANCH].checkout(True)

    try:
        repo.git.fetch()
        nrs = repo.remote("origin")
        nrs.pull(config.UPSTREAM_BRANCH)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
        LOGGER(__name__).info("Error during pull; reset to FETCH_HEAD")

    diff_index = repo.head.commit.diff("FETCH_HEAD")
    requirements_updated = any(
        diff.a_path == "requirements.txt" or diff.b_path == "requirements.txt"
        for diff in diff_index
    )

    if requirements_updated:
        install_req("pip3 install --no-cache-dir -r requirements.txt")

    LOGGER(__name__).info(f"Fetched Updates from: {REPO_LINK}")