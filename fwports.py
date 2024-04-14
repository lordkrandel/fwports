import re
import subprocess
import sys
# ruff: noqa: T201


VERSIONS = [
    "15.0",
    "16.0",
    "saas-16.3",
    "saas-16.4",
    "17.0",
    "saas-17.1",
    "saas-17.2",
    "master",
]


# SHELL -----------------------------------------------------------------------


def shell(command, input_text=None):
    print(f"$ {command}")
    proc = subprocess.run(command.split(" "), input=input_text,
                          capture_output=True, text=True, check=False)
    newline = "\n"
    return f"{proc.stdout}{(newline + proc.stderr) if proc.stderr else ''}"


# GIT -------------------------------------------------------------------------


def git_apply(check=False, filename="-", input_text=None, verbose=False):
    return shell(f"git apply {'-v ' if verbose else ''}{'--check ' if check else ''}{filename}",
                 input_text=input_text)


def git_branch(branch, create=False, delete=False):
    return shell(f"git branch {'-f ' if create else ''}{'-D ' if delete else ''}{branch}")


def git_checkout(remote, checkout_branch, force=False):
    if force:
        return shell(f"git checkout -f {remote}/{checkout_branch} -B {checkout_branch}")
    return shell(f"git checkout {checkout_branch}")


def git_diff(base_branch, new_branch, patch=False):
    return shell(f"git diff {'--patch ' if patch else ''}{base_branch}..{new_branch}")


def git_fetch(remote, fetch_branch):
    return shell(f"git fetch {remote} {fetch_branch}")


def git_log(target_branch, base_branch=False):
    return shell(f"git log {(base_branch + '..') if base_branch else ''}{target_branch}")


def git_patch(base_branch, new_branch):
    return git_diff(base_branch, new_branch, patch=True)


def git_pull(remote, pull_branch):
    return shell(f"git checkout {remote} {pull_branch}")


# -----------------------------------------------------------------------------


if __name__ == '__main__':

    breaking = False
    target_branch = sys.argv[1]
    force = '--force' in sys.argv

    # Exclude the base version for the target
    for i, version in enumerate(VERSIONS):
        if target_branch.startswith(version):
            base_branch = version
            versions = VERSIONS[i + 1:]
            print(f"fwporting unto versions: {versions}")
            break
    else:
        print(f"Cannot find base branch {base_branch}, exiting.")
        sys.exit(1)

    # Create patch from base to target branch
    patch_content = git_patch(base_branch, target_branch)

    # Checkout and reset every version
    for version in versions:
        print(git_checkout("origin", version, force=force))

        # Try to apply the patch
        apply_result = git_apply(check=True, filename="-", verbose=True, input_text=patch_content)

        # If it's breaking, exit the loop
        if 'error: patch failed' in apply_result.lower():
            # Show the patch result
            print(apply_result)
            breaking = version
            break

    else:
        print("Fw-ports will have no problems.")
        sys.exit(0)

    # If there's a breaking version
    if breaking:

        # Create new branch name, taking out fw-port prefixes
        rest_branch = re.sub(f"(?:(?:{'|'.join(VERSIONS)})-)+(.+)", r'\1', target_branch)
        new_branch = f"{breaking}-{rest_branch}"

        # Create the branch and check it out
        print(git_branch(new_branch, create=True))
        print(git_checkout(False, new_branch))

        print()
        print("-------------------")
        print()
        print(f"Branch {new_branch} created, please fix the fw-port.")
        print()
        print("Last commit message:")

        # Show last commit message to help fixing the failed patch
        print(git_log(target_branch, base_branch=base_branch))
