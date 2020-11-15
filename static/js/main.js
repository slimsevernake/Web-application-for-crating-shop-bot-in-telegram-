let list = null;

window.addEventListener('load', function() {

    sendAjax2({
//        url: "http://localhost:3003/get-moderators",
        url_: "/ajax_get_moderators/",
        method_: "get",
        data_: {},
        success_(response) {
            $('.select2-search').select2({
                data: response
            });
            $.when($("select").select2()).done(function(){
                $('.select2').css({'width' : '363px', 'height' : "55px", 'fontSize':'0.875em', 'fontWeight':'300',
                                'margin' : '10px', 'border':'1px solid', 'borderColor':'rgba(0, 0, 0, 0.2)'});
                $('.select2-selection').css({'border' : '0'});
            });
        }
    });

    sendAjax2({
        url_: "/ajax_get_channels/",
//        url: "http://localhost:3003/get-channels",
        method_: "get",
        data_: {},
        success_(response) {
            list = new ChannelsList(response);
            list.listInit();
            list.render('.main');
            selectTarget();
        }
    });
});

document.querySelector('.main__add-button').addEventListener('click', function() {
    list.addItem();
    list.render('.main');
})

document.querySelector('.button-send').addEventListener('click', function() {
    let form = document.querySelector('.channel_update');
    let objToSend = {};

    let inputs = document.querySelectorAll('.modal__field');

    for(let i = 0; i < inputs.length; i++) {
        objToSend[inputs[i].name] = inputs[i].type == 'checkbox' ? inputs[i].checked : inputs[i].value;
    }

    console.log('TO SEND -------------- ' + objToSend);

    form.reset();
    sendAjax2({
//        url: "http://localhost:3003/update-channel",
        url_: '/ajax_channels_update/',
        method_: "post",
        data_: objToSend,
        success_(res) {
            list = new ChannelsList(res);       
            list.listInit();
            list.render('.main');
            selectTarget();
        }
    });
})

function selectTarget() {
    let channelsEditButtons = document.querySelectorAll('.main__edit');
    let targetItem = null
    
    for(let i = 0; i < channelsEditButtons.length; i++) {
        channelsEditButtons[i].addEventListener('click', function(event) {
            targetItem = list.getChannel(event.target.parentNode.id);
            
            let inputs = document.querySelectorAll('.modal__field');

            for(let i = 0; i < inputs.length; i++) {
                if(inputs[i].type == 'checkbox') {
                    inputs[i].checked = targetItem[inputs[i].name];
                } else {
                    inputs[i].value = targetItem[inputs[i].name];
                }   
            }
        })
    }
}
    