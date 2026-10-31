import sys

from graph import build_graph


def main():
    topic = " ".join(sys.argv[1:]) or "The state of AI agents in enterprise software"
    app = build_graph()

    initial = {
        "topic": topic,
        "research": "",
        "draft": "",
        "critique": None,
        "revisions": 0,
        "log": [],
    }

    final = dict(initial)
    print(f"\nTopic: {topic}\n")

    for update in app.stream(initial, stream_mode="updates"):
        for node, delta in update.items():
            for line in delta.get("log", []):
                print(f"  -> {line}")
            final.update({k: v for k, v in delta.items() if k != "log"})

    critique = final["critique"]
    print(f"\nFinal score: {critique.score}/10 after {final['revisions']} revision(s)\n")
    print(final["draft"])

    with open("output.md", "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{final['draft']}\n\n---\n## Research notes\n\n{final['research']}\n")
    print("\nSaved to output.md")


if __name__ == "__main__":
    main()