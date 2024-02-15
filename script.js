document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('camera');
    const captureButton = document.getElementById('capture');
    const imageInput = document.getElementById('imageInput');
    const uploadForm = document.querySelector('form');

    let stream;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((userStream) => {
            stream = userStream;
            video.srcObject = userStream;
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
        });

    captureButton.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append('image', new File([blob], 'photo.png', { type: 'image/png' }));

            // Make a POST request to your sound generation API
            fetch('YOUR_SOUND_API_URL', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Assuming your API returns a URL to the generated sound
                const soundUrl = data.soundUrl;

                // Play the sound
                const audio = new Audio(soundUrl);
                audio.play();
            })
            .catch(error => console.error('Error generating sound:', error))
            .finally(() => {
                // Stop the camera stream after capturing the photo
                if (stream) {
                    const tracks = stream.getTracks();
                    tracks.forEach(track => track.stop());
                }

                // Reset the input field (optional)
                imageInput.value = '';
            });
        }, 'image/png');
    });
});