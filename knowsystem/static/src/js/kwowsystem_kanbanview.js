odoo.define('knowsystem.kwowsystem_kanbanview', function (require) {
"use strict";

    const KnowSystemKanbanController = require('knowsystem.kwowsystem_kanbancontroller');
    const KnowSystemKanbanModel = require('knowsystem.kwowsystem_kanbanmodel');
    const KnowSystemKanbanRenderer = require('knowsystem.knowsystem_kanbanrender');
    const KanbanView = require('web.KanbanView');
    const viewRegistry = require('web.view_registry');
    const { _lt } = require('web.core');

    const KnowSystemKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: KnowSystemKanbanController,
            Model: KnowSystemKanbanModel,
            Renderer: KnowSystemKanbanRenderer,
        }),
        display_name: _lt('Knowledge Base'),
        groupable: false,
    });

    viewRegistry.add('knowsystem_kanban', KnowSystemKanbanView);

    return KnowSystemKanbanView;

});
