from frappe.tests.utils import FrappeTestCase

from education.api.permissions import get_visible_workspaces


class TestEducationWorkspaces(FrappeTestCase):
    def test_executive_can_see_all_four_workspaces(self):
        result = get_visible_workspaces(["Education Executive Manager"])
        self.assertTrue(result["can_switch_workspace"])
        self.assertEqual(
            {item["key"] for item in result["workspaces"]},
            {"executive", "training", "learners", "faculty"},
        )

    def test_specialist_sees_only_own_workspace(self):
        cases = {
            "Education Training Manager": "training",
            "Education Learner Manager": "learners",
            "Education Faculty Manager": "faculty",
        }
        for role, expected_key in cases.items():
            with self.subTest(role=role):
                result = get_visible_workspaces([role])
                self.assertFalse(result["can_switch_workspace"])
                self.assertEqual(
                    [item["key"] for item in result["workspaces"]],
                    [expected_key],
                )

    def test_legacy_education_manager_is_not_executive(self):
        result = get_visible_workspaces(["Education Manager"])
        self.assertFalse(result["can_switch_workspace"])
        self.assertEqual(
            [item["key"] for item in result["workspaces"]],
            ["training"],
        )

    def test_unassigned_user_has_no_workspace(self):
        result = get_visible_workspaces(["Student"])
        self.assertEqual(result["workspaces"], [])
