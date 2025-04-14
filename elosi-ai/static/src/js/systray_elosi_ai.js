import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ElosiAISystray extends Component {
    setup() {
        console.log("Elosi AI Systray Icon setup");
        this.action = useService("action");
    }

    onClick() {
        console.log("Elosi AI systray icon clicked!");

        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Elosi AI Assistant',
            res_model: 'elosi.ai',
            views: [[false, 'form']],
            target: 'new',
        });
    }
}

ElosiAISystray.template = "elosi_ai.ElosiAISystray";

registry.category("systray").add("elosi_ai.systray", {
    Component: ElosiAISystray,
    sequence: 1,
});