async function upload(temp_file) {
    //console.log("Upload 시작");

    const formData = new FormData();
    formData.append('file', temp_file);

    const response = await fetch('http://10.182.32.155:8000/api/question/upload', 
    {
        method: 'POST',
        body: formData,
    });

    
    
    //console.log({"Upload 완료/ 파일명:": return_value[0]});
    //console.log({"upload--> file_name": file_name, "file_path": file_path});

    return await response.json();

}



export default upload

