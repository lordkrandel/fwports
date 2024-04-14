# TODO

- Insert into the `ocli` tool, which can interact with Github through `gh`
    - Start from an initial PR number instead of a branch name
    - When a broken fw-port is found, it should add a \
      `@fw-port up to <previous_version_to_conflicted_branch>` \
      or `@fw-port ignore`
    - Prepare a better commit message with an indication of the forward port's initial PR number
- Have a function to push the fixed commit with the prepared message
