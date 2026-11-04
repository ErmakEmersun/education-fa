from frappe import _

from . import __version__ as app_version

app_name = "education"
app_title = "Education"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = "Education"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@frappe.io"
app_license = "GNU GPL V3"

required_apps = ["erpnext"]

add_to_apps_screen = [
	{
		"name": "education",
		"logo": "/assets/education/edu-logo.svg",
		"title": "Education",
		"route": "/app/education",
		"has_permission": "education.api.permissions.has_app_permission",
	}
]

# Includes in <head>
# ------------------
# Persian RTL styling is scoped to pages rendered with dir="rtl".
app_include_css = ["/assets/education/css/iran_rtl.css"]
app_include_js = ["education.bundle.js", "/assets/education/js/campus.js"]

# include js, css files in header of web template
# web_include_css = "/assets/education/css/education.css"
# web_include_js = "/assets/education/js/education.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "education/public/scss/website"

# website
update_website_context = []

website_generators = ["Student Admission", "Admission Register"]

website_route_rules = [
	{"from_route": "/admissions", "to_route": "Student Admission"},
	{"from_route": "/admission-registers", "to_route": "Admission Register"},
	{"from_route": "/student-portal/<path:app_path>", "to_route": "student-portal"},
]

treeviews = ["Assessment Group"]

calendars = [
	"Subject Schedule",
]

standard_portal_menu_items = [
	{
		"title": "Admission",
		"route": "/admissions",
		"reference_doctype": "Student Admission",
		"role": "Student",
	},
	{
		"title": "Open Admissions",
		"route": "/admission-registers",
		"reference_doctype": "Admission Register",
		"role": "Student",
	},
]

default_roles = [
	{"role": "Student", "doctype": "Student", "email_field": "student_email_id"},
]

accounting_dimension_doctypes = ["Fees", "Fee Schedule", "Fee Structure", "Fee Term"]

global_search_doctypes = {
	"Education": [
		{"doctype": "Article", "index": 1},
		{"doctype": "Video", "index": 2},
		{"doctype": "Topic", "index": 3},
		{"doctype": "Course", "index": 4},
		{"doctype": "Program", "index": 5},
		{"doctype": "Quiz", "index": 6},
		{"doctype": "Question", "index": 7},
		{"doctype": "Fee Schedule", "index": 8},
		{"doctype": "Fee Structure", "index": 9},
		{"doctype": "Student Batch Name", "index": 10},
		{"doctype": "Student", "index": 11},
		{"doctype": "Faculty", "index": 12},
		{"doctype": "Course Activity", "index": 13},
		{"doctype": "Quiz Activity", "index": 14},
		{"doctype": "Course Enrollment", "index": 15},
		{"doctype": "Subject Registration", "index": 16},
		{"doctype": "Student Language", "index": 17},
		{"doctype": "Student Applicant", "index": 17},
		{"doctype": "Assessment Result", "index": 18},
		{"doctype": "Assessment Plan", "index": 19},
		{"doctype": "Grading Scale", "index": 21},
		{"doctype": "Guardian", "index": 20},
		{"doctype": "Student Leave Application", "index": 21},
		{"doctype": "Student Log", "index": 22},
		{"doctype": "Room", "index": 23},
		{"doctype": "Subject Schedule", "index": 24},
		{"doctype": "Student Attendance", "index": 25},
		{"doctype": "Announcement", "index": 26},
		{"doctype": "Student Category", "index": 27},
		{"doctype": "Assessment Group", "index": 28},
		{"doctype": "Campus", "index": 29},
		{"doctype": "Academic Year", "index": 30},
		{"doctype": "Academic Term", "index": 31},
		{"doctype": "School House", "index": 31},
		{"doctype": "Student Admission", "index": 32},
		{"doctype": "Fee Category", "index": 33},
		{"doctype": "Assessment Code", "index": 34},
		{"doctype": "Discussion", "index": 35},
		{"doctype": "Grade Template", "index": 36},
		{"doctype": "Grade Book", "index": 37},
	]
}

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------
# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------
# add methods and filters to jinja environment
# jinja = {
# 	"methods": "education.utils.jinja_methods",
# 	"filters": "education.utils.jinja_filters"
# }

# Installation
# ------------
# before_install = "education.install.before_install"
after_install = "education.install.after_install"
