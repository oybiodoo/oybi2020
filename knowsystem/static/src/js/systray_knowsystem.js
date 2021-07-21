odoo.define('knowsystem.systray_knowsystem', function (require) {
"use strict";

    var session = require('web.session')
    const SystrayMenu = require('web.SystrayMenu');
    const Widget = require('web.Widget');
    const Context = require('web.Context');
    const { _lt } = require('web.core');
    
    const webClient = require('web.web_client');

    const systrayKnowsystem = Widget.extend({
        template:'systrayKnowSystem',
        events: {'click': '_onOpenKnowSystemSearch'},
        /**
         * Overwrite to pass to widget whether knowsystem systray is turned on
        */
        init: function () {
            this.show_knowsystem_quick = session.show_knowsystem_quick;
            this._super.apply(this, arguments);
        },
        /**
         * The method to open wizard for searching KnowSystem
        */
        async _onOpenKnowSystemSearch(ev) {
            event.preventDefault();
            event.stopPropagation();
            var currentStateController = webClient._current_state;
            var curModel = false;
            var curIds = []; 
            if (currentStateController) {
                if (currentStateController.model) {
                    curModel = currentStateController.model;
                    if (currentStateController.id) {
                        curIds.push(parseInt(currentStateController.id))
                    };
                };
            };
            const defaultTags = await this._rpc({
                model: "knowsystem.tag",
                method: "action_return_tags_for_document",
                args: [curModel, curIds],
            })
            const KnowSystemContext = {
                default_tag_ids: defaultTags,
                default_no_selection: true,
                form_view_ref: "knowsystem.article_search_form_view",
            };
            const context = new Context(session.user_context, KnowSystemContext).eval();
            const action = {
                name: _lt("Articles Quick Search"),
                type: 'ir.actions.act_window',
                res_model: 'article.search',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            this.do_action(action);
        },
    });

    SystrayMenu.Items.unshift(systrayKnowsystem);

    return {systrayKnowsystem: systrayKnowsystem,};

});
