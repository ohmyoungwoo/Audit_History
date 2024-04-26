<script>
    import fastapi from "../lib/api"   //JS로 작성한 공통된 CRUD 함수 ???
    import Error from "../components/Error.svelte"  //오류에 대한 처리
    import { link, push } from "svelte-spa-router"
    import { is_login, username } from "../lib/store"

    import moment from "moment/min/moment-with-locales"

    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[]}
    let content = ''
    let error = {detail:[]}
    let date1 = "2024-01-01"; //audit_date test용

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function delete_question(_question_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<div vlass="container my-3">
    <!--질문-->
    <h2 class="border-bottom py-2">{question.subject}</h2>   <!--진단제목-->
    <h6 class="py-2">{question.audit_type} / {question.region} / {question.production} / [{question.file_name}]</h6>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question.content}</div>   <!--진단상세-->
            <div class="d-flex justify-content-end"> <!--진단수정일자-->
                {#if question.modify_date }  
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div> 
                </div>
                {/if}
                
                <div class="badge bg-light text-dark p-2 text-start">   <!--진단실시일자-->
                    <div>{moment(question.audit_date).format("YYYY년 MM월 DD일")}
                        <br>
                         {moment(question.audit_date_end).format("YYYY년 MM월 DD일")}
                    </div>
                    <div class="mb-2">{ question.auditor1 } { question.auditor2 } { question.auditor3 }</div>
                </div>
            </div>

            <div class="my-3"> <!--진단수정/삭제 버튼-->
                {#if question.user && $username === question.user.username }
                <a use:link href="/question-modify/{question.id}" 
                    class="btn btn-sm btn-outline-secondary">진단내용 수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_question(question.id)}>진단내용 삭제</button>
                {/if}
            </div>
            
        </div>
    </div>

    <button class="btn btn-secondary" on:click="{()=>{
        push('/')
    }}">목록으로 이동</button>``

    <!-- 답변 등록 -->
    <!--
    <Error error={error} />
    
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} 
                disabled={$is_login ? "" : "disabled"}
                class="form-control" />
        </div>
        <input type="submit" value="답변등록" 
            class="btn btn-primary {$is_login ? '' : 'disabled'}" 
            on:click="{post_answer}" />  
    </form>
    -->
</div>