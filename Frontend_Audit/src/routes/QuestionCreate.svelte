<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let audit_date = (new Date()).toJSON().slice(0, 10);
    let file_name = ''  
    let file_path = ''
    let return_value =[]
    let file
    
    // event 에 무언가 있네 ㅠㅠ ????

    function post_question(event) {
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            subject: subject,
            content: content,
            audit_date: audit_date,
            file_name: file_name,
            file_path: file_path,
        }

        //console.log({"post_file_name": params.file_name,"post_file_path": params.file_path})
        console.log({"params": params})

        fastapi('post', url, params, 
            (json) => {
                push("/")
            },
            (json_error) => {
                error = json_error
            }
        )
    }
    //upload 함수를 post_question 안에 넣어야 하나?????

    async function upload() {
        //console.log("Upload 시작3");

        const formData = new FormData();
        formData.append('file', file);
    
        const response = await fetch('http://10.182.32.155:8000/api/question/upload', 
        {
            method: 'POST',
            body: formData,
        });
    
        return_value = await response.json();
        file_name=return_value[0]
        file_path=return_value[1]

        //console.log({"upload--> file_name": file_name, "file_path": file_path});
    }

</script>


<div class="container">
    <h5 class="my-3 border-bottom pb-2">진단결과 등록</h5>
    <Error error={error} />
    
    <div>
        <h6>보고서 업로드</h6>
        <input type="file" on:change="{(event) => (file = event.target.files[0])}" /> 
        <button on:click="{upload}">업로드</button>
    </div>

    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        
        <div class="my-3">
            <label for="audit_date">진단일자</label>
            <input type="date" class="form-control" bind:value="{audit_date}">
        </div>
        
        <button class="btn btn-primary" on:click="{post_question}">저장하기</button>
    </form>
</div>