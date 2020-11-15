function getCurrDate() {
    let date = new Date();

    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    return year + "-" + month + "-" + day;
}

document.querySelector('#to-date').value = getCurrDate();
document.querySelector('#to-date').max = getCurrDate();

document.querySelector('#get-graphic').addEventListener('click', drawGraphic);

let db = {
    botsStat: [
        { y: '2020-09-25', v: 1, t: 2, total: 3},
        { y: '2020-09-26', v: 3, t: 2, total: 4},
        { y: '2020-09-27', v: 3, t: 3, total: 6},
        { y: '2020-09-28', v: 5, t: 4, total: 9},
        { y: '2020-09-29', v: 6, t: 5, total: 11},
        { y: '2020-09-30', v: 8, t: 7, total: 15},
        { y: '2020-10-01', v: 8, t: 8, total: 16},
        { y: '2020-10-02', v: 8, t: 8, total: 16},
        { y: '2020-10-03', v: 8, t: 10, total: 18},
        { y: '2020-10-04', v: 9, t: 11, total: 20}
    ],
    usersStat: [ 
        { y: '2020-09-25', v: 41, t: 61, total: 102},
        { y: '2020-09-26', v: 42, t: 67, total: 109},
        { y: '2020-09-27', v: 90, t: 102, total: 192},
        { y: '2020-09-28', v: 120, t: 136, total: 156},
        { y: '2020-09-29', v: 136, t: 136, total: 272},
        { y: '2020-09-30', v: 198, t: 220, total: 418},
        { y: '2020-10-01', v: 250, t: 274, total: 524},
        { y: '2020-10-02', v: 299, t: 324, total: 623},
        { y: '2020-10-03', v: 346, t: 354, total: 700},
        { y: '2020-10-04', v: 354, t: 370, total: 724}
    ],
    usersGrowth: [ 
        { y: '2020-09-25', v: 2, t: 2, total: 4},
        { y: '2020-09-26', v: 2, t: 6, total: 8},
        { y: '2020-09-27', v: 50, t: 38, total: 88},
        { y: '2020-09-28', v: 35, t: 35, total: 70},
        { y: '2020-09-29', v: 18, t: 5, total: 23},
        { y: '2020-09-30', v: 72, t: 86, total: 158},
        { y: '2020-10-01', v: 53, t: 64, total: 117},
        { y: '2020-10-02', v: 49, t: 52, total: 101},
        { y: '2020-10-03', v: 50, t: 30, total: 80},
        { y: '2020-10-04', v: 10, t: 16, total: 26}
    ],
    usersOutput: [ 
        { y: '2020-09-25', v: 0, t: 0, total: 0},
        { y: '2020-09-26', v: 1, t: 0, total: 1},
        { y: '2020-09-27', v: 2, t: 3, total: 5},
        { y: '2020-09-28', v: 5, t: 1, total: 6},
        { y: '2020-09-29', v: 2, t: 5, total: 7},
        { y: '2020-09-30', v: 10, t: 2, total: 12},
        { y: '2020-10-01', v: 1, t: 10, total: 11},
        { y: '2020-10-02', v: 0, t: 2, total: 2},
        { y: '2020-10-03', v: 3, t: 0, total: 3},
        { y: '2020-10-04', v: 2, t: 0, total: 2}
    ]
}

function drawGraphic() {
    let start  = document.querySelector('#from-date').value;
    let end  = document.querySelector('#to-date').value;

    let type = document.querySelector('#data-type').value;

    let allDate = db[type];

    let partDate = [];

    for(let i = 0; i < allDate.length; i++) {
        if(allDate[i].y >= start) {
            partDate.push(allDate[i]);
            if(allDate[i].y === end) break;
        }
    }

    some.setData(partDate);
}

let some = Morris.Area({
    element: 'area-example',
    data: db.botsStat,
    xkey: 'y',
    lineColors:['#5cb85c','#f0ad4e', '#8cbbf5'],
    ykeys: ['v', 't', 'total'],
    postUnits:'',
    labels: ['Viber', 'Telegram', 'Загальна']
});