# Source graph Git environment

`ops/git.ts::git` inspects committed local source using Git under scoped Deno `--allow-run=git`
permissions. Inherited loader variables (`LD_LIBRARY_PATH`, `LD_PRELOAD`, `DYLD_LIBRARY_PATH`,
`DYLD_INSERT_LIBRARIES`) make that scoped spawn fail before Git runs. The Git helper therefore
clears its child environment and sets `GIT_OPTIONAL_LOCKS=0`, retaining `--no-optional-locks` for
administrative reads. This does not grant unrestricted subprocess or environment permissions.

Git executable lookup uses the caller's PATH before constructing its cleared child environment. The
child does not inherit HOME, XDG paths, global Git config selectors or credentials. Local repository
and system Git config still apply; repository ownership must be correct and cannot depend on an
inherited `safe.directory` workaround. Source selection comes from committed gitlinks and
`.gitmodules`, not user/global config or injected `GIT_DIR`/`GIT_WORK_TREE`.

Only calls opting into `Command.clearEnv` are isolated. The generic `run()` default still inherits
its environment, including intentional scientific library paths. The local snapshot Git helper and
its temporary Git fixture helpers use the same isolation and explicit `GIT_OPTIONAL_LOCKS=0`,
retaining their no-system/global-config settings. Publication's actual push/auth commands use that
generic path; this fix does not claim to sanitize every CLI or change authentication and does not
run Git over a network. The focused tests create temporary local Git metadata and read the actual
child environment. Their controlled loader-variable regression requires launching the Deno test with
those variables set; regular tests retain the same scoped `--allow-run=git` permission.
