document.addEventListener('DOMContentLoaded', ()=>{
  const attendance = document.getElementById('attendance');
  const study = document.getElementById('study');
  const previous = document.getElementById('previous');
  const gender = document.getElementById('gender');
  const parental = document.getElementById('parental');
  const calcBtn = document.getElementById('calcBtn');
  const scoreEl = document.getElementById('score');
  const letterEl = document.getElementById('letter');

  calcBtn.addEventListener('click', ()=>{
    const a = attendance.value;
    const s = study.value;
    const p = previous.value;
    const g = gender.value;
    const parent = parental.value;

    // Basic validation
    if(!a || !s || !p){
      scoreEl.textContent = 'Please fill all fields.';
      letterEl.textContent = '';
      return;
    }

    // Call backend
    const url = `https://study-chatbot-grade-calculator.onrender.com/grade_predictor?attendance=${encodeURIComponent(a)}&study=${encodeURIComponent(s)}&previous=${encodeURIComponent(p)}&gender=${encodeURIComponent(g)}&parental=${encodeURIComponent(parent)}`;
    fetch(url)
      .then(r => r.json())
      .then(data => {
        if(data.error){
          scoreEl.textContent = 'Error: ' + data.error;
          letterEl.textContent = '';
        }else{
          scoreEl.textContent = data.predicted + '%';
          letterEl.textContent = data.letter;
        }
      })
      .catch(e => {
        scoreEl.textContent = 'Server error.';
        letterEl.textContent = '';
      });
  });
});
