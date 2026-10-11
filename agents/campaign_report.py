from .base import BaseAgent


class CampaignReportAgent(BaseAgent):
    name = "Campaign Report Agent"
    description = "Transforms campaign status, content delivery metrics, and performance analytics into an executive summary."

    def run(self, data: dict) -> dict:
        title = data.get("title", "Campaign")
        client_name = data.get("client_name", "Client")
        status = data.get("status", "Active")
        total_content = data.get("total_content", 0)
        published_content = data.get("published_content", 0)
        pending_content = data.get("pending_content", 0)
        metrics = data.get("metrics", [])
        budget = float(data.get("budget", 0.0))

        # Calculate metrics aggregates
        total_impressions = 0.0
        total_clicks = 0.0
        total_conversions = 0.0
        avg_engagement_rate = 0.0
        engagement_samples = 0

        for m in metrics:
            name = m.get("metric_name", "").lower()
            val = float(m.get("metric_value", 0))

            if "impression" in name or "views" in name or "reach" in name:
                total_impressions += val
            elif "click" in name:
                total_clicks += val
            elif "conversion" in name or "lead" in name or "sale" in name:
                total_conversions += val
            elif "engagement" in name:
                avg_engagement_rate += val
                engagement_samples += 1

        if engagement_samples > 0:
            avg_engagement_rate = round(avg_engagement_rate / engagement_samples, 2)
        elif total_impressions > 0 and total_clicks > 0:
            avg_engagement_rate = round((total_clicks / total_impressions) * 100, 2)

        completion_rate = round((published_content / total_content * 100), 1) if total_content > 0 else 0.0

        # Assess health
        health = "On Track"
        if pending_content > published_content and status == "ACTIVE":
            health = "Needs Review / Bottleneck"
        elif completion_rate >= 80:
            health = "Strong Performance"

        # Executive narrative
        narrative = (
            f"Campaign '{title}' for {client_name} is currently {status.upper()} with an overall status of '{health}'. "
            f"{published_content} of {total_content} scheduled content assets ({completion_rate}%) have been published. "
            f"Across recorded analytics, the campaign generated {int(total_impressions):,} impressions "
            f"and {int(total_clicks):,} clicks with an average engagement rate of {avg_engagement_rate}%."
        )

        insights = []
        if total_impressions > 10000 and avg_engagement_rate > 3.0:
            insights.append("High engagement resonance detected across audience segments.")
        if pending_content > 2:
            insights.append(f"{pending_content} pieces of content are waiting in manager/client review queues.")
        if budget > 0 and total_conversions > 0:
            cpa = round(budget / total_conversions, 2)
            insights.append(f"Estimated Cost Per Acquisition (CPA): ${cpa:,.2f}.")

        recommendations = [
            "Accelerate client sign-offs for pending content to maintain weekly publishing momentum.",
            "Double down on the top-performing platforms (Instagram / LinkedIn) with video adaptations.",
            "Repurpose high-performing scripts into multi-slide carousels and email summaries.",
        ]

        return {
            "agent": self.name,
            "campaign_title": title,
            "client_name": client_name,
            "overall_health": health,
            "completion_rate_pct": completion_rate,
            "kpis": {
                "total_impressions": int(total_impressions),
                "total_clicks": int(total_clicks),
                "total_conversions": int(total_conversions),
                "avg_engagement_rate_pct": avg_engagement_rate,
            },
            "executive_summary": narrative,
            "key_insights": insights,
            "strategic_recommendations": recommendations,
        }
