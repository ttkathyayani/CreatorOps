from .base import BaseAgent


class ScriptReviewAgent(BaseAgent):
    name = "Script Review Agent"
    description = "Inspects creator scripts for pacing, hook strength, call-to-action presence, and brand rule compliance."

    def run(self, data: dict) -> dict:
        script = (data.get("script") or "").strip()
        brand_rules = (data.get("brand_rules") or "").strip()
        platform = (data.get("platform") or "Instagram").strip()

        findings = []
        suggestions = []
        score = 100

        if not script:
            return {
                "agent": self.name,
                "passed": False,
                "score": 0,
                "word_count": 0,
                "estimated_duration_sec": 0,
                "findings": ["Script is completely empty."],
                "suggestions": ["Please provide a script draft or talking points to review."],
            }

        words = script.split()
        word_count = len(words)
        script_lower = script.lower()

        # Estimated duration in seconds (average speaking rate ~ 130 words per minute)
        est_duration_sec = round((word_count / 130.0) * 60)

        # 1. Word count & pacing check
        if platform in ["Instagram", "TikTok", "Twitter/X"]:
            if word_count > 150:
                findings.append(f"Script exceeds 150 words for short-form video ({word_count} words, ~{est_duration_sec}s).")
                suggestions.append("Trim fluff and tighten dialogue to keep viewer attention within 60 seconds.")
                score -= 15
            elif word_count < 25:
                findings.append(f"Script is very brief ({word_count} words).")
                suggestions.append("Ensure you have articulated the key value proposition clearly.")
                score -= 10
        elif platform == "YouTube":
            if word_count < 200:
                findings.append(f"Script is relatively short for a YouTube video ({word_count} words, ~{est_duration_sec}s).")
                suggestions.append("Expand on examples and provide step-by-step breakdowns for retention.")
                score -= 10

        # 2. Call to Action (CTA) Check
        cta_keywords = [
            "follow", "subscribe", "comment", "share", "save",
            "link in bio", "click the link", "sign up", "visit", "check out"
        ]
        has_cta = any(kw in script_lower for kw in cta_keywords)
        if not has_cta:
            findings.append("Missing explicit Call-to-Action (CTA).")
            suggestions.append("Add a clear next step (e.g., 'Save this for later', 'Drop a comment', or 'Link in bio').")
            score -= 20

        # 3. Hook Check (first 20 words)
        first_segment = " ".join(words[:min(20, word_count)]).lower()
        hook_triggers = ["why", "how", "stop", "never", "secret", "mistake", "truth", "if you", "look at", "what"]
        has_hook = any(ht in first_segment for ht in hook_triggers) or "?" in first_segment or "!" in first_segment
        if not has_hook:
            findings.append("Opening hook could be more engaging.")
            suggestions.append("Start with a high-curiosity question, bold statement, or direct problem statement in the first 3 seconds.")
            score -= 15

        # 4. Brand Guidelines Compliance
        if brand_rules:
            # Check for forbidden keywords mentioned in brand rules (e.g., "no swear words", "avoid cheap")
            rules_lines = [r.strip() for r in brand_rules.split("\n") if r.strip()]
            for rule in rules_lines:
                rule_lower = rule.lower()
                if "avoid" in rule_lower or "no " in rule_lower or "don't" in rule_lower:
                    forbidden_terms = [t.strip().strip("'\"") for t in rule.replace("avoid", "").replace("no", "").replace("don't use", "").split(",") if t.strip()]
                    for term in forbidden_terms:
                        if term and term in script_lower:
                            findings.append(f"Script contains discouraged brand term: '{term}'.")
                            suggestions.append(f"Replace '{term}' according to brand guidelines: {rule}")
                            score -= 15

        score = max(0, min(100, score))
        passed = len(findings) == 0

        return {
            "agent": self.name,
            "passed": passed,
            "score": score,
            "word_count": word_count,
            "estimated_duration_sec": est_duration_sec,
            "findings": findings if findings else ["All script checks passed successfully!"],
            "suggestions": suggestions if suggestions else ["The script structure and pacing look optimal for production."],
        }
