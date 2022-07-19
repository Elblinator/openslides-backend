from openslides_backend.permissions.management_levels import OrganizationManagementLevel

from .base import BasePresenterTestCase


class TestExportMeeting(BasePresenterTestCase):
    def test_correct(self) -> None:
        self.set_models({"meeting/1": {"name": "test_foo"}})
        status_code, data = self.request("export_meeting", {"meeting_id": 1})
        self.assertEqual(status_code, 200)
        assert data["meeting"]["1"]["name"] == "test_foo"
        for collection in (
            "group",
            "personal_note",
            "tag",
            "agenda_item",
            "list_of_speakers",
            "speaker",
            "topic",
            "motion",
            "motion_submitter",
            "motion_comment",
            "motion_comment_section",
            "motion_category",
            "motion_block",
            "motion_change_recommendation",
            "motion_state",
            "motion_workflow",
            "motion_statute_paragraph",
            "poll",
            "option",
            "vote",
            "assignment",
            "assignment_candidate",
            "mediafile",
            "projector",
            "projection",
            "projector_message",
            "projector_countdown",
            "chat_group",
            "chat_message",
        ):
            assert data[collection] == {}

        assert data["_migration_index"]

    def test_no_permissions(self) -> None:
        self.set_models(
            {
                "meeting/1": {"name": "test_foo"},
                "user/1": {
                    "organization_management_level": OrganizationManagementLevel.CAN_MANAGE_ORGANIZATION
                },
            }
        )
        status_code, data = self.request("export_meeting", {"meeting_id": 1})
        assert status_code == 403

    def test_organization_tags_exclusion(self) -> None:
        self.set_models(
            {
                "meeting/1": {"name": "name_foo", "organization_tag_ids": [12]},
                "organization_tag/12": {
                    "name": "name_bar",
                    "tagged_ids": ["meeting/1"],
                },
            }
        )
        status_code, data = self.request("export_meeting", {"meeting_id": 1})
        assert status_code == 200
        assert "organization_tag" not in data
        assert data["meeting"]["1"].get("organization_tag_ids") is None

    def test_add_users(self) -> None:
        self.set_models(
            {
                "meeting/1": {
                    "name": "exported_meeting",
                    "user_ids": [1],
                    "group_ids": [11],
                    "present_user_ids": [1],
                },
                "user/1": {
                    "group_$_ids": ["1"],
                    "group_$1_ids": [11],
                    "comment_$": ["1"],
                    "comment_$1": "blablabla",
                    "number_$": ["1"],
                    "number_$1": "spamspamspam",
                    "is_present_in_meeting_ids": [1],
                },
                "group/11": {
                    "name": "group_in_meeting_1",
                    "meeting_id": 1,
                    "user_ids": [1],
                },
            }
        )
        status_code, data = self.request("export_meeting", {"meeting_id": 1})
        assert status_code == 200
        assert data["user"]["1"]["organization_management_level"] == "superadmin"
        assert data["user"]["1"]["username"] == "admin"
        assert data["user"]["1"]["is_active"] is True
        assert data["user"]["1"]["group_$_ids"] == ["1"]
        assert data["user"]["1"]["group_$1_ids"] == [11]
        assert data["user"]["1"]["meeting_ids"] == [1]
        assert data["user"]["1"]["is_present_in_meeting_ids"] == [1]
        assert data["user"]["1"]["comment_$"] == ["1"]
        assert data["user"]["1"]["comment_$1"] == "blablabla"
        assert data["user"]["1"]["number_$"] == ["1"]
        assert data["user"]["1"]["number_$1"] == "spamspamspam"

    def test_add_users_in_2_meetings(self) -> None:
        self.set_models(
            {
                "meeting/1": {
                    "name": "exported_meeting",
                    "user_ids": [1],
                    "group_ids": [11],
                    "present_user_ids": [1],
                },
                "meeting/2": {
                    "name": "not exported_meeting",
                    "user_ids": [1],
                    "group_ids": [12],
                    "present_user_ids": [1],
                },
                "user/1": {
                    "group_$_ids": ["1", "2"],
                    "group_$1_ids": [11],
                    "group_$2_ids": [12],
                    "comment_$": ["1", "2"],
                    "comment_$1": "blablabla",
                    "comment_$2": "blablabla2",
                    "is_present_in_meeting_ids": [1, 2],
                    "meeting_ids": [1, 2],
                },
                "group/11": {
                    "name": "group_in_meeting_1",
                    "meeting_id": 1,
                    "user_ids": [1],
                },
                "group/12": {
                    "name": "group_in_meeting_2",
                    "meeting_id": 2,
                    "user_ids": [1],
                },
            }
        )
        status_code, data = self.request("export_meeting", {"meeting_id": 1})
        assert status_code == 200
        assert data["user"]["1"]["organization_management_level"] == "superadmin"
        assert data["user"]["1"]["username"] == "admin"
        assert data["user"]["1"]["is_active"] is True
        assert data["user"]["1"]["group_$_ids"] == ["1"]
        assert data["user"]["1"]["group_$1_ids"] == [11]
        assert data["user"]["1"]["meeting_ids"] == [1]
        assert data["user"]["1"]["is_present_in_meeting_ids"] == [1]
        assert data["user"]["1"]["comment_$"] == ["1"]
        assert data["user"]["1"]["comment_$1"] == "blablabla"

    def test_export_meeting_with_ex_user(self) -> None:
        self.set_models(
            {
                "meeting/1": {
                    "name": "exported_meeting",
                    "motion_submitter_ids": [1],
                    "motion_ids": [1],
                    "list_of_speakers_ids": [1],
                    "personal_note_ids": [34],
                },
                "user/11": {
                    "username": "exuser11",
                    "submitted_motion_$_ids": ["1"],
                    "submitted_motion_$1_ids": [1],
                },
                "user/12": {
                    "username": "exuser12",
                    "personal_note_$_ids": ["1"],
                    "personal_note_$1_ids": [34],
                },
                "motion/1": {
                    "list_of_speakers_id": 1,
                    "meeting_id": 1,
                    "sequential_number": 1,
                    "state_id": 1,
                    "submitter_ids": [1],
                    "title": "dummy",
                },
                "motion_submitter/1": {
                    "user_id": 11,
                    "motion_id": 1,
                    "meeting_id": 1,
                },
                "list_of_speakers/1": {
                    "content_object_id": "motion/1",
                    "meeting_id": 1,
                    "sequential_number": 1,
                },
                "motion_state/1": {
                    "motion_ids": [1],
                },
                "personal_note/34": {
                    "user_id": 12,
                    "meeting_id": 1,
                    "note": "note_in_meeting1",
                },
            }
        )
        status_code, data = self.request("export_meeting", {"meeting_id": 1})
        assert status_code == 200
        assert data["meeting"]["1"].get("user_ids") is None
        user11 = data["user"]["11"]
        assert user11.get("username") == "exuser11"
        assert user11.get("submitted_motion_$_ids") == ["1"]
        assert user11.get("submitted_motion_$1_ids") == [1]
        user12 = data["user"]["12"]
        assert user12.get("username") == "exuser12"
        assert user12.get("personal_note_$_ids") == ["1"]
        assert user12.get("personal_note_$1_ids") == [34]