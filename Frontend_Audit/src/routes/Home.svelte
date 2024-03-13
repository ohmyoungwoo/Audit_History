<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'

    let question_list = []
    let size = 10
    let page = 0
    let total = 0
    $: total_page = Math.ceil(total/size)  // 스벨트에서 변수앞에 $: 기호를 붙이면 해당 변수는 반응형 변수, 
                                           // total 변수의 값이 API 호출로 인해 그 값이 변하면 total_page 변수의 값도 실시간으로 재 계산된다

    function get_question_list(_page) {
        let params ={
            page: _page,
            size: size,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            page = _page
            total = json.total
        })
    }

    get_question_list(0)
</script>

<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="table-dark">
            <th>번호</th>
            <th>진단 제목</th>
            <th>작성일시</th>
            <th>작성자</th>
            <th>진단보고서</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr>
            <td>{i+1}</td>
            <td>
                <a use:link href="/detail/{question.id}">{question.subject}</a>
            </td>
            <td>{question.create_date}</td>
        </tr>
        {/each}
        </tbody>
    </table>

    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list(page-1)}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= page-5 && loop_page <= page+5} 
        <li class="page-item {loop_page === page && 'active'}">
            <button on:click="{() => get_question_list(loop_page)}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list(page+1)}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->

    <a use:link href="/question-create" class="btn btn-primary">진단 결과 등록하기</a>
</div>