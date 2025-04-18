
const fetch = require("node-fetch");

exports.handler = async function(event, context) {
  const body = JSON.parse(event.body);
  const apiKey = event.headers.authorization;

  try {
    const response = await fetch("https://api.salesloft.com/v2/cadence_imports.json", {
      method: "POST",
      headers: {
        "Authorization": apiKey,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    const text = await response.text();
    return {
      statusCode: response.status,
      body: text
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
