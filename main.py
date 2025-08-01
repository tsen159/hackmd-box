import requests
import os
import wcwidth

hackmd_api_key = os.environ["HACKMD_API_KEY"]
github_token = os.environ["GH_TOKEN"]
gist_id = os.environ["GIST_ID"]
gist_url = f"https://api.github.com/gists/{gist_id}"
NUM_NOTES = 6
MODE = "lastchangeAt"  # changed to "createdAt" to sort by creation date
MAX_WIDTH = 48


def truncate_string(s, max_width=MAX_WIDTH):
    """Truncate a string to a maximum length, considering the width of characters."""
    if wcwidth.wcswidth(s) <= max_width:
        return s
    truncated = s[: max_width - 3] + "..."
    return truncated


def get_hackmd_notes():
    if not hackmd_api_key:
        raise ValueError("HACKMD_API_KEY is not set in the environment variables.")
    headers = {"Authorization": f"Bearer {hackmd_api_key}"}
    response = requests.get(url="https://api.hackmd.io/v1/notes", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")

    notes = response.json()
    notes = sorted(notes, key=lambda note: note.get(MODE, 0), reverse=True)
    data = [
        (note["title"], note["publishLink"]) for note in notes if note["publishedAt"]
    ]

    return data[:NUM_NOTES]  # Limit to the last NUM_NOTES notes


def update_gists(content):
    gist_contest = "\n".join([truncate_string(item[0]) for item in content])
    md_contest = "\n\n".join([f"[{item[0]}]({item[1]})" for item in content])
    data = {
        "description": "My Latest Notes on HackMD ✏️",
        "files": {
            "hackmd_box": {"content": gist_contest},
            "hackmd_box.md": {"content": md_contest},
        },
    }
    req = requests.patch(
        url=gist_url,
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/json",
        },
        json=data,
    )


if __name__ == "__main__":
    content = get_hackmd_notes()
    update_gists(content)
