<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    export let params = {}
    const question_id = params.question_id

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let file_name = ''  
    let file_path = ''
    let auditor1 = ''
    let auditor2 = ''
    let audit_type = ''
    let region = ''
    let production = ''
    let audit_date = (new Date()).toJSON().slice(0, 10);
    let myDate = (new Date()).toJSON().slice(0, 10);
    let file

    fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
        subject = json.subject
        content = json.content
        audit_date = json.audit_date
        file_name = json.file_name
        file_path = json.file_path
        auditor1 = json.auditor1
        auditor2 = json.auditor2
        audit_type = json.audit_type
        region = json.region,
        production = json.production
    })

    function update_question(event) {
        event.preventDefault()
        let url = "/api/question/update"
        let params = {
            question_id: question_id,
            subject: subject,
            content: content,
            audit_date: audit_date,
            file_name: file_name,
            file_path: file_path,
            auditor1: auditor1,
            auditor2: auditor2,
            audit_type: audit_type,
            region: region,
            production: production,
        }
        fastapi('put', url, params, 
            (json) => {
                push('/detail/'+question_id)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    async function upload_modify() {
        console.log("Upload 변경");

        //const formData = new FormData();
        //formData.append('file', file);
    
        //const response = await fetch('http://10.182.32.155:8000/api/question/upload', 
        //{
        //    method: 'POST',
        //    body: formData,
        //});
    
        //return_value = await response.json();

        //file_name=return_value[0]
        //file_path=return_value[1]

        //console.log({"upload--> file_name": file_name, "file_path": file_path});
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">진단내용 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div>
            <h6>보고서 업로드</h6>
            <input type="file" on:change="{(event) => (file = event.target.files[0])}"/> 
            <button on:click="{upload_modify}">업로드</button>
        </div>

        <div class="row mb-3">
            <div class = "col-4">
                <label for="audit_type">유형</label>
                <input type="text" class="form-control" bind:value="{audit_type}">
            </div>

            <div class = "col-4">
                <label for="region">사업장</label>
                <input type="text" class="form-control" bind:value="{region}">
            </div>
            
            <div class = "col-4">
                <label for="production">제품군</label>
                <input type="text" class="form-control" bind:value="{production}">
            </div>
        </div>

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

        <div class="row mb-3">
            <div class = "col-4">
                <label for="auditor1">진단자1</label>
                <input type="text" class="form-control" bind:value="{auditor1}">
            </div>
            <div class = "col-4">
                <label for="auditor2">진단자2</label>
                <input type="text" class="form-control" bind:value="{auditor2}">
            </div>
        </div>
        <button class="btn btn-primary" on:click="{update_question}">수정하기</button>
    </form>
</div>