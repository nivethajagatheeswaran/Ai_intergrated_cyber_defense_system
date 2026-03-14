def analyze(results):
    auto_actions = []
    human_review = []

    for r in results:
        if r["action"] == "auto_quarantine":
            auto_actions.append(r)
        elif r["action"] == "human_in_loop":
            human_review.append(r)

    return {
        "auto_quarantine": auto_actions,
        "human_review_required": human_review,
        "summary": {
            "total_modules": len(results),
            "critical_threats": len(auto_actions),
            "needs_human_decision": len(human_review)
        }
    }