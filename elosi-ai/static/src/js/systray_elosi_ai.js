import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ElosiAISystray extends Component {
    setup() {
        console.log("Elosi AI Systray Icon setup");
        this.action = useService("action"); // Example of using a service
    }

    onClick() {
        console.log("Elosi AI systray icon clicked!");
        // Example action: Open a view
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Elosi AI Assistant',
            res_model: 'elosi.ai', // Replace with your actual model if needed
            views: [[false, 'form']],
            target: 'new',
        });
    }
}

// Define the template name that will be used in the XML file
ElosiAISystray.template = "elosi_ai.ElosiAISystray";

// Register the component in the systray registry
registry.category("systray").add("elosi_ai.systray", {
    Component: ElosiAISystray,
    sequence: 10, // Adjust sequence as needed
});