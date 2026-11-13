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


    def test_student_doctype_has_scoped_management_permissions(self):
        meta = frappe.get_meta("Student")
        permissions = {row.role: row for row in meta.permissions}
        self.assertTrue(permissions["Education Executive Manager"].read)
        self.assertTrue(permissions["Education Executive Manager"].write)
        self.assertTrue(permissions["Education Executive Manager"].create)
        self.assertTrue(permissions["Education Executive Manager"].delete)
        self.assertTrue(permissions["Education Learner Manager"].read)
        self.assertTrue(permissions["Education Learner Manager"].write)
        self.assertTrue(permissions["Education Learner Manager"].create)
        self.assertFalse(permissions["Education Learner Manager"].delete)
        self.assertTrue(permissions["Education Training Manager"].read)
        self.assertFalse(permissions["Education Training Manager"].write)
        self.assertTrue(permissions["Education Faculty Manager"].read)
        self.assertFalse(permissions["Education Faculty Manager"].write)

    def test_applicant_doctype_is_managed_by_learners_and_executive(self):
        meta = frappe.get_meta("Student Applicant")
        permissions = {row.role: row for row in meta.permissions}
        self.assertTrue(permissions["Education Executive Manager"].read)
        self.assertTrue(permissions["Education Executive Manager"].write)
        self.assertTrue(permissions["Education Executive Manager"].delete)
        self.assertTrue(permissions["Education Learner Manager"].read)
        self.assertTrue(permissions["Education Learner Manager"].write)
        self.assertTrue(permissions["Education Learner Manager"].create)
        self.assertFalse(permissions["Education Learner Manager"].delete)
