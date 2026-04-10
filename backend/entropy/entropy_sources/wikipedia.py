import requests
import hashlib

def get_wiki_entropy():
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "recentchanges",
        "rcprop": "timestamp|title",
        "rclimit": 1,
        "format": "json"
    }

    headers = {
        "User-Agent": "EntropyLane/1.0 (test@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)

        if response.status_code != 200:
            print("Status error:", response.status_code)
            return None

        data = response.json()

        if "query" not in data or "recentchanges" not in data["query"]:
            print("Unexpected format:", data)
            return None

        changes = data["query"]["recentchanges"]

        if not changes:
            return None

        change = changes[0]

        timestamp = change.get("timestamp", "")
        title = change.get("title", "")

        raw = timestamp + title

        return hashlib.sha256(raw.encode()).hexdigest()

    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    print(get_wiki_entropy())