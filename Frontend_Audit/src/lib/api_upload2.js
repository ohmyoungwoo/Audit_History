const upload = async (upload_file) => { 

    console.log("upload file", upload_file)

    const formData = new FormData()
    formData.append('file', upload_file)

    //return {"file_name":file.filename, "file_path":file_location, "file_data": formData}

}

export default upload

