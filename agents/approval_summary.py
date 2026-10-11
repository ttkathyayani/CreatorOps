from .base import BaseAgent


class ApprovalSummaryAgent(BaseAgent):
    name = "Approval Summary Agent"
    description = "Consolidates manager and client review comments into an actionable, prioritized revision checklist."

    def run(self, data: dict) -> dict:
        approvals = data.get("approvals", [])
        content_title = data.get("content_title", "Content Item")

        if not approvals:
            return {
                "agent": self.name,
                "content_title": content_title,
                "status": "clean",
                "summary": "No feedback or change requests recorded yet.",
                "action_items": [],
                "unresolved_count": 0,
            }

        action_items = []
        positive_notes = []
        unresolved_count = 0

        for idx, app in enumerate(approvals, 1):
            comment = app.get("comment", "").strip()
            reviewer = app.get("reviewer", "Reviewer")
            decision = app.get("decision", "")

            if not comment:
                continue

            is_change_request = "CHANGES_REQUESTED" in decision or "rejected" in decision.lower()

            # Categorize keywords
            comment_lower = comment.lower()
            category = "General"
            if any(k in comment_lower for k in ["hook", "opening", "intro", "pacing", "seconds"]):
                category = "Hook & Pacing"
            elif any(k in comment_lower for k in ["cta", "call to action", "link", "bio"]):
                category = "Call to Action"
            elif any(k in comment_lower for k in ["audio", "music", "visual", "b-roll", "image", "asset"]):
                category = "Visuals & Assets"
            elif any(k in comment_lower for k in ["brand", "tone", "font", "color", "logo"]):
                category = "Branding"
            elif any(k in comment_lower for k in ["spelling", "grammar", "wording", "typo"]):
                category = "Copywriting"

            if is_change_request:
                unresolved_count += 1
                action_items.append({
                    "id": idx,
                    "reviewer": reviewer,
                    "category": category,
                    "task": comment,
                    "priority": "High" if "must" in comment_lower or "crucial" in comment_lower else "Medium",
                    "status": "Pending Revision",
                })
            else:
                positive_notes.append(f"{reviewer}: \"{comment}\"")

        summary_text = (
            f"Found {unresolved_count} unresolved revision requirement(s) from stakeholders."
            if unresolved_count > 0
            else "All feedback is constructive or approved. No critical blockers detected."
        )

        return {
            "agent": self.name,
            "content_title": content_title,
            "status": "action_required" if unresolved_count > 0 else "approved_ready",
            "summary": summary_text,
            "unresolved_count": unresolved_count,
            "action_items": action_items,
            "positive_feedback": positive_notes,
            "recommended_next_step": "Address high-priority items before re-submitting for manager review." if unresolved_count > 0 else "Proceed with asset export and scheduled publishing.",
        }
