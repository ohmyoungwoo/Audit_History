<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let audit_date = (new Date()).toJSON().slice(0, 10);
    let audit_date_end = (new Date()).toJSON().slice(0, 10);
    let file_name = ''  
    let file_path = ''
    let auditor1 = ''
    let auditor2 = ''
    let auditor3 = ''
    let audit_type = ''
    let company = 'LGE'
    let region = ''
    let production = ''
    let return_value =[]
    let file
    let audit_type_list = ["품질체제(한국)", "품질체제(해외)", "품질체제(O/S)", "품질체제(사내도급)", "이슈품질", "생산지승인"]
    let company_list = ["LGE", "신성델타", "성철사", "고모텍", "청호", "ACE-TEC", "동인테크", "금원테크", "(주)원현","송기업",
                        "성진테크", "대남테크", "하성기업"]
    let region_list = ["창원", "평택", "구미", "TR(태주)", "PN(남경)", "TA(천진)", "QA(청도)", "VH(하이퐁)",
                       "TA(태국)", "IN(땅그랑)", "IL(노이다)", "IL(푸네)", "SR(사우디)", "AT(터키)", "WR(폴란드)",
                       "EG(이집트)", "RA(러시아)", "MN(몬테레이)", "SP(브라질)","TN(테네시)", "협력사"]
    let production_list = ["냉장고", "세탁기","건조기", "에어컨", "RAC", "SAC", "오븐", "식세기", "청소기", "정수기", "공청기", 
                           "컴프", "컴프(냉장고)","컴프(에어컨)", "실내기", "실외기", "모터", "TV", "모니터", "사이니지", "PC", 
                           "IVI", "로봇", "EV충전", "뷰티"]

    
    // event 에 무언가 있네 ㅠㅠ ????

    async function post_question(event) {
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            subject: subject,
            content: content,
            audit_date: audit_date,
            audit_date_end: audit_date_end,
            file_name: file_name,
            file_path: file_path,
            auditor1: auditor1,
            auditor2: auditor2,
            auditor3: auditor3,
            audit_type: audit_type,
            company: company,
            region: region,
            production: production,
        }

        //console.log({"post_file_name": params.file_name,"post_file_path": params.file_path})
        
        //params.file_name, params.file_path = await upload()
        
        //params.file_name = await upload()
        return_value = await upload()
        params.file_name = return_value[0]
        params.file_path = return_value[1]

        //console.log({"params": params})

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

    //async function upload() {
    async function upload() {
        console.log("Upload 시작");

        const formData = new FormData();
        formData.append('file', file);
    
        const response = await fetch('http://10.182.32.155:8000/api/question/upload', 
        {
            method: 'POST',
            body: formData,
        });
    
        return_value = await response.json();
        
        //console.log({"Upload 완료/ 파일명:": return_value[0]});
        //console.log({"upload--> file_name": file_name, "file_path": file_path});

        return return_value

    }

</script>


<div class="container">
    <h5 class="my-3 border-bottom pb-2">진단결과 등록</h5>
    <Error error={error} />
    
    <div>
        <h6>보고서 업로드</h6>    
        <input type="file" on:change="{(event) => (file = event.target.files[0])}" /> 
        <!--<button on:click="{upload}">업로드</button>-->
    </div>

    <form method="post" class="my-3">
        <div class="row mb-3">
            <div class = "col-3">
                <label for="audit_type">유형</label>
                <select type="text" class="form-control" bind:value="{audit_type}">
                    {#each audit_type_list as audit_type_item }
                        <option value="{audit_type_item}">{audit_type_item}</option>
                    {/each}
                </select>
            </div>

            <div class = "col-3">
                <label for="region">회사</label>
                <select type="text" class="form-control" bind:value="{company}">
                    {#each company_list as company_item }
                        <option value="{company_item}">{company_item}</option>
                    {/each}
                </select>
            </div>

            <div class = "col-3">
                <label for="region">사업장</label>
                <select type="text" class="form-control" bind:value="{region}">
                    {#each region_list as region_item }
                        <option value="{region_item}">{region_item}</option>
                    {/each}
                </select>
            </div>

            <div class = "col-3">
                <label for="production">제품군</label>
                <select type="text" class="form-control" bind:value="{production}">
                    {#each production_list as production_item }
                        <option value="{production_item}">{production_item}</option>
                    {/each}
                </select>
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
        
        <div class ="row mb-3">
            <div class = "col-4">
                <label for="audit_date">진단일자(시작)</label>
                <input type="date" class="form-control" bind:value="{audit_date}">
            </div>
            <div class = "col-4"> 
                <label for="audit_date_end">진단일자(종료)</label>
                <input type="date" class="form-control" bind:value="{audit_date_end}">
            </div>
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
            <div class = "col-4">
                <label for="auditor3">진단자3</label>
                <input type="text" class="form-control" bind:value="{auditor3}">
            </div>
        </div>
        
        <button class="btn btn-primary" on:click="{post_question}">저장하기</button>
    </form>
</div>