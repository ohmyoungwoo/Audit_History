import { access_token, username, is_login } from "../lib/store"    // Store 변수 생성
import { get } from 'svelte/store'

async function upload(upload_file) {
    let url = "/api/question/upload"
    let _url = 'http://10.182.32.155:8000' + url
    //let content_type = 'application/json'
    let return_value = {}

    let options = { 
        method: 'post',
        //headers: { "Content-Type": content_type },
        headers: {},
    }

    console.log("-Upload 함수 시작", _url)

    try {

        const _access_token = get(access_token)
        if (_access_token) {
            options.headers["Authorization"] = "Bearer " + _access_token
        }

        const formData = new FormData()
        formData.append('file', upload_file)

        options['body'] = formData

        console.log("-Upload Back end 시작")
        //console.log(options)

        //const response = await fetch(_url, {method: 'post', body: formData})
        const response = await fetch(_url, options)
        

        console.log("-Upload Back end 완료")
        //console.log("--resopnse:", response)
        return_value = await response.json()
        //console.log("--resopnse.json:", return_value)

        return return_value
        
    } catch(e) {
        //alert(JSON.stringify(e))
        alert("Upload 실패");
    }

}



export default upload

