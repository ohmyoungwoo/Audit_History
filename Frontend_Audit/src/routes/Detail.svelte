<script>
    import fastapi from "../lib/api"   //JS로 작성한 공통된 CRUD 함수 ???
    import Error from "../components/Error.svelte"  //오류에 대한 처리
    import { push } from "svelte-spa-router"
    import { is_login } from "../lib/store"

    import moment from "moment/min/moment-with-locales"

    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content
        }
        fastapi('post', url, params,
            (json) => {
                content = ''
                error = {detail:[]}     // 오류 발행 후 다시 입력값을 조정하여 성공하면 오류 메시지를 없애기 위해
                get_question()
            },
            (err_json) => {           // Error 발생하면 failure_callback에 의해 err_json 이 {detail: ...} 형태로 전달됨
                error = err_json
            }
        )
    }
</script>

<div vlass="container my-3">
    <!--질문-->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question.content}</div>
            <div class="d-flex justify-content-end"></div>
                <div class="badge bg-light text-dark p-2">
                    {moment(question.create_date).format("YYYY년 MM월 DD일")}</div>
        </div>
    </div>

    <button class="btn btn-secondary" on:click="{()=>{
        push('/')
    }}">목록으로 이동</button>

    <!-- 답변 등록 -->

    <Error error={error} />
    <!--
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