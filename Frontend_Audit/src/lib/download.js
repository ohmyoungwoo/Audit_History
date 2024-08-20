async function download(file_name) {

    //console.log(file_name)
    let _url = 'http://10.182.32.155:8000/api/question/download/' + file_name
    
    const response = await fetch(_url);
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = file_name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

export default download