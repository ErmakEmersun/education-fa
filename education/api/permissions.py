import frappe


# Internal role names are intentionally stable (English) so integrations and
# permission rules do not depend on translated labels.
WORKSPACE_ROLES = {
    "Education Executive Manager": {
        "key": "executive",
        "label": "مدیریت اجرایی",
        "route": "/app/education-executive",
        "accent": "gold",
        "modules": [
            "نمای کلی سامانه",
            "مدیریت آموزش",
            "مدیریت فراگیران",
            "مدیریت مربیان و اساتید",
            "مدیریت کاربران و کارشناسان",
            "گزارش‌های جامع",
            "سوابق ممیزی",
            "تنظیمات سامانه",
        ],
    },
    "Education Training Manager": {
        "key": "training",
        "label": "مدیریت آموزش",
        "route": "/app/education-training",
        "accent": "blue",
        "modules": [
            "دوره‌ها و سرفصل‌ها",
            "برنامه‌ریزی کلاس‌ها",
            "جلسات آموزشی",
            "حضور و غیاب",
            "آزمون‌ها و نمرات",
            "ارزشیابی آموزشی",
            "گزارش‌های آموزشی",
        ],
    },
    "Education Learner Manager": {
        "key": "learners",
        "label": "مدیریت فراگیران",
        "route": "/app/education-learners",
        "accent": "teal",
        "modules": [
            "ثبت و بررسی فراگیر",
            "بانک فراگیران",
            "پرونده آموزشی",
            "کارت فراگیر",
            "ثبت‌نام دوره‌ها",
            "گواهینامه‌ها",
            "گزارش‌های فراگیران",
        ],
    },
    "Education Faculty Manager": {
        "key": "faculty",
        "label": "مدیریت امور مربیان و اساتید",
        "route": "/app/education-faculty",
        "accent": "purple",
        "modules": [
            "ثبت و پرونده مدرس",
            "بانک مربیان و اساتید",
            "تخصص‌ها و مدارک",
            "تخصیص مدرس به دوره",
            "برنامه تدریس",
            "کارت شناسایی مدرس",
            "ارزیابی و حق‌التدریس",
        ],
    },
}

EXECUTIVE_ROLE = "Education Executive Manager"
LEGACY_ROLES = {"Education Manager"}


def get_visible_workspaces(roles):
    """Return workspace metadata without exposing any business records."""
    role_set = set(roles or [])

    if EXECUTIVE_ROLE in role_set:
        workspaces = list(WORKSPACE_ROLES.items())
        return {
            "role": EXECUTIVE_ROLE,
            "can_switch_workspace": True,
            "workspaces": [
                {"key": role_data["key"], "label": role_data["label"],
                 "route": role_data["route"], "accent": role_data["accent"],
                 "modules": role_data["modules"]}
                for _role, role_data in workspaces
            ],
        }

    # A specialized account receives one workspace only, even if it has
    # accidentally been assigned more than one specialist role.
    for role_name, role_data in WORKSPACE_ROLES.items():
        if role_name in role_set:
            return {
                "role": role_name,
                "can_switch_workspace": False,
                "workspaces": [{
                    "key": role_data["key"], "label": role_data["label"],
                    "route": role_data["route"], "accent": role_data["accent"],
                    "modules": role_data["modules"],
                }],
            }

    # Backward compatibility for existing installations. The legacy role is
    # mapped to the training workspace, not to executive-wide access.
    if role_set & LEGACY_ROLES:
        role_data = WORKSPACE_ROLES["Education Training Manager"]
        return {
            "role": "Education Manager",
            "can_switch_workspace": False,
            "workspaces": [{
                "key": role_data["key"], "label": role_data["label"],
                "route": role_data["route"], "accent": role_data["accent"],
                "modules": role_data["modules"],
            }],
        }

    return {"role": None, "can_switch_workspace": False, "workspaces": []}


def has_app_permission():
    """Allow the Education app only to explicitly authorized management roles."""
    if frappe.session.user == "Administrator":
        return True

    roles = set(frappe.get_roles(frappe.session.user))
    return bool(roles.intersection(set(WORKSPACE_ROLES) | LEGACY_ROLES))


@frappe.whitelist()
def get_workspace_context():
    """Return only the current user's permitted workspace navigation metadata."""
    if frappe.session.user == "Guest":
        frappe.throw("برای مشاهده محیط کاری وارد سامانه شوید.", frappe.PermissionError)

    context = get_visible_workspaces(frappe.get_roles(frappe.session.user))
    if not context["workspaces"]:
        frappe.throw("شما مجوز ورود به محیط مدیریت آموزش‌یار را ندارید.", frappe.PermissionError)

    return context
