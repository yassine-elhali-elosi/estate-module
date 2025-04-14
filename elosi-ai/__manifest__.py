{
    "name": "Elosi AI",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/elosi_ai_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/elosi-ai/static/src/js/systray_elosi_ai.js",
            "/elosi-ai/static/src/xml/templates.xml",
        ]
    },
    "application": True
}