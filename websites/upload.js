url = "https://api-inference.huggingface.co/models/Tommybear1136/convnext_mass_detection"
document.getElementById('fileInput').addEventListener('change', function (event) {
    let max = 0
    let res

    const file = event.target.files[0]
    const reader = new FileReader()

    reader.readAsDataURL(file)

    reader.onloadend = () => {
        const data = {
            inputs: {
                image: reader.result.split(',')[1]
            }
        }

        fetch(url, {
            headers: {
                Authorization: "Bearer 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",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            method: "POST",
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)  //可看console決定輸出到螢幕上要什麼
                for (i = 0; i < data.length; i++) {
                    if (data[i].score > max) {
                        max = data[i].score
                        res = data[i].label
                    }
                }

                document.getElementById('responseOutput').innerText = res
            })
            .catch((e) => {
                console.log(e)
            })
    }
})