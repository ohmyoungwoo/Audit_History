<script>
    let file;
    
    async function upload() {
        const formData = new FormData();
        formData.append('file', file);
    
        const response = await fetch('http://10.182.32.155:8000/api/question-create/file/', 
        {
            method: 'POST',
            body: formData,
        });
    
        const result = await response.json();
        console.log(result);
    }
</script>

<input type="file" on:change="{(event) => (file = event.target.files[0])}" />
<button on:click="{upload}">업로드</button>