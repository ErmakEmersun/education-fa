import frappe
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


    def test_course_faculty_enrollment_and_attendance_permissions_are_scoped(self):
        faculty = {row.role: row for row in frappe.get_meta("Faculty").permissions}
        self.assertTrue(faculty["Education Faculty Manager"].create)
        self.assertTrue(faculty["Education Faculty Manager"].write)
        self.assertFalse(faculty["Education Faculty Manager"].delete)
        self.assertTrue(faculty["Education Executive Manager"].delete)
        self.assertTrue(faculty["Education Training Manager"].read)
        self.assertFalse(faculty["Education Training Manager"].write)

        course = {row.role: row for row in frappe.get_meta("Course").permissions}
        self.assertTrue(course["Education Training Manager"].create)
        self.assertTrue(course["Education Training Manager"].write)
        self.assertTrue(course["Education Executive Manager"].delete)
        self.assertFalse(course["Education Faculty Manager"].write)

        enrollment = {
            row.role: row
            for row in frappe.get_meta("Course Enrollment").permissions
        }
        self.assertTrue(enrollment["Education Learner Manager"].create)
        self.assertTrue(enrollment["Education Learner Manager"].write)
        self.assertFalse(enrollment["Education Learner Manager"].submit)
        self.assertFalse(enrollment["Education Learner Manager"].delete)
        self.assertTrue(enrollment["Education Executive Manager"].submit)

        attendance = {
            row.role: row
            for row in frappe.get_meta("Student Attendance").permissions
        }
        self.assertTrue(attendance["Education Training Manager"].create)
        self.assertTrue(attendance["Education Training Manager"].write)
        self.assertTrue(attendance["Education Training Manager"].submit)
        self.assertFalse(attendance["Education Learner Manager"].write)
        self.assertTrue(attendance["Education Executive Manager"].delete)
