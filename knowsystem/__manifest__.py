# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Knowledge Base System",
    "version": "14.0.1.0.6",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/14.0/knowsystem-knowledge-base-system-506",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail",
        "web_editor"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/res_config_settings.xml",
        "views/knowsystem_article_revision.xml",
        "views/knowsystem_article_template.xml",
        "wizard/create_from_template.xml",
        "views/editor/options.xml",
        "views/editor/snippets.xml",
        "views/knowsystem_article.xml",
        "views/knowsystem_section.xml",
        "views/knowsystem_tag.xml",
        "views/knowsystem_tour.xml",
        "views/ir_attachment.xml",
        "reports/article_report.xml",
        "reports/article_report_template.xml",
        "wizard/article_update.xml",
        "wizard/add_to_tour.xml",
        "wizard/article_search.xml",
        "views/menu.xml",
        "wizard/mail_compose_message.xml",
        "data/data.xml"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to build deep and structured knowledge base for internal and external use. Knowledge System. KMS",
    "description": """
For the full details look at static/description/index.html

* Features * 

- Single-view knowledge navigation
- Fast, comfortable, and professional knowledge recording
- Get benefit from your knowledge
- &lt;i class='fa fa-dedent'&gt;&lt;/i&gt; Website documentation builder
- &lt;i class='fa fa-globe'&gt;&lt;/i&gt; Partner knowledge base portal and public knowledge system
- Interactive and evolving knowledge base
- Any business and functional area
- &lt;i class='fa fa-gears'&gt;&lt;/i&gt; Custom knowledge system attributes
- Secured and shared knowledge



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "298.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=83&ticket_version=14.0&url_type_id=3",
}