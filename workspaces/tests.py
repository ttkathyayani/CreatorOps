from django.test import TestCase
from django.contrib.auth.models import User
from workspaces.models import Workspace, Membership
from clients.models import Client
from campaigns.models import Campaign
from content.models import ContentItem, ContentVersion
from agents import (
    ScriptReviewAgent,
    ContentIdeasAgent,
    ApprovalSummaryAgent,
    CampaignReportAgent,
)


class CreatorOpsCoreTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testcreator", password="password123")
        self.manager = User.objects.create_user(username="testmanager", password="password123")
        self.workspace = Workspace.objects.create(name="Apex Digital Agency", description="Test agency")
        
        self.membership_creator = Membership.objects.create(
            user=self.user, workspace=self.workspace, role=Membership.Role.CREATOR
        )
        self.membership_manager = Membership.objects.create(
            user=self.manager, workspace=self.workspace, role=Membership.Role.MANAGER
        )
        
        self.client = Client.objects.create(
            workspace=self.workspace,
            name="Neon Athletics",
            contact_email="marketing@neonathletics.com",
            brand_guidelines="Bold, energetic, high performance. No passive voice."
        )
        
        self.campaign = Campaign.objects.create(
            client=self.client,
            title="Q4 Sneaker Launch",
            objective="Drive conversions for runner shoe line",
            budget=25000.00
        )

    def test_workspace_slug_generation(self):
        """TC-01: Verify automatic unique slug generation on workspace save"""
        self.assertEqual(self.workspace.slug, "apex-digital-agency")

    def test_membership_roles(self):
        """TC-02: Verify multi-tenant role distinction between Creator and Manager"""
        self.assertEqual(self.membership_creator.role, Membership.Role.CREATOR)
        self.assertEqual(self.membership_manager.role, Membership.Role.MANAGER)

    def test_content_lifecycle_and_versioning(self):
        """TC-03: Verify ContentItem creation, status transitions, and version snapshot audit trail"""
        item = ContentItem.objects.create(
            campaign=self.campaign,
            creator=self.user,
            title="IG Reel 1: Run Past Limits",
            platform=ContentItem.Platform.INSTAGRAM,
            script_body="Stop wishing. Start sprinting. The Neon Runner X is here. Comment RUN below!",
            caption="#NeonAthletics #RunFast",
            status=ContentItem.Status.DRAFT
        )
        self.assertEqual(item.status, "draft")
        
        # Test automated version snapshot creation
        v1 = item.create_version(user=self.user)
        self.assertEqual(v1.revision_number, 1)
        self.assertIn("Stop wishing", v1.script_snapshot)
        
        # Update and create revision 2
        item.script_body = "Stop wishing. Start sprinting with 40% more rebound. Comment RUN below!"
        item.status = ContentItem.Status.PENDING_MANAGER
        item.save()
        v2 = item.create_version(user=self.user)
        self.assertEqual(v2.revision_number, 2)
        self.assertEqual(item.versions.count(), 2)

    def test_script_review_agent(self):
        """TC-04: Verify AI Script Review Agent NLP scoring and brand rule checks"""
        agent = ScriptReviewAgent()
        result = agent.run({
            "script": "Stop scrolling right now! Here is the greatest workout routine for daily runners looking to improve marathon endurance fast. Follow these three steps and comment RUN below to receive the free guide today!",
            "brand_rules": "Must be energetic. Avoid sluggish, lazy.",
            "platform": "Instagram"
        })
        self.assertIn("score", result)
        self.assertIn("word_count", result)
        self.assertGreaterEqual(result["score"], 80)
        self.assertTrue(result["passed"])

    def test_content_ideas_agent(self):
        """TC-05: Verify AI Content Ideas Agent concept and hook generation"""
        agent = ContentIdeasAgent()
        result = agent.run({
            "industry": "Fitness & Athletics",
            "audience": "Marathon runners",
            "goal": "Product Awareness",
            "platform": "Instagram"
        })
        self.assertIn("ideas", result)
        self.assertGreater(len(result["ideas"]), 0)

    def test_approval_summary_agent(self):
        """TC-06: Verify AI Approval Summary Agent comment clustering and action items"""
        agent = ApprovalSummaryAgent()
        comments = [
            {"author": "Manager Jane", "comment": "Audio is slightly quiet at 0:15.", "decision": "changes_requested"},
            {"author": "Client Reviewer", "comment": "Color grade looks great, but trim 3 seconds from the intro.", "decision": "changes_requested"}
        ]
        result = agent.run({"comments": comments})
        self.assertIn("summary", result)
        self.assertIn("action_items", result)
