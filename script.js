const form = document.getElementById('predictForm');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const loader = document.getElementById('loader');
const button = document.getElementById('predictBtn');

form.addEventListener('submit', async function (e) {
  e.preventDefault();

  resultDiv.style.display = 'none';
  errorDiv.textContent = '';
  loader.style.display = 'block';
  button.disabled = true;
  button.style.opacity = 0.7;

  const data = {
    Area: parseFloat(document.getElementById('area').value),
    Bedrooms: parseInt(document.getElementById('bedrooms').value),
    Bathrooms: parseInt(document.getElementById('bathrooms').value),
    Floors: parseInt(document.getElementById('floors').value),
    YearBuilt: parseInt(document.getElementById('yearbuilt').value),
    Location: document.getElementById('location').value,
    Condition: document.getElementById('condition').value,
    Garage: document.getElementById('garage').value
  };

  try {
    const res = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const json = await res.json();

    if (res.ok) {
      loader.style.display = 'none';
      button.disabled = false;
      button.style.opacity = 1;

      resultDiv.style.display = 'block';
      resultDiv.innerHTML = `
        <div class="fade-in">
          <p>Estimated House Price:</p>
          <h2>${json.prediction}</h2>
        </div>
      `;
    } else {
      throw new Error(json.error || 'Prediction failed.');
    }
  } catch (err) {
    loader.style.display = 'none';
    button.disabled = false;
    button.style.opacity = 1;
    errorDiv.textContent = err.message || 'Network or system error. Please check if Flask is running.';
  }
});
