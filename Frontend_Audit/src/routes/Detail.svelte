<script>
    import fastapi from "../lib/api"   //JS로 작성한 공통된 CRUD 함수 ???
    import Error from "../components/Error.svelte"  //오류에 대한 처리

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

<h1>{question.subject}</h1>

<div>
    {question.content}
</div>
<ul>
    {#each question.answers as answer}
        <li>{answer.content}</li>
    {/each}
</ul>
<Error error={error} />
<form method="post">
    <textarea rows="15" bind:value={content}></textarea>
    <input type="submit" value="답변등록" on:click="{post_answer}">
</form>