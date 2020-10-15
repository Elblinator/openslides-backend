from tests.system.action.base import BaseActionTestCase


class AssignmentUpdateActionTest(BaseActionTestCase):
    def test_update_correct(self) -> None:
        self.create_model("meeting/110", {"name": "name_sdurqw12"})
        self.create_model(
            "assignment/111", {"title": "title_srtgb123", "meeting_id": 110}
        )
        response = self.client.post(
            "/",
            json=[
                {
                    "action": "assignment.update",
                    "data": [{"id": 111, "title": "title_Xcdfgee"}],
                }
            ],
        )
        self.assert_status_code(response, 200)
        model = self.get_model("assignment/111")
        assert model.get("title") == "title_Xcdfgee"

    def test_update_correct_full_fields(self) -> None:
        self.create_model("meeting/110", {"name": "name_sdurqw12"})
        self.create_model(
            "assignment/111", {"title": "title_srtgb123", "meeting_id": 110}
        )
        response = self.client.post(
            "/",
            json=[
                {
                    "action": "assignment.update",
                    "data": [
                        {
                            "id": 111,
                            "title": "title_Xcdfgee",
                            "description": "text_test1",
                            "open_posts": 12,
                            "phase": 1,
                            "default_poll_description": "text_test2",
                            "number_poll_candidates": True,
                        }
                    ],
                }
            ],
        )
        self.assert_status_code(response, 200)
        model = self.get_model("assignment/111")
        assert model.get("title") == "title_Xcdfgee"
        assert model.get("description") == "text_test1"
        assert model.get("open_posts") == 12
        assert model.get("phase") == 1
        assert model.get("default_poll_description") == "text_test2"
        assert model.get("number_poll_candidates") is True

    def test_update_wrong_id(self) -> None:
        self.create_model("assignment/111", {"title": "title_srtgb123"})
        response = self.client.post(
            "/",
            json=[
                {
                    "action": "assignment.update",
                    "data": [{"id": 112, "title": "title_Xcdfgee"}],
                }
            ],
        )
        self.assert_status_code(response, 400)
        model = self.get_model("assignment/111")
        assert model.get("title") == "title_srtgb123"