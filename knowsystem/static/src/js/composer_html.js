odoo.define('knowsystem.composer_html', function (require) {
"use strict";

    const fieldRegistry = require('web.field_registry');
    const FieldHtml = require('web_editor.field.html');
    const dialogs = require('web.view_dialogs');
    const rpc = require('web.rpc');
    const Context = require('web.Context');
    
    const { _lt, qweb } = require('web.core');

    const KnowSystemComposerHtml = FieldHtml.extend({
        events: {"click .open_knowsystem": "_onOpenKnowSystem",},
        /**
         * Rewrite to render quick parts
        */
        _renderEdit: function () {
            this._super.apply(this, arguments);
            rpc.query({
                model: "knowsystem.section",
                method: "action_check_option",
                args: ["composer"],
            }).then(function (need) {
                if (need) {
                    var quickKnowSystem = qweb.render("ComposerQuickLink", {});
                    self.$('.note-toolbar').append(quickKnowSystem);
                };
            });
        },
        /**
         * @private
         * @param {MouseEvent} ev
         * The method to open article quick search
        */
        async _onOpenKnowSystem(event) {
            // The method to open article quick search
            var self = this;
            var defaultTags = await self._rpc({
                model: "knowsystem.tag",
                method: "action_return_tags_for_document",
                args: [self.record.data['model'], [parseInt(self.record.data['res_id'])]],
            });
            const KnowSystemContext = {
                default_tag_ids: defaultTags,
                default_no_selection: false,
            };
            const context = new Context(self.record.context, KnowSystemContext).eval();
            const dialog = new dialogs.FormViewDialog(self, {
                res_model: "article.search",
                title: _lt("Articles quick search"),
                context: context,
                readonly: false,
                shouldSaveLocally: false,
                buttons: [
                    {
                        text: (_lt("Update Body")),
                        classes: "btn-primary",
                        click: function () {
                            dialog._save().then(
                                self._onApplyArticleAction(dialog, "add_to_body"),
                            );
                        },
                    },
                    {
                        text: (_lt("Share URL")),
                        classes: "btn-primary",
                        click: function () {
                            dialog._save().then(
                                self._onApplyArticleAction(dialog, "share_url"),
                            );
                        },
                    },
                    {
                        text: (_lt("Attach PDF")),
                        classes: "btn-primary",
                        click: function () {
                            dialog._save().then(
                                self._onApplyArticleAction(dialog, "add_pdf"),
                            );
                        },
                    },
                    {
                        text: (_lt("Close")),
                        classes: "btn-secondary o_form_button_cancel",
                        close: true,
                    },
                ],
            });
            dialog.open();
         
        },
        /**
         * @private
         * @param {dialog} FormViewDialog instance
         * @param {action} - char - name of action to do
         * The method to updat composer body
        */
        async _onApplyArticleAction(dialog, action) {
            var self = this;
            var record = dialog.form_view.model.get(dialog.form_view.handle);
            var articles = record.data.selected_article_ids.data;
            var articleIDS = [];
            _.each(articles, function (art) {articleIDS.push(parseInt(art.res_id))});
            var article = await self._rpc({
                model: 'knowsystem.article',
                method: 'proceed_article_action',
                args: [articleIDS, action],
            })
            if (article) {
                if (article.descr && article.descr.length !== 0) {
                    self.$content = self.$('.note-editable:first');
                    self.$content.append(article.descr);
                };
                if (article.url && article.url.length !== 0) {
                    self.$content = self.$('.note-editable:first');
                    self.$content.append(article.url);
                };
                if (article.attachment_ids) {
                    self._onAttachmentChange(article.attachment_ids);
                };
            };
            dialog.close();
        },
    });

    fieldRegistry.add('know_system_composer', KnowSystemComposerHtml);
    return KnowSystemComposerHtml

});
