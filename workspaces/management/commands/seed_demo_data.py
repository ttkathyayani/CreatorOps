from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workspaces.models import Workspace, Membership
from clients.models import Client
from campaigns.models import Campaign
from content.models import ContentItem, ContentVersion
from approvals.models import Approval
from analytics.models import CampaignMetric


class Command(BaseCommand):
    help = "Seeds initial demo data for CreatorOps SaaS evaluation"

    def handle(self, *args, **options):
        self.stdout.write("Seeding CreatorOps demo data...")

        # 1. Create Demo Users
        users_data = [
            ("admin", "admin@creatorops.io", "admin123", Membership.Role.ADMIN, "Alex", "Admin"),
            ("manager", "manager@creatorops.io", "admin123", Membership.Role.MANAGER, "Marcus", "Manager"),
            ("creator", "creator@creatorops.io", "admin123", Membership.Role.CREATOR, "Chloe", "Creator"),
            ("client", "client@auraskincare.com", "admin123", Membership.Role.CLIENT_REVIEWER, "Elena", "Reviewer"),
        ]

        users = {}
        for username, email, password, role, first, last in users_data:
            user, created = User.objects.get_or_create(username=username, defaults={"email": email, "first_name": first, "last_name": last})
            user.set_password(password)
            user.save()
            users[username] = (user, role)
            self.stdout.write(f"User: {username} (password: {password})")

        # 2. Create Workspace
        workspace, _ = Workspace.objects.get_or_create(
            name="Apex Media Agency",
            defaults={"description": "Full-service digital content & influencer marketing studio."}
        )

        # Assign Memberships
        for username, (user, role) in users.items():
            Membership.objects.update_or_create(
                user=user,
                workspace=workspace,
                defaults={"role": role}
            )

        # 3. Create Clients
        c1, _ = Client.objects.update_or_create(
            workspace=workspace,
            name="Aura Skincare",
            defaults={
                "contact_email": "marketing@auraskincare.com",
                "industry": "Clean Beauty & Wellness",
                "company_notes": "Premium organic skincare brand launching clinical brightening serum.",
                "brand_guidelines": (
                    "Tone: Empowering, clean, scientific yet accessible.\n"
                    "Mandatory Tag: #AuraGlow, #CleanSkincareRoutine\n"
                    "Forbidden: Never make miraculous anti-aging cure claims. Avoid aggressive sales tactics."
                )
            }
        )

        c2, _ = Client.objects.update_or_create(
            workspace=workspace,
            name="Nova Cloud Solutions",
            defaults={
                "contact_email": "growth@novacloud.io",
                "industry": "B2B SaaS / DevOps",
                "company_notes": "Cloud infrastructure optimization platform for high-scale Kubernetes clusters.",
                "brand_guidelines": (
                    "Tone: Technical, authoritative, data-driven, concise.\n"
                    "Mandatory Tag: #CloudOps, #DevOpsEfficiency\n"
                    "Key Message: 40% AWS cloud spend reduction without latency tradeoffs."
                )
            }
        )

        c3, _ = Client.objects.update_or_create(
            workspace=workspace,
            name="Urban Fit Co.",
            defaults={
                "contact_email": "collabs@urbanfit.co",
                "industry": "Athleisure & Fitness",
                "company_notes": "High-performance training gear engineered for hybrid athletes.",
                "brand_guidelines": (
                    "Tone: Energetic, bold, inspiring, raw athletic discipline.\n"
                    "Mandatory Tag: #BuiltForMovement, #UrbanFit\n"
                    "Visuals: Fast-paced cuts, high-contrast urban lighting."
                )
            }
        )

        # 4. Create Campaigns
        today = date.today()
        camp1, _ = Campaign.objects.update_or_create(
            client=c1,
            title="Summer Glow 2026 Product Launch",
            defaults={
                "objective": "Launch the Brightening Vitamin C Dew Serum across TikTok and Instagram Reels.",
                "target_audience": "Skincare enthusiasts 20-35 looking for clean dermatological glow.",
                "status": Campaign.Status.ACTIVE,
                "start_date": today - timedelta(days=14),
                "end_date": today + timedelta(days=45),
                "budget": 12500.00
            }
        )

        camp2, _ = Campaign.objects.update_or_create(
            client=c2,
            title="Q4 Cloud Cost Optimization Drive",
            defaults={
                "objective": "Target CTOs and DevOps leads with LinkedIn thought leadership & video case studies.",
                "target_audience": "DevOps Engineers, VP of Engineering, Cloud Architects.",
                "status": Campaign.Status.ACTIVE,
                "start_date": today - timedelta(days=7),
                "end_date": today + timedelta(days=60),
                "budget": 20000.00
            }
        )

        camp3, _ = Campaign.objects.update_or_create(
            client=c3,
            title="High-Intensity Athleisure Drop",
            defaults={
                "objective": "Launch seamless compression training line with high-energy creator workout reels.",
                "target_audience": "Fitness creators, CrossFitters, hybrid runners 22-38.",
                "status": Campaign.Status.PLANNING,
                "start_date": today,
                "end_date": today + timedelta(days=30),
                "budget": 8500.00
            }
        )

        # 5. Create Content Items in various stages of the workflow
        creator_user = users["creator"][0]
        manager_user = users["manager"][0]
        client_user = users["client"][0]

        # Item 1: Pending Client Approval
        item1, _ = ContentItem.objects.update_or_create(
            campaign=camp1,
            title="Morning Dew Routine: 3 Easy Steps to Glass Skin",
            defaults={
                "creator": creator_user,
                "platform": ContentItem.Platform.INSTAGRAM,
                "script_body": (
                    "[00:00 - 00:03] Hook: Stop using 10 different products every morning.\n"
                    "[00:03 - 00:15] Showcase Aura Brightening Dew serum texture on natural morning skin.\n"
                    "[00:15 - 00:30] Breakdown the active niacinamide and cold-pressed citrus actives.\n"
                    "[00:30 - 00:45] Final glow check in daylight with clear CTA: Link in bio for 20% off launch code #AuraGlow."
                ),
                "caption": (
                    "Minimal steps. Maximum hydration. ✨ Start your morning with the all-new Aura Glow Dew Serum. "
                    "Clean, dermatologically tested, and vegan. #AuraGlow #CleanSkincareRoutine #GlassSkin"
                ),
                "due_date": today + timedelta(days=3),
                "status": ContentItem.Status.PENDING_CLIENT
            }
        )
        item1.create_version(user=creator_user)

        # Add Manager Approval record for item1
        Approval.objects.get_or_create(
            content_item=item1,
            reviewer=manager_user,
            decision=Approval.Decision.MANAGER_APPROVED,
            defaults={"comment": "Hook is strong and pacing matches Instagram Reels trends. Approved to send to Elena for client signoff."}
        )

        # Item 2: Pending Manager Review
        item2, _ = ContentItem.objects.update_or_create(
            campaign=camp1,
            title="Dermatologist vs Viral Trends: What Actually Works?",
            defaults={
                "creator": creator_user,
                "platform": ContentItem.Platform.TIKTOK,
                "script_body": (
                    "[00:00 - 00:04] Hook: I tested every viral skincare hack so you don't ruin your skin barrier.\n"
                    "[00:04 - 00:25] Reacting to lemon juice and harsh scrubs—why they do more harm than good.\n"
                    "[00:25 - 00:50] The science behind balanced barrier repair with Aura Skincare's gentle ceramide cream."
                ),
                "caption": "Your skin barrier will thank you later 🙌 Avoid the hype, choose the science. #AuraGlow #BarrierRepair #SkincareFacts",
                "due_date": today + timedelta(days=5),
                "status": ContentItem.Status.PENDING_MANAGER
            }
        )
        item2.create_version(user=creator_user)

        # Item 3: Changes Requested (Returned to Creator)
        item3, _ = ContentItem.objects.update_or_create(
            campaign=camp1,
            title="Before & After 14 Days Glow Challenge",
            defaults={
                "creator": creator_user,
                "platform": ContentItem.Platform.YOUTUBE,
                "script_body": (
                    "[00:00 - 00:10] Hook: We gave 5 people our new formula for two weeks.\n"
                    "[00:10 - 00:45] Daily diary snippets and unretouched skin close-ups.\n"
                    "[00:45 - 01:00] Results and participant reactions."
                ),
                "caption": "14 days of consistency. The results speak for themselves. Full video live! #AuraGlow",
                "due_date": today + timedelta(days=8),
                "status": ContentItem.Status.CHANGES_REQUESTED
            }
        )
        item3.create_version(user=creator_user)
        Approval.objects.get_or_create(
            content_item=item3,
            reviewer=client_user,
            decision=Approval.Decision.CLIENT_CHANGES_REQUESTED,
            defaults={"comment": "Please ensure lighting conditions in the Before and After comparisons are identical to maintain authentic credibility."}
        )

        # Item 4: Published!
        item4, _ = ContentItem.objects.update_or_create(
            campaign=camp2,
            title="Why 68% of Enterprise Kubernetes Clusters Overspend",
            defaults={
                "creator": creator_user,
                "platform": ContentItem.Platform.LINKEDIN,
                "script_body": (
                    "Cloud wastage is the silent budget killer in modern engineering teams.\n"
                    "Here are 3 ways Nova Cloud automatically reclaims underutilized node compute."
                ),
                "caption": "Efficiency isn't just about cutting costs—it's about maximizing engineering agility. Read the full case study: #CloudOps #DevOpsEfficiency",
                "due_date": today - timedelta(days=3),
                "status": ContentItem.Status.PUBLISHED
            }
        )
        item4.create_version(user=creator_user)
        Approval.objects.get_or_create(
            content_item=item4,
            reviewer=manager_user,
            decision=Approval.Decision.MANAGER_APPROVED,
            defaults={"comment": "Excellent technical accuracy. Ready to publish."}
        )

        # Item 5: Draft
        item5, _ = ContentItem.objects.update_or_create(
            campaign=camp3,
            title="Zero Distraction: The Apex Seamless Legging Launch",
            defaults={
                "creator": creator_user,
                "platform": ContentItem.Platform.INSTAGRAM,
                "script_body": "[00:00 - 00:05] Rapid urban running montage in downtown sunrise lighting. High tempo beat drop.",
                "caption": "Engineered for speed, durability, and comfort. Drop 01 live now. #BuiltForMovement #UrbanFit",
                "due_date": today + timedelta(days=12),
                "status": ContentItem.Status.DRAFT
            }
        )
        item5.create_version(user=creator_user)

        # 6. Add Campaign Telemetry Metrics
        CampaignMetric.objects.get_or_create(
            campaign=camp1,
            metric_name="Total Impressions",
            recorded_date=today - timedelta(days=2),
            defaults={"metric_value": 84200.00, "notes": "Instagram Reels viral pick up"}
        )
        CampaignMetric.objects.get_or_create(
            campaign=camp1,
            metric_name="Engagement Rate (%)",
            recorded_date=today - timedelta(days=2),
            defaults={"metric_value": 5.4, "notes": "Comments and shares exceeding benchmark"}
        )
        CampaignMetric.objects.get_or_create(
            campaign=camp2,
            metric_name="Qualified Leads",
            recorded_date=today - timedelta(days=1),
            defaults={"metric_value": 142.00, "notes": "B2B Whitepaper downloads from LinkedIn"}
        )
        CampaignMetric.objects.get_or_create(
            campaign=camp2,
            metric_name="Cost per Acquisition ($)",
            recorded_date=today - timedelta(days=1),
            defaults={"metric_value": 38.50, "notes": "Down 22% from baseline"}
        )

        self.stdout.write(self.style.SUCCESS("CreatorOps demo data successfully seeded!"))
