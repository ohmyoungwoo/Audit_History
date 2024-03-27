import qs from "qs"
import { access_token, username, is_login } from "./store"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    // operation : 데이터를 처리하는 방법 ex)get, post, put, delete
    // url : 요청 URL, Backend 서버의 호스트명 이후의 URL만 전달 ex) /api/question/list
    // params : 요청 데이터 ex) {page: 1, keword: "마크다운"}
    // success_callback: API 호출 성공 시 수행할 함수, 전달된 함수에는 API 호출 시 리턴되는 json 값이 입력됨
    // failure_callback: API 호출 실패 시 수행할 함수, 전달된 함수에는 오류 값이 입력됨

    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)   // params를 JSON으로 변경해서 body에 입력

    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }

    let _url = 'http://10.182.32.155:8000'+ url
    
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

    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
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
                    }else if(operation !== 'login' && response.status === 401) { // token time out
                        access_token.set('')
                        username.set('')
                        is_login.set(false)
                        alert("로그인이 필요합니다.")
                        push('/user-login')
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