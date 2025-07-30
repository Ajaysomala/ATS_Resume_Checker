// /frontend/app.js

document.getElementById('resumeForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const jdText = document.getElementById('jd').value;
  const resumeFile = document.getElementById('resume').files[0];

  if (!jdText || !resumeFile) {
    alert("⚠️ Please provide both JD and Resume.");
    return;
  }

  const formData = new FormData();
  formData.append('jd', jdText);
  formData.append('resume', resumeFile);

  try {
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    document.getElementById('score').innerText = data.match_score || 0;
    document.getElementById('matched').innerText = data.matched_keywords.join(', ') || 'None';
    document.getElementById('unmatched').innerText = data.unmatched_keywords.join(', ') || 'None';

    document.getElementById('result').style.display = 'block';
  } catch (error) {
    alert("🚨 Something went wrong. Is your backend running?");
    console.error(error);
  }
});
