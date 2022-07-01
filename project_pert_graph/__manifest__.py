# Copyright 2016-2020 Onestein (<http://www.onestein.eu>)
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Project PERT Graph",
    "version": "13.0.1.0.0",
    "category": "Project",
    "website": "https://dkgoup.fr",
    "summary": "Enables to calculate critical path by PERT graph",
    "author": "joannes landy",
    "license": "AGPL-3",

    "depends": ["project",
                "web_timeline",

                "project_task_add_very_high",

                "hr_timesheet",
                ],
    "data": [
        "views/project_task_view.xml",
        "views/project_task_type_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
