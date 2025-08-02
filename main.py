import requests
import os
import wcwidth
from typing import List, Tuple

hackmd_api_key = os.environ.get("HACKMD_API_KEY")
github_token = os.environ.get("GH_TOKEN")
gist_id = os.environ.get("GIST_ID")

gist_url = f"https://api.github.com/gists/{gist_id}"
NUM_NOTES = 6
MODE = "lastchangeAt"  # change to "createdAt" to sort by creation date
MAX_WIDTH = 48


def truncate_string(s, max_width=MAX_WIDTH):
    """
    Truncate a string to a maximum length, considering the width of characters.
    """
    if wcwidth.wcswidth(s) <= max_width:
        return s
    truncated = s[: max_width - 3] + "..."
    return truncated


def get_hackmd_notes(
    hackmd_api_key, num_notes=NUM_NOTES, sort_method=MODE
) -> List[Tuple[str, str]]:
    """
    Fetch the latest HackMD notes.
    Args:
        hackmd_api_key (str): The API key for HackMD.
        num_notes (int): The number of notes to retrieve.
        sort_method (str): The field to sort notes by, could be "lastchangeAt" or "createdAt".
    Returns:
        list: A list of tuples containing the title and publish link of each note.
    Raises:
        ValueError: If the API key is not set.
        SystemExit: If there is an HTTP error while fetching notes.
    """
    if not hackmd_api_key:
        raise ValueError("HACKMD_API_KEY is not set in the environment variables.")
    headers = {"Authorization": f"Bearer {hackmd_api_key}"}
    response = requests.get(url="https://api.hackmd.io/v1/notes", headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")

    notes = response.json()
    notes = sorted(notes, key=lambda note: note.get(sort_method, 0), reverse=True)
    data = [
        (note["title"], note["publishLink"]) for note in notes if note["publishedAt"]
    ]

    return data[:num_notes]  # limit to the last NUM_NOTES notes


def update_gists(content, gist_url=gist_url, github_token=github_token):
    """
    Update the GitHub Gist with the latest HackMD notes.
    Args:
        content (list): A list of tuples containing the title and publish link of each note.
        gist_url (str): The URL of the GitHub Gist to update.
        github_token (str): The GitHub token for authentication.
    Raises:
        SystemExit: If there is an HTTP error while updating the gist.
        ValueError: If the GitHub token or Gist ID is not set.
    """
    if not github_token:
        raise ValueError("GH_TOKEN is not set in the environment variables.")
    if not gist_url:
        raise ValueError("GIST_ID is not set in the environment variables.")

    gist_contest = "\n".join([truncate_string(item[0]) for item in content])
    md_contest = "\n\n".join([f"[{item[0]}]({item[1]})" for item in content])
    data = {
        "description": "My Latest HackMD Notes ✏️",
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

    try:
        req.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred while updating gist: {err}")


if __name__ == "__main__":
    content = get_hackmd_notes(hackmd_api_key)
    update_gists(content)
