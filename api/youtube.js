const fs = require("fs");
const path = require("path");
const { execFile } = require("child_process");

function runYtDlp(args) {
    return new Promise((resolve, reject) => {
        execFile(
            "yt-dlp",
            args,
            {
                windowsHide: true
            },
            (error, stdout, stderr) => {
                if (error) {
                    return reject(
                        new Error(stderr || error.message)
                    );
                }

                resolve(stdout);
            }
        );
    });
}

async function getVideo(url) {
    const cookiesPath = path.resolve(
        process.cwd(),
        "loveinter.txt"
    );

    if (!fs.existsSync(cookiesPath)) {
        throw new Error("cookies.txt file not found");
    }

    const output = await runYtDlp([
        "--dump-single-json",
        "--no-warnings",
        "--no-check-certificates",
        "--cookies",
        cookiesPath,
        "--user-agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        url
    ]);

    const info = JSON.parse(output);

    if (!info || !info.formats || info.formats.length === 0) {
        throw new Error("No formats found");
    }

    const audioVideoFormats = info.formats.filter(
        (format) =>
            format.url &&
            format.vcodec !== "none" &&
            format.acodec !== "none"
    );

    const videoOnlyFormats = info.formats.filter(
        (format) =>
            format.url &&
            format.vcodec !== "none" &&
            format.acodec === "none"
    );

    const audioOnlyFormats = info.formats.filter(
        (format) =>
            format.url &&
            format.vcodec === "none" &&
            format.acodec !== "none"
    );

    const selectedFormat =
        audioVideoFormats.sort(
            (a, b) => (b.height || 0) - (a.height || 0)
        )[0] ||
        videoOnlyFormats.sort(
            (a, b) => (b.height || 0) - (a.height || 0)
        )[0] ||
        audioOnlyFormats.sort(
            (a, b) => (b.abr || 0) - (a.abr || 0)
        )[0];

    if (!selectedFormat || !selectedFormat.url) {
        throw new Error("No playable format found");
    }

    return {
        success: true,
        title: info.title,
        author: info.uploader,
        thumbnail: info.thumbnail,
        duration: info.duration,
        selected: {
            format_id: selectedFormat.format_id,
            ext: selectedFormat.ext,
            height: selectedFormat.height,
            resolution: selectedFormat.resolution,
            vcodec: selectedFormat.vcodec,
            acodec: selectedFormat.acodec,
            filesize:
                selectedFormat.filesize ||
                selectedFormat.filesize_approx
        },
        download_url: selectedFormat.url,
        formats_count: info.formats.length
    };
}

// API HANDLER
module.exports = async function handler(req, res) {
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

    if (req.method === "OPTIONS") {
        return res.status(200).end();
    }

    if (req.method === "GET") {
        return res.status(200).json({
            success: true,
            message: "YouTube API is running. Send POST request with url."
        });
    }

    if (req.method !== "POST") {
        return res.status(405).json({
            success: false,
            error: "Method not allowed"
        });
    }

    try {
        const { url } = req.body;

        if (!url) {
            return res.status(400).json({
                success: false,
                error: "No URL provided"
            });
        }

        const data = await getVideo(url);

        return res.status(200).json(data);
    } catch (error) {
        return res.status(500).json({
            success: false,
            error: error.message
        });
    }
};