from .base import BaseAgent


class ContentIdeasAgent(BaseAgent):
    name = "Content Ideas Agent"
    description = "Generates high-engagement content concepts, formats, and hooks tailored to audience, industry, and platform."

    def run(self, data: dict) -> dict:
        industry = (data.get("industry") or "General").strip()
        audience = (data.get("audience") or "Target Customers").strip()
        goal = (data.get("goal") or "Brand Awareness").strip()
        platform = (data.get("platform") or "Instagram").strip()

        ideas = []

        # Platform-tailored frameworks
        if platform in ["Instagram", "TikTok"]:
            ideas.extend([
                {
                    "title": f"The 3 Biggest Mistakes {audience} Make in {industry}",
                    "format": "Short-Form Video / Reel (30-45s)",
                    "hook": f"Stop doing this if you want better results in {industry}...",
                    "angle": "Contrarian breakdown + fast-paced tactical fix.",
                    "call_to_action": "Save this reel and comment 'GUIDE' for the checklist.",
                },
                {
                    "title": f"Day in the Life / Behind-the-Scenes: {goal}",
                    "format": "Carousel / Story Series (7 slides)",
                    "hook": "Here is what nobody tells you about our process...",
                    "angle": "Authenticity, transparent workflow, relatable story.",
                    "call_to_action": "Share this with a teammate who needs to see this.",
                },
                {
                    "title": f"Before vs After: Achieving {goal}",
                    "format": "Split Screen Transformation Reel",
                    "hook": "90 days ago we started here... look at what happened.",
                    "angle": "Visual proof and quick milestone breakdown.",
                    "call_to_action": "Follow for weekly tips and case studies.",
                },
            ])
        elif platform == "YouTube":
            ideas.extend([
                {
                    "title": f"The Ultimate {industry} Playbook for {audience} (Full Masterclass)",
                    "format": "Long-Form Video (12-15 min)",
                    "hook": f"If I had to start over in {industry} today, here is the exact 4-step framework I'd follow.",
                    "angle": "Comprehensive step-by-step tutorial with screen recordings and real data.",
                    "call_to_action": "Download the free template linked in the description.",
                },
                {
                    "title": f"Why Most {industry} Strategies Fail (And What Works Instead)",
                    "format": "Deep Dive / Video Essay (8-10 min)",
                    "hook": "Everyone is teaching the old way. Here is why modern algorithms changed everything.",
                    "angle": "Data-backed industry analysis and future trend breakdown.",
                    "call_to_action": "Subscribe and hit the bell for our deep-dive series.",
                },
            ])
        elif platform == "LinkedIn":
            ideas.extend([
                {
                    "title": f"How We Scaled Our {goal} Strategy for {industry} Leaders",
                    "format": "Text Post + Infographic Slide",
                    "hook": f"Most {audience} focus on vanity metrics. Here is the framework that drove 3.4x ROI.",
                    "angle": "Executive thought leadership, metrics, and actionable lessons.",
                    "call_to_action": "What is your biggest bottleneck this quarter? Drop your thoughts below.",
                },
                {
                    "title": f"5 Lessons Learned After Running 50+ {industry} Campaigns",
                    "format": "Curated Carousel / Document (PDF)",
                    "hook": "Experience is expensive. Save yourself 6 months of trial and error with these 5 rules.",
                    "angle": "B2B frameworks, operational clarity, and playbook sharing.",
                    "call_to_action": "Repost this if your network would benefit.",
                },
            ])
        else:  # Twitter/X or default
            ideas.extend([
                {
                    "title": f"The Zero-to-One Guide for {audience} in {industry}",
                    "format": "Visual Thread (8-10 tweets)",
                    "hook": f"Here is how high-growth teams achieve {goal} without burning out their budget. A thread 🧵👇",
                    "angle": "Bite-sized tactical insights with concise charts.",
                    "call_to_action": "Retweet the first post if you found this valuable.",
                },
                {
                    "title": f"Unpopular Opinion in {industry}",
                    "format": "High-Impact Single Post + Discussion",
                    "hook": f"Unpopular opinion: {goal} is not about luck, it's about structured iteration.",
                    "angle": "Thought-provoking thesis supported by direct observations.",
                    "call_to_action": "Do you agree or disagree? Let's discuss in the replies.",
                },
            ])

        return {
            "agent": self.name,
            "status": "success",
            "parameters": {
                "industry": industry,
                "audience": audience,
                "goal": goal,
                "platform": platform,
            },
            "suggested_ideas_count": len(ideas),
            "ideas": ideas,
            "key_recommendation": f"Focus on high-retention hooks and deliver a tangible takeaway aligned with '{goal}'.",
        }
