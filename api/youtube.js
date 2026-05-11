const ytdl = require("@distube/ytdl-core");

export default async function handler(req, res) {

    // =========================
    // CORS
    // =========================
    res.setHeader(
        "Access-Control-Allow-Origin",
        "*"
    );

    res.setHeader(
        "Access-Control-Allow-Methods",
        "GET, POST, OPTIONS"
    );

    res.setHeader(
        "Access-Control-Allow-Headers",
        "Content-Type"
    );

    // =========================
    // OPTIONS
    // =========================
    if (req.method === "OPTIONS") {

        return res.status(200).end();
    }

    // =========================
    // ONLY POST
    // =========================
    if (req.method !== "POST") {

        return res.status(405).json({
            success: false,
            error: "Method not allowed"
        });
    }

    try {

        // =========================
        // GET URL
        // =========================
        const { url } = req.body;

        if (!url) {

            return res.status(400).json({
                success: false,
                error: "No URL provided"
            });
        }

        // =========================
        // VALIDATE URL
        // =========================
        if (!ytdl.validateURL(url)) {

            return res.status(400).json({
                success: false,
                error: "Invalid YouTube URL"
            });
        }

        // =========================
        // GET INFO
        // =========================
        const info = await ytdl.getInfo(url);

        // =========================
        // BEST FORMAT
        // =========================
        const format = ytdl.chooseFormat(
            info.formats,
            {
                quality: "highest",
                filter: "audioandvideo"
            }
        );

        // =========================
        // RESPONSE
        // =========================
        return res.status(200).json({
            success: true,
            title: info.videoDetails.title,
            thumbnail: info.videoDetails.thumbnails?.pop()?.url,
            author: info.videoDetails.author?.name,
            lengthSeconds: info.videoDetails.lengthSeconds,
            views: info.videoDetails.viewCount,
            download_url: format.url
        });

    } catch (error) {

        return res.status(500).json({
            success: false,
            error: error.message
        });
    }
}