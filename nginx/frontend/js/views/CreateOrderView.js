import { OrderFormComponent } from "../components/OrderFormComponent.js";
import { Section, SectionView } from "./SectionView.js";

export class CreateOrderView extends SectionView {
    render({ onSubmit }) {
        const formComponent = new OrderFormComponent(onSubmit);
        const section = new Section("create-order", formComponent);
        super.render([section]);
    }
}
