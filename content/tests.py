from django.test import TestCase
from django.contrib.auth.models import User
from workspaces.models import Workspace
from clients.models import Client
from campaigns.models import Campaign
from content.models import ContentItem, SocialPublishLog
from content.publishing_service import SocialPublishingService


class SocialPublishingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testadmin", password="password123")
        self.workspace = Workspace.objects.create(name="Apex Agency", slug="apex-agency")
        self.client_brand = Client.objects.create(
            workspace=self.workspace,
            name="Quantum Athletics",
            contact_email="brand@quantum.com",
            brand_guidelines="Tone: High-energy athletic apparel. Prohibited: lazy, cheap.",
        )
        self.campaign = Campaign.objects.create(
            client=self.client_brand,
            title="Summer Launch 2026",
            objective="Brand Awareness",
            budget=15000.00,
        )
        self.item = ContentItem.objects.create(
            campaign=self.campaign,
            creator=self.user,
            title="Push Past The Limit - Seamless Shorts",
            platform=ContentItem.Platform.INSTAGRAM,
            script_body="Start strong: Stop settling for gear that rolls down. Introducing seamless support.",
            caption="Engineered for athletes who demand more. #QuantumAthletics #Fitness",
            status=ContentItem.Status.APPROVED,
        )

    def test_direct_publishing_meta_graph(self):
        result = SocialPublishingService.publish_content_item(
            self.item, user=self.user, target_platform="Instagram"
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["platform_name"], "Meta Graph API (Instagram)")
        self.assertTrue(result["post_id"].startswith("ig_"))
        self.assertIn("instagram.com/p/", result["post_url"])

        # Verify DB updates
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, ContentItem.Status.PUBLISHED)
        self.assertEqual(self.item.published_platform, "Meta Graph API (Instagram)")
        self.assertTrue(SocialPublishLog.objects.filter(content_item=self.item).exists())

    def test_direct_publishing_youtube(self):
        result = SocialPublishingService.publish_content_item(
            self.item, user=self.user, target_platform="YouTube"
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["platform_name"], "YouTube Data API v3")
        self.assertTrue(result["post_id"].startswith("yt_"))
        self.assertIn("youtube.com/shorts/", result["post_url"])

    def test_direct_publishing_tiktok(self):
        result = SocialPublishingService.publish_content_item(
            self.item, user=self.user, target_platform="TikTok"
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["platform_name"], "TikTok Content Posting API v2")
        self.assertTrue(result["post_id"].startswith("v_pub_file_"))
        self.assertIn("tiktok.com", result["post_url"])

    def test_connected_accounts_discovery(self):
        accounts = SocialPublishingService.get_connected_accounts(self.workspace)
        self.assertEqual(len(accounts), 3)
        platforms = [a["service_name"] for a in accounts]
        self.assertIn("Meta Graph API v19.0", platforms)
        self.assertIn("YouTube Data API v3", platforms)
        self.assertIn("TikTok Content Posting API v2", platforms)
