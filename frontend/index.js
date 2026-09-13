console.log("index.js is running")
document.getElementById("login-form").addEventListener("submit", async(event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const API_BASE = "http://127.0.0.1:8000"

    console.log("EMAIL:", email);
    console.log("PASSWORD:", password)

    const response = await fetch(`${API_BASE}/auth/jwt/login`, {
        method: "POST",
        headers: {
            "Content-Type":"application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: email,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok){
        console.log("Login Successful");

        localStorage.setItem("access_token", data.access_token);
        window.location.href = "home.html";
    } else {

        console.error("Login Failed")
        console.error(data.detail)
    }
});


