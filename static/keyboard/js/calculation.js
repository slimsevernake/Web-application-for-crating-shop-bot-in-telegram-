// checking if grid is full
function checkingGrid() {
    let numberOfButtons = document.querySelectorAll(`.button-base-setting`).length;  
    let r = definePosition(document.querySelectorAll(`.button-base-setting`)[numberOfButtons-1]);

    if(r.gridColumnEnd == 7 && r.gridRowEnd == 3) {
        document.querySelector('.button-add').disabled = true;
        return true;
    } else {
        document.querySelector('.button-add').disabled = false;
        return false;
    }
}

// define current position
function definePosition(button) {
    let container = document.querySelector('.view-block__main-panel');
    let position = {};
    
    let hPart = Math.round(container.scrollWidth / 6);
    let leftSide = button.offsetLeft;

    if(leftSide == 0) {
        position.gridColumnStart = 1;
    } else if((leftSide >= hPart - 2) && (leftSide <= hPart + 2)) {
        position.gridColumnStart = 2;
    } else if((leftSide >= hPart*2 - 2) && (leftSide <= hPart*2 + 2)) {
        position.gridColumnStart = 3;
    } else if((leftSide >= hPart*3 - 2) && (leftSide <= hPart*3 + 2)) {
        position.gridColumnStart = 4;
    } else if((leftSide >= hPart*4 - 2) && (leftSide <= hPart*4 + 2)) {
        position.gridColumnStart = 5;
    } else if((leftSide >= hPart*5 - 2) && (leftSide <= hPart*5 + 2)) {
        position.gridColumnStart = 6;
    }

    position.gridColumnEnd = position.gridColumnStart + Math.round(button.offsetWidth / hPart);

    let vPart = Math.round(container.scrollHeight / 2);
    let topSide = button.offsetTop;

    if(topSide == 0) {
        position.gridRowStart = 1;
    } else if((topSide >= vPart - 2) && (topSide <= vPart + 2)) {
        position.gridRowStart = 2;
    } else if((topSide >= vPart*2 - 2) && (topSide <= vPart*2 + 2)) {
        position.gridRowStart = 3;
    }

    position.gridRowEnd = position.gridRowStart + Math.round(button.offsetHeight / vPart);

    return position;
}

// define button to change styles
function defineCurrentButton(e) {
    let inputs = document.querySelectorAll(`.control-input`);

    for(let i = 0; i < inputs.length; i++) {
        if(inputs[i].checked) {
            selectedInput = inputs[i];
        }
    }
    return document.querySelector(`label[for="${selectedInput.id}"`);
}

// convert rgb to hex
function rgb2hex(rgb) {
    rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    
    function hex(x) {
        return ("0" + parseInt(x).toString(16)).slice(-2);
    }

    return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
}