
const clientId = '1489957';
const redirectUri = 'https://ai.meta.com/blog/large-language-model-llama-meta-ai/';
let accessToken = null;

const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const dashboard = document.getElementById('dashboard');
const metricsDiv = document.getElementById('metrics');

function showDashboard() {
    dashboard.style.display = 'block';
    login.style.display = 'none';
}

function logout() {
    accessToken = null;
    dashboard.style.display = 'none';
    login.style.display = 'block';
    metricsDiv.innerHTML = '';
}

loginBtn.addEventListener('click', () => {
    window.location.href = `https://api.pinterest.com/oauth/?response_type=token&client_id=${clientId}&redirect_uri=${redirectUri}`;
});

logoutBtn.addEventListener('click', logout);

const urlParams = new URLSearchParams(window.location.hash.substr(1));
accessToken = urlParams.get('access_token');

if (accessToken) {
    showDashboard();

    // Fetch and display metrics here using Pinterest API
    // Example:
    metricsDiv.innerHTML = '<p>Followers: 1000</p><p>Likes: 500</p>';
}
