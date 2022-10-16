const mf = document.getElementById("mathfield-edit");
const field = mf.getElementsByTagName('math-field')[0];
field.setOptions({
    virtualKeyboardMode: "manual",
    virtualKeyboardLayout: 'dvorak',
    virtualKeyboardContainer: document.getElementById("main")
});
const add_button = mf.getElementsByClassName('add')[0]; 
const delete_button = document.createElement("button");
delete_button.innerHTML = "-";
delete_button.classList.add("delete");
delete_button.style = "display: inline-block; float: right;";

function line_after(node) {
    let next = mf.cloneNode(true);
    node.after(next);
    next.appendChild(delete_button.cloneNode(true));
    next.getElementsByClassName("add")[0].addEventListener('click', add_line);
    next.getElementsByClassName("delete")[0].addEventListener('click', delete_line);
    next.getElementsByTagName('math-field')[0].focus();
}
function add_line(e) {
    line_after(this.parentNode.parentNode);
}
function delete_line(e) {
    this.parentNode.remove();
}

add_button.addEventListener('click', add_line);
