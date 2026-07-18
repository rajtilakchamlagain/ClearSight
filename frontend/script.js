document.getElementById('track-btn').addEventListener('click', async () => {
    const refImages = document.getElementById('ref-images').files;
    const targetVideo = document.getElementById('target-video').files[0];
    const twinMode = document.getElementById('twin-mode').value;
    const videoCondition = document.getElementById('video-condition').value;

    if (refImages.length === 0 || !targetVideo) {
        alert("Please select both Reference Images and a Target Video.");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < refImages.length; i++) {
        formData.append("reference_images", refImages[i]);
    }
    formData.append("target_video", targetVideo);
    formData.append("twin_mode", twinMode);
    formData.append("video_condition", videoCondition);

    // Update UI
    document.getElementById('track-btn').classList.add('hidden');
    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('results-panel').classList.add('hidden');
    document.getElementById('placeholder').classList.add('hidden');

    try {
        const response = await fetch('/api/track', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === "success") {
            const timestamp = new Date().getTime();
            document.getElementById('result-video').src = data.video_url + "?t=" + timestamp;
            document.getElementById('time-visible').innerText = data.seconds_visible + "s";
            document.getElementById('frames-tracked').innerText = data.frames_tracked;
            document.getElementById('accuracy-metric').innerText = data.accuracy + "%";
            
            document.getElementById('results-panel').classList.remove('hidden');
        } else {
            alert("Error processing video: " + data.message);
            document.getElementById('placeholder').classList.remove('hidden');
        }
    } catch (err) {
        alert("Connection failed. Ensure the FastAPI backend is running.");
        document.getElementById('placeholder').classList.remove('hidden');
        console.error(err);
    } finally {
        document.getElementById('track-btn').classList.remove('hidden');
        document.getElementById('loader').classList.add('hidden');
    }
});
