import swal from "sweetalert";
import router from '@/router/index.js';
const checkExpiry = function() {
    let info;
    let intervalId;
    fetch('http://127.0.0.1:5000/auth/myinfo',{
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('ac_token')}`
                }
            })
            .then(res => res.json())
            .then(data => { 
                console.log(data);  
            })
            .catch((error) => {
                swal("Error!", "It's us don't worry, we're on it", "error");
                console.error('Error:', error);
            })
            const storedIntervalId = localStorage.getItem('intervalId');
            if (storedIntervalId) {
                clearInterval(Number(storedIntervalId));
            }
            intervalId = setInterval( () => {
                fetch('http://127.0.0.1:5000/auth/myinfo',{
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('ac_token')}`
                    }
                })
                .then(res => res.json())
                .then(data => { 
                    info  = data.user_details;
                    var curr_time = new Date().getTime();
                    var exp_time = info.exp;
                    var timeLeft = Math.floor((exp_time - curr_time/1000)/60)
                    console.log(timeLeft)
                    if (timeLeft <= 10) {
                        swal({
                            title: `Your session is about to expire in ${timeLeft} minutes!`,
                            text: "Do you want to stay logged in?",
                            icon: "warning",
                            buttons: ["Log out", "Stay"]
                        })
                        .then((keepLohgedIn) => {
                            if (keepLohgedIn) {
                                fetch('http://127.0.0.1:5000/auth/refresh_access',{
                                    method: 'GET',
                                    headers: {
                                        Authorization: `Bearer ${localStorage.getItem('ref_token')}`
                                    }
                                })
                                .then(resp => {
                                    if (!resp.ok){
                                        swal("Error fecthing data!", "It's us don't worry, we're on it", "error")
                                        throw new Error(resp.statusText + " " + resp.status)
                                    }
                                    return resp.json()
                                })
                                .then(data => {
                                    localStorage.setItem('ac_token', data.ac_token);
                                    swal("Success!", "Your session has been refreshed!", "success");
                                    clearInterval(intervalId);
                                    checkExpiry();
                                })
                                .catch()
                            } else{
                                swal("Success!", "Logged out successfully", "success")
                                router.push('/');
                                clearInterval(intervalId);
                            }
                        })
                    }
                })
                .catch((error) => {
                    swal("Error!", "It's us don't worry, we're on it", "error");
                    console.error('Error:', error);
                })
            }, 600000)
            localStorage.setItem('intervalId', intervalId.toString());
        }

export default checkExpiry;