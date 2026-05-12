async function downloadVideo() {

    const response = await fetch(
        "https://youtubeend-6riv.vercel.app/api/youtube",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: "https://youtu.be/4hcQrh0tI_o?si=8NNAv1wB1EO5HtU"
            })
        }
    );

    const data = await response.json();

    console.log(data);

    if (data.success) {

        window.open(data.download_url);

    } else {

        console.log(data.error);
    }
}

downloadVideo()