odoo.define('knowsystem.many2many_kanban', function (require) {
"use strict";

    const fieldRegistry = require('web.field_registry');
    const relationalFields = require('web.relational_fields');

    const knowSystemKanban = relationalFields.FieldMany2Many.extend({
        events: _.extend({}, relationalFields.FieldMany2Many.prototype.events, {
            'click .article_select': '_articleSelect',
        }),
        /**
         * @private
         * @param {MouseEvent} event
         * The method to add to selection
        */        
        _articleSelect: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var articleId = parseInt(event.currentTarget.id);
            this.trigger_up('field_changed', {
                dataPointID: this.dataPointID,
                changes: _.object(["selected_article_ids"], [{
                    operation: 'ADD_M2M',
                    ids: [{"id": articleId}],
                }])
            });
        },
        /**
         * @private
         * @param {MouseEvent} event
         * The method to save the views
        */ 
        _onOpenRecord: function (event) {
            this._super.apply(this, arguments);
            var articleID = parseInt(event.target.id);
            this._rpc({
                model: "knowsystem.article",
                method: 'update_number_of_views',
                args: [[articleID]],
                context: {},
            })
        },
    });

    fieldRegistry.add('many2many_knowsystem_kanban', knowSystemKanban);
});
