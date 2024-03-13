const fastapi = (operation, url, params, success_callback, failure_callback) => {
    // operation : 데이터를 처리하는 방법 ex)get, post, put, delete
    // url : 요청 URL, Backend 서버의 호스트명 이후의 URL만 전달 ex) /api/question/list
    // params : 요청 데이터 ex) {page: 1, keword: "마크다운"}
    // success_callback: API 호출 성공 시 수행할 함수, 전달된 함수에는 API 호출 시 리턴되는 json 값이 입력됨
    // failure_callback: API 호출 실패 시 수행할 함수, 전달된 함수에는 오류 값이 입력됨

    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)   // params를 JSON으로 변경해서 body에 입력

    let _url = 'http://127.0.0.1:8000'+ url

    //let _url = import.meta.env.VITE_SERVER_URL + url  // 작동 안함 (이유를 모르겠음 ????)
    //alert(import.meta.env.VITE_SERVER_URL)

    if(method === 'get') {
        _url += "?" + new URLSearchParams(params) // 파라미터를 GET 방식에 맞게끔 URLSearchParams를 사용하여 파라미터를 조립
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => {
            if(response.status === 204) {
                if(success_callback) {
                    success_callback()
                }
                return
            }

            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {
                            success_callback(json)
                        }
                    }else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })
        })
}

export default fastapi