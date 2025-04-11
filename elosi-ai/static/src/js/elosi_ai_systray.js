import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class MySystrayWidget extends Component {
    setup() {
        console.log("MySystrayWidget setup");
    }

    onClick() {
        alert("My systray icon clicked!");
    }
}
MySystrayWidget.template = "elosi_ai.MySystrayWidgetTemplate";

registry.category("systray").add("elosi_ai.my_systray_widget", {
    Component: MySystrayWidget,
});
