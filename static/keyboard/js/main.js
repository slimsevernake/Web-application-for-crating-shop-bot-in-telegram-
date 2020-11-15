document.querySelector('.button-add').addEventListener('click', addButton);
document.querySelector('.button-delete').addEventListener('click', deleteButton);
document.querySelector('.delete-all-buttons').addEventListener('click', deleteAllButtons);
document.querySelector('.save-all-buttons').addEventListener('click', saveButtons);

document.querySelector('#b-name').addEventListener('input', changeName);
document.querySelector('#b-text').addEventListener('input', changeText);
document.querySelector('#b-backgroundColor').addEventListener('input', changeBackground);
document.querySelector('#b-color').addEventListener('input', changeColor);
document.querySelector('#b-fontSize').addEventListener('input', changeFontSize);
document.querySelector('#b-vertical').addEventListener('change', changeVertical);
document.querySelector('#b-horizontal').addEventListener('change', changeHorizontal);
document.querySelector('#b-width').addEventListener('change', changeWeight);
document.querySelector('#b-height').addEventListener('change', changeHeight);
document.querySelector('#b-description').addEventListener('change', changeDescription);
document.querySelector('#b-type').addEventListener('change', changeType);
document.querySelector('#b-action').addEventListener('change', changeAction);

function addButton() {
   let container = document.querySelector(`.view-block__view-buttons`);

    let numberOfButtons = document.querySelectorAll(`.view-block__view-buttons .button-base-setting`).length;
    // let buttonName = (!numberOfButtons) ? 'btn_1' : 'btn_' + (Number(document.querySelectorAll(`.view-block__view-buttons .button-base-setting`)[numberOfButtons-1].dataset.name.slice(6))+1);
    let buttonName = (!numberOfButtons) ? 'btn_1' : 'btn_' + (Number(numberOfButtons)+1);

    container.insertAdjacentHTML('beforeEnd', 
            `<input type="radio" name="buttons" id="${buttonName}" class="control-input"/>
             <label for="${buttonName}" data-name="${buttonName}" 
                    class="button-base-setting"
                    onclick="checkStyles(this)">
                    Нова кнопка
             </label>`);

    checkingGrid();
}

function deleteButton() {
    let selectedInput = null;
    
    let inputs = document.querySelectorAll(`.view-block__view-buttons .control-input`);

    if(!inputs.length) return;

    for(let i = 0; i < inputs.length; i++) {
        if(inputs[i].checked) {
            selectedInput = inputs[i];
        }
    }

    if(!selectedInput) {
        alert("Спочатку потрібно обрати кнопку!")
        return;
    }

    selectedInput.remove();
    document.querySelector(`label[for="${selectedInput.id}"`).remove();

    checkingGrid();
}

function deleteAllButtons() {
    document.querySelector('.view-block__view-buttons').innerHTML = '';

    checkingGrid();
}

function saveButtons() {
    let list = makeObject();

    console.log(list);
}

function makeObject() {
    let buttons = document.querySelectorAll(`.button-base-setting`);
    let list = [];
// доробити
    for(let i = 0; i < buttons.length; i++) {
        let newObj = {};
        newObj.name = buttons[i].dataset.name;
        newObj.text = buttons[i].innerHTML.trim();
        newObj.width = (getComputedStyle(buttons[i]).gridColumnEnd - getComputedStyle(buttons[i]).gridColumnStart - 1) || 1;
        newObj.height = (getComputedStyle(buttons[i]).gridRowEnd - getComputedStyle(buttons[i]).gridRowStart - 1) || 1;
        newObj.position = buttons[i] + 1;
        newObj.text_v_align = getComputedStyle(buttons[i]).alignItems;
        newObj.text_h_align = getComputedStyle(buttons[i]).textAlign;
        newObj.text_size = getComputedStyle(buttons[i]).fontSize; 
        newObj.bg_color = getComputedStyle(buttons[i]).backgroundColor;
        newObj.color = getComputedStyle(buttons[i]).color;
        newObj.action_type = buttons[i].dataset.action;
        newObj.description = buttons[i].dataset.description;
        
        list.push(newObj);
    }

    return list;
}

function checkStyles(e) {
    document.querySelector(`#b-name`).value = e.dataset.name;
    document.querySelector(`#b-text`).value = e.innerHTML.trim();
    document.querySelector(`#b-width`).value = ((getComputedStyle(e).gridColumnEnd - getComputedStyle(e).gridColumnStart) - 1) || 1;
    document.querySelector(`#b-height`).value = ((getComputedStyle(e).gridRowEnd - getComputedStyle(e).gridRowStart) - 1) || 1;
    document.querySelector(`#b-backgroundColor`).value = rgb2hex(getComputedStyle(e).backgroundColor);
    document.querySelector(`#b-color`).value = rgb2hex(getComputedStyle(e).color);
    document.querySelector(`#b-vertical`).value = getComputedStyle(e).alignItems;
    document.querySelector(`#b-horizontal`).value = getComputedStyle(e).textAlign;
    document.querySelector(`#b-fontSize`).value = getComputedStyle(e).fontSize.slice(0, -2);

    if(window.matchMedia("(max-width: 970px)").matches) {
        const el = document.querySelector('.control-block');
        el.scrollIntoView({behavior: "smooth"});
    }
}

function changeName(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.dataset.name = e.target.value;
}

function changeText(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.innerHTML = e.target.value;
}

function changeBackground(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.style.backgroundColor = e.target.value;
}

function changeColor(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.style.color = e.target.value;
}

function changeFontSize(e) {   
    let currentButton = defineCurrentButton(e);
    currentButton.style.fontSize = e.target.value + 'px';
}

function changeVertical(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.style.alignItems = e.target.value;
}

function changeHorizontal(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.style.textAlign = e.target.value;
}

function changeDescription(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.dataset.description = e.target.value;
}

function changeType(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.dataset.type = e.target.value;
}

function changeAction(e) {
    let currentButton = defineCurrentButton(e);
    currentButton.dataset.action = e.target.value;
}

function changeWeight(e) { 
    if(checkingGrid()) return;

    let currentButton = defineCurrentButton(e);
    let position = definePosition(currentButton);

    currentButton.style.gridColumnStart = position.gridColumnStart;
    currentButton.style.gridColumnEnd = position.gridColumnStart + (+e.target.value);
}

function changeHeight(e) { 
    if(checkingGrid()) return;

    let currentButton = defineCurrentButton(e); 
    let position = definePosition(currentButton);

    currentButton.style.gridRowStart = position.gridRowStart;
    currentButton.style.gridRowEnd = position.gridRowStart + (+e.target.value);
}