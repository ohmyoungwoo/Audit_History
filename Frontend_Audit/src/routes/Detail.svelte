<script>
    import fastapi from "../lib/api"   //JS로 작성한 공통된 CRUD 함수 ???

    export let params = {}
    let question_id = params.question_id
    let question = {}

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()
</script>

<h1>{question.subject}</h1>

<div>
    {question.content}
</div>