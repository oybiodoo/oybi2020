odoo.define('knowsystem.knowsystem_formrenderer', function (require) {
"use strict";

    const FormRenderer = require('web.FormRenderer');

    const KnowSystemFormRenderer = FormRenderer.extend({
    	/**
    	* Fully re-write to replace translation alerts
    	*/
        displayTranslationAlert: function () {},
    });

    return KnowSystemFormRenderer;

});
