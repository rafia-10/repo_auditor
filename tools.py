import os, re, io, zipfile, requests
from pathlib import Path
from langchain_core.tools import tool
from dotenv import load_dotenv

@tool("download_repo")
def download_repo_tool(repo_url: str, ref: str = "main") -> dict:
    """
    Download a GitHub repository as a zipball and extract it.
    Args:
        repo_url: full GitHub repo URL (e.g., https://github.com/user/repo)
        ref: branch, tag, or commit (default "main")
    Returns:
        dict with path to extracted repo
    """
    owner_repo = "/".join(repo_url.rstrip("/").split("/")[-2:])
    zip_url = f"https://api.github.com/repos/{owner_repo}/zipball/{ref}"

    headers = {}
    load_dotenv(dotenv_path="repo_auditor/.env")
    gh_token = os.getenv("GITHUB_TOKEN")
    if gh_token:
        headers["Authorization"] = f"token {gh_token}"

    r = requests.get(zip_url, headers=headers)
    r.raise_for_status()

    repo_dir = Path("/tmp") / f"{owner_repo.replace('/', '_')}_{ref}"
    repo_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(repo_dir)

    return {"path": str(repo_dir.resolve()), "repo": repo_url, "ref": ref}


@tool("scan_envs")
def scan_envs_tool(root_path: str) -> dict:
    """
    Scan a repo directory for .env files and detect sensitive entries.
    Returns: findings list with file, line, key, redacted value
    """
    findings = []
    env_files = list(Path(root_path).rglob(".env*"))
    suspicious_patterns = [
        r"API[_-]?KEY",
        r"SECRET",
        r"PASSWORD",
        r"TOKEN",
        r"ACCESS[_-]?KEY",
    ]

    for path in env_files:
        with open(path, "r", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                if "=" not in line:
                    continue
                key, val = line.strip().split("=", 1)
                for pat in suspicious_patterns:
                    if re.search(pat, key, re.IGNORECASE):
                        redacted = val[:4] + "****" if val else ""
                        findings.append(
                            {"file": str(path), "line": i, "key": key, "value": redacted}
                        )

    return {
        "root": root_path,
        "env_files_scanned": [str(p) for p in env_files],
        "findings": findings,
        "status": (
            "no_env_files" if not env_files else
            "no_secrets" if not findings else
            "secrets_found"
        )
    }



def get_all_tools():
    return [download_repo_tool, scan_envs_tool]