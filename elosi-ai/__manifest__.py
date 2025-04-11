{
    "name": "Elosi AI",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/elosi_ai_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "elosi-ai/static/src/js/elosi_ai_systray.js",
            "elosi-ai/views/templates.xml"
        ]
    },
    "application": True
}