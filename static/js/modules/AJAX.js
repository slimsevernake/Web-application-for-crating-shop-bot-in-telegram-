function sendAjax({url, method, success, data}) {
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

    if (data) {
        xhr.send(JSON.stringify(data));
    }  	
}