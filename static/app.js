SERVER_URL = "http://127.0.0.1:5000"

function handleLogin(response){
    console.log(response);
    localStorage.setItem("token", response.credential);
}
function onLinkAdsAccount(){
    window.location.href = `${SERVER_URL}/authorize`;
}