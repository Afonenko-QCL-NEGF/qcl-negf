# Ordinary offline documentation: Root/Nix owns immutable payload/assets closure.
# These Base-only guards validate layout before imports, not external admission.
get(ENV, "QCL_DOCS_PROFILE", "") in ("offline-v1", "pilot-v1") ||
    error("Operator recipe requires explicit offline-v1 or pilot-v1")

# Staging reads this versioned literal without executing Julia. Keep the exact LF
# bytes and final newline; this is generated index source, not a second chapter.
const QCL_DOCS_OPERATOR_INDEX = "# Документация оператора\n\n[Восстановление прерванного запуска](@ref operator-recovery)\n\n[Неизменяемый runtime захвата](capture-runtime-delivery.md)\n\n[Свидетельство сборки solver](solver-build-receipt.md)\n"

function _qcl_docs_path(name)
    value = get(ENV, name, "")
    isempty(value) && error("Missing required documentation path: " * name)
    startswith(value, "/") && isabspath(value) || error("Documentation path must be Linux absolute")
    (endswith(value, "/") || occursin("//", value) ||
     any(part -> part == "." || part == "..", split(value, '/'))) &&
        error("Documentation path has noncanonical components")
    value == normpath(value) || error("Documentation path must be normalized")
    cursor = value
    while true
        islink(cursor) && error("Documentation path has a symlink ancestor")
        parent = dirname(cursor)
        parent == cursor && break
        cursor = parent
    end
    return value
end
function _qcl_docs_directory(path)
    isdir(path) || error("Required documentation directory is missing")
    realpath(path) == path || error("Documentation directory is not canonical")
end
function _qcl_docs_contains(parent, child)
    a, b = splitpath(parent), splitpath(child)
    return length(b) >= length(a) && b[1:length(a)] == a
end
_qcl_docs_root = _qcl_docs_path("QCL_DOCS_ROOT")
_qcl_docs_attempt = _qcl_docs_path("QCL_DOCS_ATTEMPT")
_qcl_docs_source = _qcl_docs_path("QCL_DOCS_SOURCE")
_qcl_docs_build = _qcl_docs_path("QCL_DOCS_BUILD")
for path in (_qcl_docs_root, _qcl_docs_attempt, _qcl_docs_source, dirname(_qcl_docs_build))
    _qcl_docs_directory(path)
end
(_qcl_docs_contains(_qcl_docs_root, _qcl_docs_attempt) ||
 _qcl_docs_contains(_qcl_docs_attempt, _qcl_docs_root)) && error("ROOT and ATTEMPT overlap")
(_qcl_docs_contains(_qcl_docs_source, _qcl_docs_build) ||
 _qcl_docs_contains(_qcl_docs_build, _qcl_docs_source)) && error("SOURCE and BUILD overlap")
_qcl_docs_source == joinpath(_qcl_docs_attempt, "stage", "operator", "src") ||
    error("SOURCE does not match operator layout")
_qcl_docs_build == joinpath(_qcl_docs_attempt, "raw", "operator") ||
    error("BUILD does not match operator layout")
(ispath(_qcl_docs_build) || islink(_qcl_docs_build)) && error("BUILD already exists")
joinpath(realpath(dirname(_qcl_docs_build)), "operator") == _qcl_docs_build ||
    error("BUILD candidate is not canonical")
VERSION == v"1.13.0" || error("Documentation requires Julia 1.13.0")
_qcl_docs_project = joinpath(_qcl_docs_root, "julia", "Project.toml")
for name in ("Project.toml", "Manifest.toml")
    expected = joinpath(_qcl_docs_root, "julia", name)
    cursor = expected
    while true
        islink(cursor) && error("Documentation project has a symlink ancestor")
        parent = dirname(cursor)
        parent == cursor && break
        cursor = parent
    end
    isfile(expected) || error("Missing regular pilot project input")
    realpath(expected) == expected || error("Documentation project input is not canonical")
end
Base.active_project() == _qcl_docs_project || error("Wrong active pilot project")

using Documenter
makedocs(
    root = _qcl_docs_root,
    source = _qcl_docs_source,
    build = _qcl_docs_build,
    modules = Module[],
    remotes = nothing,
    sitename = "Документация оператора",
    format = Documenter.HTML(prettyurls = false, edit_link = nothing,
        disable_git = true, analytics = "", warn_outdated = false,
        prerender = false, mathengine = nothing,
        assets = ["assets/qcl-fixed-light.css"],
        repolink = "https://github.com/Afonenko-QCL-NEGF/qcl-negf"),
    pages = ["Home" => "index.md", "Recovery" => "recovery.md",
        "Capture runtime" => "capture-runtime-delivery.md",
        "Solver build receipt" => "solver-build-receipt.md"],
    pagesonly = false,
    doctest = false,
    linkcheck = false,
    checkdocs = :none,
    warnonly = false,
    draft = false,
)
