document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('estimatorForm');
  const resultDiv = document.getElementById('result');

  form.addEventListener('submit', function(e) {
      e.preventDefault();

      const formData = new FormData(form);
      const dataEntries = Object.fromEntries(formData.entries());
      console.log("krushang: ", dataEntries)

      fetch('/estimate', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(dataEntries),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data, "krushang")
          let resultHTML = `<h2>Winning Probability for Second Batting Team is: ${(data.probability * 100).toFixed(2)}%</h2>`;
          resultHTML += '<h3>Similar Scenario:</h3>';
          const scenario = data.scenarios[0];
          resultHTML += `
              <p>Team A: ${scenario.team_a}, Team B: ${scenario.team_b}</p>
              <p>Team Batting First: ${scenario.batting_first}</p>
              <p>Runs Scored: ${scenario.runs_scored}</p>
              <p>Wickets Fallen: ${scenario.wickets_fallen}</p>
              <p>Overs Completed: ${scenario.overs_completed}</p>
              <p>Runs Required to Win: ${scenario.runs_required}</p>
              <p>Winning Team: ${scenario.winning_team}</p>
          `;
          resultHTML += '<h3>Factors Considered:</h3>';
          for (const [factor, value] of Object.entries(data.factors)) {
              resultHTML += `<p>${factor}: ${value.toFixed(2)}</p>`;
          }
          resultDiv.innerHTML = resultHTML;
      })
      .catch(error => {
          console.error('Error:', error);
          resultDiv.innerHTML = '<p>An error occurred. Please try again.</p>';
      });
  });
});