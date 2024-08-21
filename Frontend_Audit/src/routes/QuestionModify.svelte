<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    //import upload_modify from "../lib/upload_modify"
    //import upload from "QuestionCreate.svelte"   글로벌 변수 지정 필요함
    import Error from "../components/Error.svelte"
    import { access_token, username, is_login } from "../lib/store"    // Store 변수 생성
    import { get } from 'svelte/store'

    export let params = {}
    const question_id = params.question_id

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let audit_date = (new Date()).toJSON().slice(0, 10);
    let audit_date_end = (new Date()).toJSON().slice(0, 10);
    let audit_year_start = (new Date()).toJSON().slice(0, 4);
    let audit_year_end = (new Date()).toJSON().slice(0, 4);
    let file_name = ''  
    let file_path = ''
    let pdf_file_name = ''  
    let pdf_file_path = ''
    let auditor1 = ''
    let auditor2 = ''
    let auditor3 = ''
    let audit_type = ''
    let company = ''
    let region = ''
    let production = ''
    let return_value =[]
    //let myDate = (new Date()).toJSON().slice(0, 10);
    let file
    let file_pdf
    let audit_type_list = ["품질체제(한국)", "품질체제(해외)", "품질체제(O/S)", "품질체제(사내도급)", "이슈품질", "생산지승인"]
    let company_list = ["LGE", "신성델타", "성철사", "고모텍", "청호", "ACE-TEC", "동인테크", "금원테크", "(주)원현","송기업",
                        "성진테크", "대남테크", "하성기업"]
    let region_list = ["창원", "평택", "구미", "TR(태주)", "PN(남경)", "TA(천진)", "QA(청도)", "VH(하이퐁)",
                       "TH(태국)", "IN(땅그랑)", "IL(노이다)", "IL(푸네)", "SR(사우디)", "AT(터키)", "WR(폴란드)",
                       "EG(이집트)", "RA(러시아)", "MN(몬테레이)", "SP(브라질)","TN(테네시)", "협력사"]
    let production_list = ["냉장고", "세탁기","건조기", "에어컨", "RAC", "SAC", "오븐", "식세기", "청소기", "정수기", "공청기", 
                           "컴프", "컴프(냉장고)","컴프(에어컨)", "실내기", "실외기", "모터", "TV", "모니터", "사이니지", "PC", 
                           "IVI", "로봇", "EV충전", "뷰티"]

    fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
        subject = json.subject
        content = json.content
        audit_date = json.audit_date.slice(0,10)
        audit_date_end = json.audit_date_end.slice(0,10)
        audit_year_start = json.audit_date.slice(0,4)
        audit_year_end = json.audit_date_end.slice(0,4)
        file_name = json.file_name
        file_path = json.file_path
        pdf_file_name = json.pdf_file_name
        pdf_file_path = json.pdf_file_path
        auditor1 = json.auditor1
        auditor2 = json.auditor2
        auditor3 = json.auditor3
        audit_type = json.audit_type
        company = json.company
        region = json.region
        production = json.production
    })

    async function update_question(event) {
        event.preventDefault()
        let url = "/api/question/update"
        let params = {
            question_id: question_id,
            subject: subject,
            content: content,
            audit_date: audit_date,
            audit_date_end: audit_date_end,
            audit_year_start: audit_date.slice(0,4),    // 추가됨
            audit_year_end: audit_date_end.slice(0,4),  // 추가됨
            file_name: file_name,
            file_path: file_path,
            pdf_file_name: pdf_file_name,
            pdf_file_path: pdf_file_path,
            auditor1: auditor1,
            auditor2: auditor2,
            auditor3: auditor3,
            audit_type: audit_type,
            company: company,
            region: region,
            production: production,
        }

        //let return_value = {}

        if (file !== undefined){
            console.log("보고서 Upload 호출 시작");
            return_value = await upload_modify(file);
            console.log("보고서 Upload 호출 완료");
            //console.log("return_value: ", return_value)
            //console.log("return_value[file_name]:", return_value['file_name'])

            params.file_name = return_value['file_name'];
            params.file_path = return_value['file_path'];
        }
        
        if (file_pdf !== undefined){
            return_value = await upload_modify(file_pdf);
            params.pdf_file_name = return_value['file_name'];
            params.pdf_file_path = return_value['file_path'];
        }

        //console.log({"params": params, "url": url})

        fastapi('put', url, params, 
            (json) => {
                push('/detail/'+question_id)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    //async function upload() {
    async function upload_modify(upload_file) {
        let url = "/api/question/upload"
        let _url = 'http://10.182.32.155:8000' + url
        //let content_type = 'application/json'

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

            return_value = await response.json()    // return_value is not defined
            //return_value = response.json()
            //console.log("--resopnse.json:", return_value)

            return return_value
            
        } catch(e) {
            //alert(JSON.stringify(e))
            alert("Upload 실패");
        }
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">진단내용 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <!--<div>
            <h6>변경 보고서 업로드 (현재 파일명: {file_name})</h6>
            <input type="file" on:change="{(event) => (file = event.target.files[0])}"/> -->
            <!--<button on:click="{upload_modify}">업로드</button>-->
        <!--</div>-->
        

        <div class="row mb-3">
            <div class = "col-6">
                <h6>변경 보고서 업로드 (현재 파일명: {file_name})</h6>    
                <input type="file" on:change="{(event) => (file = event.target.files[0])}" /> 
            </div>
            <div class = "col-6">
            <!--<button on:click="{upload}">업로드</button>-->
                <h6>변경 결재 pdf 업로드 (현재 파일명: {pdf_file_name})</h6>    
                <input type="file" on:change="{(event) => (file_pdf = event.target.files[0])}" /> 
            </div>
        </div>


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
        <button class="btn btn-primary" on:click="{update_question}">수정하기</button>
    </form>
</div>