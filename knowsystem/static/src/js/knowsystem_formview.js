odoo.define('knowsystem.knowsystem_formview', function (require) {
"use strict";

    const KnowSystemFormController = require('knowsystem.knowsystem_formcontroller');
    const KnowSystemFormRenderer = require('knowsystem.knowsystem_formrenderer');
    const FormView = require('web.FormView');
    const viewRegistry = require('web.view_registry');

    const KnowSystemFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KnowSystemFormController,
            Renderer: KnowSystemFormRenderer,
        }),
    });

    viewRegistry.add('knowsystem_form', KnowSystemFormView);

    return KnowSystemFormView;

});