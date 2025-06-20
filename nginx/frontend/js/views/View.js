export class View {
    constructor(root) {
        this.root = root;
    }
    render(content) {
        this.root.innerHTML = content;
    }
    clear() {
        this.root.innerHTML = "";
    }
}
