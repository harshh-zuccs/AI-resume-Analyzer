document.getElementById("uploadForm").addEventListener("submit", async function(e) {

    e.preventDefault(); // prevents page reload

    const fileInput = document.getElementById("resumeFile");
    const jobRole = document.getElementById("jobRole").value;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("job_role", jobRole);

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze-pdf", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("result").textContent = JSON.stringify(data, null, 2);

    } catch (error) {
        console.error(error);
        document.getElementById("result").textContent = "Error connecting to API";
    }
});