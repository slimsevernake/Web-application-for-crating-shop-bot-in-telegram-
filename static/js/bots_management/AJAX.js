function sendAjax({url, method, success, data}) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let xhr = new XMLHttpRequest();

    xhr.addEventListener('load', function({target}) {
       if (target.status == 200) {
          const response = JSON.parse(target.response);
          success(response);
          console.log(response, 'response');
       }
       console.log(method, 'method');
    });

    xhr.open(method, url);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    if (data){
        xhr.send(data);
    }  	
}
//TODO without jquery django did not take values
function sendAjax2({url_, method_, success_, data_}) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
             async: true,
             method:  method_,
             headers: {"X-CSRFToken": csrftoken},
             url: url_,
             data: data_,
             success:function(response){
                  response = JSON.parse(response);
                  success_(response);
             },
             error : function(){
                 console.log('fail', url_, method_, data_)
             }
         });
}

