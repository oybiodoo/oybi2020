odoo.define('knowsystem.ActionMenus', function (require) {
'use strict';

    const components = {ActionMenus: require('web.ActionMenus'),};
    const { patch } = require('web.utils');
    const Context = require('web.Context');

    patch(components.ActionMenus, 'knowsystem/static/src/components/action_menus.js', {
        async willStart() {
            await this._super.apply(this, arguments);
            this.knowsystemQuickSearch = await this._setKnowSystem(this.props);
        },
        async willUpdateProps(nextProps) {
            await this._super.apply(this, arguments);
            this.knowsystemQuickSearch = await this._setKnowSystem(nextProps);
        },
        /**
         * @private
         * @param {Object} props
         * @returns {Promise<Object[]>}
         */
        async _setKnowSystem(props) {
            const knowsystemQuickSearch = await this.rpc({
                model: "knowsystem.section",
                method: "action_check_option",
                args: ["form"],
            })
            return knowsystemQuickSearch;
        },    
        /**
         * @private
         * @param {MouseEvent} ev
         */
        async _onOpenKnowSystem(ev) {
            ev.stopPropagation();
            const defaultTags = await this.rpc({
                model: "knowsystem.tag",
                method: "action_return_tags_for_document",
                args: [this.env.action.res_model, this.props.activeIds],
            })
            const KnowSystemContext = {
                default_tag_ids: defaultTags,
                default_no_selection: true,
                form_view_ref: "knowsystem.article_search_form_view",
            };
            const context = new Context(this.props.context, KnowSystemContext).eval();
            const action = {
                name: this.env._t("Articles Quick Search"),
                type: 'ir.actions.act_window',
                res_model: 'article.search',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            this.trigger('do-action', {
                action: action,
                options: {},
            });
        },
    });

});
